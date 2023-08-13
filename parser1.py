import json
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup


json_file = open('json1.json', 'w+')


url = 'https://www.darkreading.com/latest/news'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

today = datetime.today().date()

one_article = soup.find('div', class_='topic-content-article')  #контейнер с новостью
article_date = one_article.find('div', class_='arcile-date').text
test_date = datetime.strptime("2023-08-11", "%Y-%m-%d").date()
news_count = 0

# print(test_date)

while True:
  parsed_date = datetime.strptime(article_date, '%B %d, %Y').date()  #дата в контейнере, приведенная к нужному формату
  if parsed_date == test_date:
    news_title = one_article.find(class_='article-title').text  #заголовок новости
    today_link = one_article.find('a').get('href')  #ссылка на саму новость
    news_response = requests.get(today_link)  #реквест полученной ссылки
    news_soup = BeautifulSoup(news_response.text, 'lxml') #суп полученной ссылки
    paragraph = news_soup.find_all('p')
    p_list = []
    for i in paragraph:
        p_list.append(i.text)
    news_body = ". ".join(p_list) #полный текст статьи

    data = {'date': article_date,  #запись в словарь даты
            'link': today_link, #запись в словарь ссылки
            'title': news_title,  #запись в словарь заголовка
            'body': news_body}  #запись в словарь текста статьи

    json.dump(data, json_file)

    news_count += 1

    one_article = one_article.find_next('div', class_='topic-content-article')
    article_date = one_article.find('div', class_='arcile-date').text

  else:
    json_file.close
    print(f'За сегодняшний день на сйте: {url} найдено {news_count} новостей')
    break
