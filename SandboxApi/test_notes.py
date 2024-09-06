import requests

r = requests.post("http://localhost:8000/signup", json={"uname": "first", "password": "Abc123", "repassword": "Abc123"})
print(r.request.path_url)
print(r)
token = r.json()

r = requests.post("http://localhost:8000/note", json={"title": "First Note", "description": "My first note in this app!", "token": token})
print(r.request.path_url)
print(r.json())

r = requests.post("http://localhost:8000/note", json={"title": "Second Note", "description": "My second note in this app!", "token": token})
print(r.request.path_url)
print(r.json())

r = requests.post("http://localhost:8000/signup", json={"uname": "second", "password": "dfgdfg", "repassword": "dfgdfg"})
print(r.request.path_url)
print(r)
token = r.json()

r = requests.post("http://localhost:8000/note", json={"title": "First Note!!", "description": "My first note in this app!", "token": token})
print(r.request.path_url)
print(r.json())

r = requests.post("http://localhost:8000/note", json={"title": "Second Note!!", "description": "My second note in this app!", "token": token})
print(r.request.path_url)
print(r.json())

r = requests.get("http://localhost:8000/notes")
print(r.request.path_url)
print(r.json())

r = requests.get("http://localhost:8000/note/0")
print(r.request.path_url)
print(r.json())

r = requests.post("http://localhost:8000/login", json={"uname": "first", "password": "Abc123"})
print(r.request.path_url)
print(r.json())
