import json
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common import StaleElementReferenceException

address = []


# Вспомогательная функция для чтения данных из JSON-файла
def read_data_from_json():
    data = []
    try:
        with open("database_frontier.json", 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
    return data


# Функция для добавления данных в JSON-файл
def write_data_to_json(data):
    with open("database_frontier.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)


# функция добавления ссылок
def json_sort():
    links = []
    try:
        with open("database_frontier.json", 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            if data:
                with open("database_frontier.json", "r", encoding="utf-8") as db_json:
                    data_json = json.load(db_json)

                for obj in data_json:
                    links.append(obj["link"])
                return links
            else:
                return links
    except json.JSONDecodeError as e:
        print(f"Невозможно загрузить данные из файла: {e}")
        return links


# Вспомогательная функция для слияния старых и новых данных
def merge_data(old_data, new_data):
    all_data = old_data + new_data
    return all_data


# Функция для парсинга новостей
def parse_news(data_news):
    js_data = read_data_from_json()
    js_info_href = json_sort()
    spook_json_file = []

    for item in range(len(data_news)):
        if data_news[item] in js_info_href:
            print(f'Ссылка {data_news[item]} уже существует')
            continue
        else:
            try:
                time.sleep(1)
                driver.get(f'{data_news[item]}')

                body_news = ''
                datatime_news_elem = driver.find_element(By.CLASS_NAME, "date")
                date_news = datatime_news_elem.text

                title_news_elem = driver.find_element(By.XPATH, "//h1[@class='title-text']")
                title_news = title_news_elem.text

                body_news_elem = driver.find_elements(By.XPATH, "//p")
                for text in body_news_elem:
                    body_news += text.text

                news_data = {
                    "link": data_news[item],
                    "date": date_news,
                    "title": title_news,
                    "body": body_news
                }

                spook_json_file.append(news_data)

            except StaleElementReferenceException:
                break

            except NoSuchElementException:
                break

    all_data = merge_data(js_data, spook_json_file)
    write_data_to_json(all_data)
    driver.back()


def begin():
    time.sleep(3)
    link = driver.find_elements(By.CSS_SELECTOR, 'a.title-wrapper')
    for URI in link:
        href = URI.get_attribute('href')
        if href:
            address.append(href)

    parse_news(address)


if __name__ == '__main__':
    file = open("database_frontier.json", "a")
    file.close()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.datacenterfrontier.com/')
    begin()
    driver.quit()
