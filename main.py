import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


json_path = 'json.json'

dictionary = {
    'https://www.datacenterdynamics.com/en/news/': {
        'a_xpath': "//a[@class='block-link headline-link']",
        'title': "//h1[@class='article-heading']",
        'body': "//div[@class='block-text']",
        'teaser': "//div[@class='article-sub-heading']/p",
        'short_name': "datacenterdynamics"
    },
    'https://www.datacenterfrontier.com/': {
        'a_xpath': "//a[@class='title-wrapper']",
        'title': "//h1[@class='title-text']",
        'body': "//p",
        'teaser': "//div[@class='teaser-text']",
        'short_name': "datacenterfrontier"
    },
    'https://www.datacenterknowledge.com/': {
        'a_xpath': "//div[@class='title']/a",
        'title': "//h1[@itemprop='headline']",
        'body': "//div[@itemprop='articleBody']",
        'teaser': "//div[@class='field field-name-field-penton-content-summary field-type-text-long field-label-hidden']",
        'short_name': "datacenterknowledge"
    },
    'https://datacentre.solutions/news': {
        'a_xpath': "//h5[a[@class='text-dark']]/a",
        'title': "//div[@class='postSection']/h1",
        'body': "//div[@class='post-details']//p",
        'teaser': "//div[@class='postSection']/h2",
        'short_name': "datacentre.solutions"
    },
    'https://datacentrereview.com/': {
        'a_xpath': "//h5[@class='sc_blogger_item_title entry-title']/a",
        'title': "//h1",
        'body': "//div[@class='elementor-widget-container']/p",
        'teaser': None,
        'short_name': "datacentrereview"
    },
    'https://dcnnmagazine.com/': {
        'a_xpath': "//h3[@class='jeg_post_title']/a",
        'title': "//h1",
        'body': "//div[@class='content-inner  jeg_link_underline']//p",
        'teaser': None,
        'short_name': "dcnnmagazine"
    },
    'https://datacenternews.asia/': {
        'a_xpath': "//a[@class='flex flex-col md:flex-row gap-4 hover:opacity-75']",
        'title': "//h1",
        'body': "//div[@class='flex flex-col lg:flex-row gap-x-10 gap-y-5']/div[2]",
        'teaser': None,
        'short_name': "datacenternews"
    },
    'https://www.capacitymedia.com/news': {
        'a_xpath': "//div[@class='PromoB-title']/a",
        'title': "//h1",
        'body': "//div[@class='RichTextArticleBody-body RichTextBody']/p",
        'teaser': "//h2[@class='ArticlePage-subHeadline']",
        'short_name': "capacitymedia"
    }
}

all_news_list = []
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

for link, details in dictionary.items():
    driver.get(link)
    time.sleep(1)
    a_xpath = details['a_xpath']
    news_links = driver.find_elements(By.XPATH, a_xpath)
    for li in news_links[:1]:
        all_news_list.append(li.get_attribute('href'))
driver.close()

print(all_news_list)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
for link in all_news_list:
    driver.get(link)
    time.sleep(0.5)
    title = teaser = body = ''
    for _, details in dictionary.items():
        if details['short_name'] in link:
            title = driver.find_element(By.XPATH, details['title']).text
            teaser = driver.find_element(By.XPATH, details['teaser']).text
            body_elements = driver.find_elements(By.XPATH, details['body'])
            for text in body_elements:
                body += text.text.replace('\n', ' ')
            break

    print(link, title, teaser, body)

# print(all_news_list)
