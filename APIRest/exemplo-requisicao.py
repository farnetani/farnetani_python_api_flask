import requests
import json

url = 'http://127.0.0.1:8080/api/cliente'
headers = {'Content-Type': 'application/json'}

filters = [dict(name='nome', op='like', val='%Junior%')]
params = dict(q=json.dumps(dict(filters=filters)))

print('Filtrando: ' + str(params))
response = requests.get(url, params=params, headers=headers)
#assert response.status_code == 200
print(response.json())
print(response.status_code)