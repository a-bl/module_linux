import requests
from bs4 import BeautifulSoup

# url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
#
# for n, i in enumerate(items, start=1):
#     itemName = i.find('h4', class_='card-title').text.strip()
#     itemPrice = i.find('h5').text
#     print(f'{n}:  {itemPrice} for {itemName}')
#
# # scraping with pagination
#
# pages = soup.find('ul', class_='pagination')
# urls = []
# links = pages.find_all('a', class_='page-link')
#
# for link in links:
#     pageNum = int(link.text) if link.text.isdigit() else None
#     if pageNum != None:
#         hrefval = link.get('href')
#         urls.append(hrefval)
#
# for slug in urls:
#     newUrl = url.replace('?page=1', slug)
#     response = requests.get(newUrl)
#     soup = BeautifulSoup(response.text, 'lxml')
#     items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
#     for n, i in enumerate(items, start=n+1):
#         itemName = i.find('h4', class_='card-title').text.strip()
#         itemPrice = i.find('h5').text
#         print(f'{n}:  {itemPrice} за {itemName}')

url = 'https://scrapingclub.com/exercise/list_basic/'
params = {'page': 1}
# set a number greater than the number of the first page to start the cycle
pages = 2
n = 1

while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

    for n, i in enumerate(items, start=n+1):
        itemName = i.find('h4', class_='card-title').text.strip()
        itemPrice = i.find('h5').text
        print(f'{n}:  {itemPrice} for {itemName}')

    # [-2] the penultimate value because the last is "Next"
    last_page_num = int(soup.find_all('a', class_='page-link')[-2].text)
    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1
