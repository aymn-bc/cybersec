# SQL Injection Brute-forcer

A blind SQL injection brute-forcer built for PortSwigger Web Security Academy labs.
Implemented in both Python and C (libcurl).

## Usage

### Python
```bash
pip install requests
python3 scan.py
```

### C
```bash
gcc -o scan scan.c -lcurl -Wall -Wextra -O2
./scan
```

## Disclaimer
This tool is for educational purposes only.
Only use it on legal, authorized targets such as PortSwigger Web Security Academy labs.

## Author
Aymen