import requests

response = requests.post('http://127.0.0.1:5000/api/login', json={'username': 'admin', 'password': 'admin123'})
token = response.json()['access_token']
print(token)  # Aquí verás la cadena completa sin cortar
