import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = 'https://bikefair.org/listings?location%5B0%5D=51.33684119999999&location%5B1%5D=5.9482681&height' \
      '=&delivery_distance=10&country_code=NL&sort%5Bkey%5D=best_match&sort%5Bdirection%5D=asc '
params = {'page': 1}
# set a number greater than the number of the first page to start the cycle
pages = 48
n = 0

itemsName = []
itemsPrice = []
itemsLocation = []
itemsFrameSize = []
itemsCondition = []
to_json = []

while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='px-3 w-full sm:w-1/2 lg:w-1/2 xl:w-1/3 mb-6')
    # print(items)

    for n, i in enumerate(items, start=n+1):
        # itemName = i.find('h3', class_='font-bold line-clamp-2 h-12 px-2').text.strip()
        itemName = i.find('h3', class_='font-bold line-clamp-2 h-12 px-2').text.split(",")[0]
        itemsName.append(itemName)
        itemPrice = i.find('div', class_='font-bold text-base').text.strip()
        itemsPrice.append(itemPrice)
        itemLocation = i.find_all('div', class_='text-gray-800')[0].text.strip()
        itemsLocation.append(itemLocation)
        itemFrameSize = i.find_all('div', class_='text-gray-800')[1].text.split()
        itemFrameSize = ' '.join(itemFrameSize)
        itemsFrameSize.append(itemFrameSize)
        itemCondition = i.find('div', class_='ml-4 truncate').text.strip()
        itemsCondition.append(itemCondition)
        # print(f"{n}: {itemPrice}")
        print(f'{n}: {itemName},\n     Price: {itemPrice},\n     Location: {itemLocation},\n     '
              f'Frame size: {itemFrameSize},\n     Condition: {itemCondition}')
        item_to_json = {
            'Name': itemName,
            'Price': itemPrice,
            'Location': itemLocation,
            'Frame Size': itemFrameSize,
            'Condition': itemCondition
        }
        to_json.append(item_to_json)
    params['page'] += 1

df = pd.DataFrame({
    'Name': itemsName,
    'Price': itemsPrice,
    'Location': itemsLocation,
    'Frame Size': itemsFrameSize,
    'Condition': itemsCondition
})
df.to_csv('bikes.csv', index=False)

with open('bikes.json', 'w') as f:
    f.write(json.dumps(to_json, indent=4))
