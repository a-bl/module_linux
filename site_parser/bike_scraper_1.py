import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = 'https://www.rad-krefeld.de/Hollandr%C3%A4der.html'
params = {'seiten_id': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 0

itemsName = []
itemsPrice = []

while params['seiten_id'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='artikeluebersicht col-xs-12 thumbnail')

    for n, i in enumerate(items, start=n + 1):
        itemName = i.find('h2').text.strip()
        itemsName.append(itemName)
        itemPrice = i.find('span', class_='preisanzeige').text
        itemsPrice.append(itemPrice)
        print(f'{n}:  {itemName},\n     '
              f'Price: {itemPrice}')

    # [-2] the penultimate value because the last is "Next"
    last_page_num = 2
    pages = last_page_num if pages < last_page_num else pages
    params['seiten_id'] += 1

df = pd.DataFrame({
    'Name': itemsName,
    'Price': itemsPrice,
    'Category': "Hollandräder"
})
df.to_csv('bikes_1.csv', index=False)

url = 'https://www.rad-krefeld.de/Trekkingr%C3%A4der.html'
params = {'seiten_id': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 0

itemsName = []
itemsPrice = []

while params['seiten_id'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='artikeluebersicht col-xs-12 thumbnail')

    for n, i in enumerate(items, start=n + 1):
        itemName = i.find('h2').text.strip()
        itemsName.append(itemName)
        itemPrice = i.find('span', class_='preisanzeige').text
        itemsPrice.append(itemPrice)
        print(f'{n}:  {itemName},\n     '
              f'Price: {itemPrice}')

    # [-2] the penultimate value because the last is "Next"
    last_page_num = 4
    pages = last_page_num if pages < last_page_num else pages
    params['seiten_id'] += 1

df = pd.DataFrame({
    'Name': itemsName,
    'Price': itemsPrice,
    'Category': "Trekkingräder"
})
df.to_csv('bikes_1.csv', mode='a', header=False, index=False)

url = 'https://www.rad-krefeld.de/E-Räder.html'
params = {'seiten_id': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 0

itemsName = []
itemsPrice = []

while params['seiten_id'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='artikeluebersicht col-xs-12 thumbnail')

    for n, i in enumerate(items, start=n + 1):
        itemName = i.find('h2').text.strip()
        itemsName.append(itemName)
        itemPrice = i.find('span', class_='preisanzeige').text
        itemsPrice.append(itemPrice)
        print(f'{n}:  {itemName},\n     '
              f'Price: {itemPrice}')

    # [-2] the penultimate value because the last is "Next"
    last_page_num = 11
    pages = last_page_num if pages < last_page_num else pages
    params['seiten_id'] += 1

df = pd.DataFrame({
    'Name': itemsName,
    'Price': itemsPrice,
    'Category': "E-Räder"
})
df.to_csv('bikes_1.csv', mode='a', header=False, index=False)

url = 'https://www.rad-krefeld.de/Bakfiets_und_Seniorenr%C3%A4der.html'
params = {'seiten_id': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 0

itemsName = []
itemsPrice = []

while params['seiten_id'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='artikeluebersicht col-xs-12 thumbnail')

    for n, i in enumerate(items, start=n + 1):
        itemName = i.find('h2').text.strip()
        itemsName.append(itemName)
        itemPrice = i.find('span', class_='preisanzeige').text
        itemsPrice.append(itemPrice)
        print(f'{n}:  {itemName},\n     '
              f'Price: {itemPrice}')

    # [-2] the penultimate value because the last is "Next"
    last_page_num = 2
    pages = last_page_num if pages < last_page_num else pages
    params['seiten_id'] += 1

df = pd.DataFrame({
    'Name': itemsName,
    'Price': itemsPrice,
    'Category': "Bakfiets und Seniorenräder"
})
df.to_csv('bikes_1.csv', mode='a', header=False, index=False)