import requests
import json

r = requests.post('https://core-echoes.herokuapp.com/add_route', data=json.dumps([1, 2, 3, 4]))
print r
