import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'
HEADER = [
    'product_page_url',
    'universal_ product_code (upc)',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url',
]

res = requests.get(url)
print(res)


def add_book(book_url, category):
    res = requests.get(book_url)
    book = {}
    if res.ok:
        html = BeautifulSoup(
            res.text, 'html.parser')
        book['product_page_url'] = book_url
        book['title'] = html.find('head').find(
            'title').text.split('|')[0].strip()
        book['product_description'] = html.find(
            'div', {'id': 'product_description'}).find_next('p').text
        book['category'] = category
        product_description = html.find('h2', text='Product Information').find_next(
            'table', {'class': 'table table-striped'}).findAll('tr')
        for desc in product_description:
            if desc.find('th').text == 'UPC':
                book['universal_ product_code (upc)'] = desc.find('td').text
            elif desc.find('th').text == 'Price (incl. tax)':
                book['price_including_tax'] = desc.find('td').text
            elif desc.find('th').text == 'Price (excl. tax)':
                book['price_excluding_tax'] = desc.find('td').text
            elif desc.find('th').text == 'Availability':
                book['number_available'] = desc.find('td').text
            elif desc.find('th').text == 'Number of reviews':
                book['review_rating'] = desc.find('td').text

    return book


def create_categories(res):
    categories = {}
    cats = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'class': 'side_categories'}).find('ul', {'class': ''}).findAll('li')
    for cat in cats:
        name = cat.find('a').text.replace('\n', '').replace(' ', '')
        link = cat.find('a')['href']
        categories[name] = link

    return categories


if res.ok:
    # categories = create_categories(res)
    # print(categories)
    category = 'test'
    book_urls = [
        'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', ]
    for book_url in book_urls:
        res = add_book(book_url, category)
        print(res)
else:
    print('error')
