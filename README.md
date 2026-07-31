# 🛡️ Cybersecurity Portfolio

A comprehensive collection of security research, vulnerability analysis, CTF writeups, and penetration testing projects. This repository documents my journey in offensive and defensive cybersecurity.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Featured Writeups](#featured-writeups)
- [Repository Structure](#repository-structure)
- [Skills & Topics](#skills--topics)
- [Quick Start](#quick-start)
- [Contact](#contact)

---

## 🎯 Overview

This repository contains:
- **CTF Writeups** - Detailed solutions to TryHackMe and other platforms
- **Vulnerability Research** - CVE analysis and exploitation techniques
- **Binary Exploitation** - Reverse engineering and crackme solutions
- **Web Security** - Application pentesting and vulnerability assessment
- **Tools & Scripts** - Custom security tools and automation scripts
- **Educational Content** - Learning materials and practical examples

**Experience Level:** Intermediate to Advanced  
**Focus Areas:** Web Application Security, Reverse Engineering, Privilege Escalation

---

## ⭐ Featured Writeups

### [Node.js Deserialization RCE - "Jax Sucks Alot"](./tryhackme/CTFs/Jax_sucks_alot/)

**Critical vulnerability chain combining deserialization attacks with privilege escalation**

- **Platform:** TryHackMe
- **Difficulty:** Medium/Hard
- **CVSS Score:** 9.8 (Critical)
- **Topics:** Unsafe deserialization, code execution, reverse shells, sudo exploitation

**Key Findings:**
- Unsafe `eval()` on untrusted serialized objects
- Immediate code execution via IIFE pattern
- Privilege escalation through misconfigured sudo
- Complete system compromise (user → root)

[📖 Full Technical Writeup](./tryhackme/CTFs/Jax_sucks_alot/README.md)

---

## 📁 Repository Structure

```
cybersec/
├── 📚 TryHackMe/
│   ├── CTFs/                          # CTF Challenge Writeups
│   │   ├── Jax_sucks_alot/           # Node.js RCE (Featured)
│   │   ├── W1seGuy/                  # Encryption & Decryption
│   │   ├── TakeOver/                 # DNS & Subdomain Enumeration
│   │   ├── brickHeist/               # (Add summary)
│   │   └── fools_mate/               # (Add summary)
│   └── WebAppPentesting/             # Web app testing techniques
│
├── 🔍 CVE Research/
│   ├── Node_js_deserialization/      # CVE analysis & PoC
│   └── RoundCube_vul/                # RoundCube vulnerability (CVE-2025-49113)
│
├── 💾 Binary Exploitation/
│   ├── crackmes/                     # Reverse engineering challenges
│   │   ├── crackme01-09              # Progressive difficulty
│   │   └── Makefile                  # Build system
│   └── reverseme/                    # Reverse engineering labs
│
├── 🎓 Learning Resources/
│   ├── LiveOverFlow/                 # LiveOverFlow YouTube tutorials
│   │   ├── Simple crackme assembly
│   │   ├── Uncrackable crackme
│   │   └── Modern stack exploitation
│   ├── Hacker101/                    # HackerOne learning path
│   │   ├── encryptedPastebin/        # Crypto challenges
│   │   ├── Micro-CMS v2/             # CMS vulnerabilities
│   │   └── photoGallery/             # Photo app exploitation
│   └── PortSwigger/                  # Web Security Academy
│       ├── SQLi labs/                # SQL Injection
│       └── Blind SQLi/               # Blind SQL Injection
│
├── 🛠️ Tools & Scripts/
│   ├── my_tools/                     # Custom security tools
│   │   ├── scan.c / scan.py          # Network scanning utilities
│   │   ├── ai_scan.c                 # Advanced scanning
│   │   └── nodejsshell.py            # Payload generation
│   └── paths/                        # Pentesting scripts
│
├── 🔐 Cryptography/
│   └── tools_web.txt                 # Cryptographic tools reference
│
├── 🔎 Discovery/
│   └── nmap/                         # Network reconnaissance
│
├── Linux Security/
│   └── root_privilege_escalation.txt # Privilege escalation techniques
│
└── 📖 README.md                       # This file
```

---

## 🎓 Skills & Topics

### Web Application Security
- ✅ SQL Injection (Error-based, Blind, Time-based)
- ✅ Deserialization vulnerabilities
- ✅ Server-side template injection
- ✅ Cross-Site Scripting (XSS)
- ✅ Cross-Site Request Forgery (CSRF)
- ✅ Authentication bypass
- ✅ Directory traversal & enumeration

### Network & System Security
- ✅ Nmap reconnaissance & scanning
- ✅ Service enumeration
- ✅ Privilege escalation (Linux/Windows)
- ✅ Sudo misconfiguration exploitation
- ✅ Firewall bypass techniques

### Reverse Engineering & Binary Exploitation
- ✅ Disassembly & analysis (GDB)
- ✅ Crackme solving
- ✅ Buffer overflow basics
- ✅ Assembly language understanding
- ✅ Static & dynamic analysis

### Cryptography & Encoding
- ✅ XOR encryption
- ✅ Base64 encoding/decoding
- ✅ Hash identification & cracking
- ✅ Symmetric & asymmetric cryptography

### Tools & Technologies
- **Penetration Testing:** Burp Suite, SQLMap, Metasploit
- **Reconnaissance:** Nmap, Gobuster, Shodan
- **Reverse Engineering:** GDB, Radare2, IDA (basics)
- **Exploitation:** Custom Python/Node.js scripts
- **Cryptanalysis:** John the Ripper, Hashcat
- **Version Control:** Git, GitHub

---

## 🚀 Quick Start

### Prerequisites
```bash
# Core tools
sudo pacman -S nmap gobuster sqlmap git python nodejs

# Optional tools
python-pip
pip install --break-system-packages burpsuite requests paramiko pycryptodome
```

### Clone & Explore
```bash
git clone https://github.com/aymn-bc/cybersec.git
cd cybersec

# View featured writeup
cat tryhackme/CTFs/Jax_sucks_alot/README.md

# Run custom tools
python my_tools/nodejsshell.py
```

### Featured Writeup Deep Dive
```bash
cd tryhackme/CTFs/Jax_sucks_alot/
# Read full technical analysis with remediation strategies
cat README.md
```

---

## 📊 Statistics

| Category | Count | Status |
|----------|-------|--------|
| CTF Writeups | 5+ | ✅ Ongoing |
| CVE Research | 2 | ✅ Active |
| Crackmes | 9 | ✅ Complete |
| Learning Labs | 10+ | ✅ In Progress |
| Custom Tools | 4+ | ✅ Maintained |

---

## 🔒 Security Best Practices

This repository contains **educational content only** for authorized security testing and learning purposes:

- ✅ All exploits tested in controlled environments
- ✅ No active vulnerabilities disclosed responsibly
- ✅ Follows responsible disclosure principles
- ✅ Educational and documentation purposes only

**Disclaimer:** Unauthorized access to computer systems is illegal. All tools and techniques are for authorized testing only.

---

## 🎯 Current Focus

- Advanced web application exploitation
- Binary exploitation & reverse engineering
- CVE research & vulnerability analysis
- Building custom exploitation tools
- Networking fundamentals & system hardening

---

## 📈 Learning Path

```
Beginner
  ├── CTF Challenges (TryHackMe, HackTheBox)
  ├── Web fundamentals (PortSwigger)
  └── Basic reverse engineering (Crackmes)
        ↓
Intermediate
  ├── Advanced SQLi & injection attacks
  ├── Deserialization vulnerabilities
  ├── Privilege escalation techniques
  └── Custom tool development
        ↓
Advanced
  ├── CVE research & analysis
  ├── Complex binary exploitation
  ├── Zero-day research
  └── Security research publications
```

---

## 📚 References & Resources

### Educational Platforms
- [TryHackMe](https://www.tryhackme.com/) - Hands-on cybersecurity training
- [HackerOne](https://www.hackerone.com/) - Bug bounty & learning
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Web security
- [LiveOverFlow](https://www.youtube.com/c/LiveOverflow) - Binary exploitation tutorials

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Web vulnerability framework
- [CWE](https://cwe.mitre.org/) - Common Weakness Enumeration
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1) - Vulnerability scoring
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Security standards

### Tools Documentation
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
- [GDB Command Reference](https://sourceware.org/gdb/current/onlinedocs/gdb/)

---

## 🤝 Contributing

This is a personal learning portfolio. Feedback and suggestions are welcome!

- **Found an issue?** Open a GitHub issue
- **Have improvements?** Submit a pull request
- **Questions?** Reach out via LinkedIn or email

---

## 📞 Contact

- **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/aymen-bc)
- **GitHub:** [@aymn-bc](https://github.com/aymn-bc)
- **Email:** [your.email@example.com]

---

## 📄 License

This repository contains educational content for authorized security testing and learning purposes only. See LICENSE file for details.

---

## 🎓 Acknowledgments

- TryHackMe for excellent CTF challenges
- HackerOne for bug bounty learning
- LiveOverFlow for binary exploitation tutorials
- PortSwigger for web security training
- The cybersecurity community for knowledge sharing

---

**Last Updated:** July 2026  
**Status:** 🟢 Actively Maintained

⭐ **If you find this helpful, please star the repository!**