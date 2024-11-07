import requests

endpoints = 'http://localhost:8000/demo/'
# endpoints = 'http://localhost:8000/api/products/list-create'

get_response = requests.post(endpoints, json={"title": "generic list createAPIView"})
# print(get_response.json())
print(get_response.status_code)