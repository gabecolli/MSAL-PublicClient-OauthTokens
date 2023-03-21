import requests

endpoint = "http://localhost:5056/api/auth/login/"

headers = {
    'Content-Type': 'application/json',
}


body = {
    "username" : 'test',
    "password" : 'test'
}

response = requests.post(endpoint, headers=headers, json=body)




