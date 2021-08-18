import requests

response = requests.post('http://127.0.0.1:5000/movies/add', \
    json={'name': 'Name', 'description': 'Description', 'link': 'www.google.de'})

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())