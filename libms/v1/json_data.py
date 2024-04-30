import json
import requests
if __name__ == '__main__':
    response = requests.get('http://127.0.0.1:5000/allbooks')
    data = response.json()
    print(data)
    print()
    if data != []:
        li = [i for i in data[0].keys()]
        print(li)
        li = [i for i in data[0].values()]
        print(li)

def get_inventory_data():
    response = requests.get('http://127.0.0.1:5000/allbooks')
    data = response.json()
    return data
def get_borrowed_data():
    response = requests.get('http://127.0.0.1:5000/booksborrowed')
    data = response.json()
    return data