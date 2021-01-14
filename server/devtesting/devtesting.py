import requests

BASE = "http://127.0.0.1:5000/"

if __name__ == '__main__':
    response = requests.get(BASE + "personinfo/simon")
    print(response.json())