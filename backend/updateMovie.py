import requests

response = requests.post('http://127.0.0.1:5000/movies/update', \
    json={'id': 6, 'name': 'Name', 'description': 'changed', 'link': 'www.google.de'})

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())