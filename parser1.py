import json
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup

response = requests.get('https://beta.darkreading.com/edge')
soup = BeautifulSoup(response.text, 'lxml')

today = datetime.today().date()
site_date = soup.find('div', class_='spotlight-right ml-3')
parsed_data = datetime.strptime(site_date.text, '%b %d, %Y').date()


news_title = soup.find('div', class_='spotlight-left').find('a').text
today_link = soup.find('div', class_='spotlight-left').find('a').get('href')

news_response = requests.get(today_link)
soup = BeautifulSoup(news_response.text, 'lxml')

paragraph = soup.find_all('p')
p_list = []
for i in paragraph:
    p_list.append(i.text)
news_body = ". ".join(p_list)
# print(news_body)


data = {'date': site_date.text,
        'link': today_link,
        'title': news_title,
        'body': news_body}

with open('json1.json', 'w') as file:
    json.dump(data, file)



# print(paragraph.text)
# print(site_date)
# if parsed_data == today:
#     print(url)
# else:
#     print(site_date)