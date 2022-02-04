# coding: utf8

import requests
from bs4 import BeautifulSoup
import math
import csv

url = 'https://books.toscrape.com/'
HEADER = [
    'product_page_url',
    'title',
    'universal_ product_code (upc)',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'review_rating',
    'product_description',
    'category',
    'image_url',
]
CSV_PATH = "C:\\Users\\USER\\Documents\\OCR\\Projet\\P2_couignoux_julien\\"

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
        print(book['title'])
        product_information = html.find('h2', text='Product Information').find_next(
            'table', {'class': 'table table-striped'}).findAll('tr')
        for desc in product_information:
            if desc.find('th').text == 'UPC':
                book['universal_ product_code (upc)'] = desc.find('td').text
            elif desc.find('th').text == 'Price (incl. tax)':
                book['price_including_tax'] = desc.find(
                    'td').text
            elif desc.find('th').text == 'Price (excl. tax)':
                book['price_excluding_tax'] = desc.find('td').text
            elif desc.find('th').text == 'Availability':
                book['number_available'] = desc.find('td').text
            elif desc.find('th').text == 'Number of reviews':
                book['review_rating'] = desc.find('td').text
        if html.find(
                'div', {'id': 'product_description'}):
            book['product_description'] = html.find(
                'div', {'id': 'product_description'}).find_next('p').text
        book['category'] = category[0]
        book['image_url'] = str(url) + html.find(
            'div', {'id': 'product_gallery'}).find('img')['src'].replace('../../', '')

    return book


def create_links_list(category):
    links_list = []
    index = requests.get(url + category[1])
    if index.ok:
        total_number = BeautifulSoup(index.text, 'html.parser').find(
            'form', {'class': 'form-horizontal'}).find('strong').text
        if int(total_number) >= 20:
            books_number = BeautifulSoup(index.text, 'html.parser').find(
                'form', {'class': 'form-horizontal'}).find('strong').find_next('strong').find_next('strong').text
            pages_number = math.ceil(int(total_number) / int(books_number))
        else:
            pages_number = 1
        print(pages_number)
        if pages_number == 1:
            for article in BeautifulSoup(index.text, 'html.parser').findAll('article', {'class': 'product_pod'}):
                link = str(url) + 'catalogue/' + article.find(
                    'div', {'class': 'image_container'}).find('a')['href'].replace('../../../', '')
                links_list.append(link)
        else:
            for i in range(pages_number):
                page = requests.get(
                    url + category[1].replace('index', 'page-'+str(i + 1)))
                for article in BeautifulSoup(page.text, 'html.parser').findAll('article', {'class': 'product_pod'}):
                    link = str(url) + 'catalogue/' + article.find(
                        'div', {'class': 'image_container'}).find('a')['href'].replace('../../../', '')
                    links_list.append(link)
    if len(links_list) != int(total_number):
        print('liste lien différent nombre livres')

    return links_list


def create_categories(res):
    categories = {}
    cats = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'class': 'side_categories'}).find('ul', {'class': ''}).findAll('li')
    for cat in cats:
        name = cat.find('a').text.replace('\n', '').replace(' ', '')
        link = cat.find('a')['href']
        categories[name] = link

    return categories


def create_csv(books):
    with open(CSV_PATH + str(category[0]) + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADER)
        writer.writeheader()
        for book in books:
            print(book)
            writer.writerow(book)

    return CSV_PATH + str(category[0]) + '.csv'


if res.ok:
    categories = create_categories(res)
    # categories = {'Travel': 'catalogue/category/books/travel_2/index.html', }
    books = {}
    for category in categories.items():
        books[category[0]] = []
        book_url_list = create_links_list(category)
        for book_url in book_url_list:
            book_details = add_book(book_url, category)
            books[category[0]].append(book_details)
        path_csv = create_csv(books[category[0]])
else:
    print('error')

# print(books)
