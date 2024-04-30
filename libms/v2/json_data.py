import requests

def get_all_books():
    response = requests.get('http://127.0.0.1:5000/allbooksdata')
    data = response.json()
    return data

def get_all_borrowed_book():
    response = requests.get('http://127.0.0.1:5000/borrowedbooksdata')
    data = response.json()
    return data