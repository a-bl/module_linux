import requests
from bs4 import BeautifulSoup

url = 'https://bikefair.org/listings?location%5B0%5D=51.33684119999999&location%5B1%5D=5.9482681&height' \
      '=&delivery_distance=10&country_code=NL&sort%5Bkey%5D=best_match&sort%5Bdirection%5D=asc '
params = {'page': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 1

while params['page'] <= pages:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='px-3 w-full sm:w-1/2 lg:w-1/2 xl:w-1/3 mb-6')
    # print(items)

    for n, i in enumerate(items, start=n+1):
        itemName = i.find('h3', class_='font-bold line-clamp-2 h-12 px-2').text.split(",")[0]
        itemPrice = i.find('div', class_='font-bold text-base').text
        # print(f"{n}: {itemPrice}")
        print(f'{n}:  {itemPrice} for {itemName}')
