import requests

url = "http://127.0.0.1:8001/"

payload = {
    "username": "Karina",
    "mail": "user@example.com",
    "password": "password1"
}
payload1 = {
    "grant_type": "",
    "username": "Karina",
    "password": "password1",
    "scope": "",
    "client_id": "",
    "client_secret": ""
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# response0 = requests.request("POST", url=url + 'auth/register', headers=headers, json=payload)
# print(response0.text)

response = requests.request("POST", url + 'auth', headers=headers, data=payload1)
print(response.text, response.cookies)

response2 = requests.request("GET", url + 'user/1/favorites', cookies=response.cookies)
print(response2.status_code, response2.text)

# response2 = requests.request("GET", url + '/')
# print(response2.status_code, response2.text)
