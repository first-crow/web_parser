import time
import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
}
response = requests.get('https://www.securitylab.ru/news/')
soup = BeautifulSoup(response.text, 'lxml')
find_index_lastpage = soup.find(class_="page-picker").text.strip().split()
last_page = int(find_index_lastpage[1])

parser = []
# for page in range(1,last_page-1):
for page in range(1, 4):
    link = f'https://www.securitylab.ru/news/page1_{page}.php'
    response = requests.get(url=link, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    all_url_news = soup.find_all("a", class_="article-card inline-card")
    all_url_list = ('https://www.securitylab.ru' + url.get('href') for url in all_url_news)
    print(f'Page: {page}')
    for url in all_url_list:
        about_news = requests.get(url)
        soup = BeautifulSoup(about_news.text, 'lxml')
        print(f'Сollecting data from the news: {url}')
        print('*' * 75)
        time.sleep(2)
        for item in url:
            url_new = url
            author = soup.find('div', itemprop="author").text
            data = soup.find('time').text.replace(',', '').replace('/', '').replace('  ', ' - ').strip()
            title = soup.find('h1', class_="page-title pt-3 px-3").text
            descriptions = soup.find('div', class_="articl-text").find_all('p')
            for description in descriptions:
                description = description.text.strip().replace('  ', ' ')

        parser.append({
            "url_news": url_new,
            "author": author,
            "data": data,
            "title": title,
            "description": description
        })

with open('www_securitylab_ru.json', "a", encoding="utf-8") as file:
    json.dump(parser, file, indent=4, ensure_ascii=False)
    print('Data collection completed')
