import requests
import time

BASE = "http://127.0.0.1:8080/"
# BASE = "http://127.0.0.1:5000/"

if __name__ == '__main__':
    response = requests.get(BASE + "personinfo/simon")
    while(1):
        time.sleep(30)
    print(response.json())