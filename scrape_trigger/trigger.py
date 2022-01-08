import requests 

ngrok_url = 'https://b01f-79-66-31-24.ngrok.io'
endpoint = f'{ngrok_url}/box-office-mojo-scraper'

r = requests.post(endpoint, json={})
print(r.json()['data'])