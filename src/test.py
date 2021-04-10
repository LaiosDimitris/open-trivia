import requests

response = requests.get('http://rpg-api.com/weapons').json()

print(response)