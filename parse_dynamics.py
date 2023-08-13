import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


data_new = []


# Вспомогательная функция для чтения данных из JSON-файла
def read_data_from_json():
    data = []
    try:
        with open("database_dynamics.json", 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
    return data


# Функция для добавления данных в JSON-файл
def write_data_to_json(data_d):
    with open("database_dynamics.json", "w", encoding="utf-8") as json_file:
        json.dump(data_d, json_file, ensure_ascii=False)


# функция добавления ссылок
def json_sort():
    links = []
    try:
        with open("database_dynamics.json", 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            if data:
                with open("database_dynamics.json", "r", encoding="utf-8") as db_json:
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


# Создаем начальную работу с сайтом
def begin():
    try:
        driver.execute_script("window.stop();")
        # Убираем окно Privacy и 'got it'
        driver.find_element(By.XPATH, "/html/body/div[7]/div[1]/div/div[3]/a[1]/div/div").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div/a").click()
    except NoSuchElementException:
        pass
    # Переходим ко всем новостям сайта
    driver.find_element(By.XPATH, "/html/body/main/div/div/section/section[2]/div/div[1]/h2/a").click()


# для парсинга новостей на странице
def parse_news(data_news):
    # Преобразуем множество в список
    js_data = read_data_from_json()
    js_info_href = json_sort()
    spook_json_file = []
    # Вывод списка данных
    for item in range(len(data_news)):
        if data_news[item] not in js_info_href:
            driver.get(f'{data_news[item]}')
            print(data_news[item])
            time.sleep(1)
            body_news = ''
            datatime_news_elem = driver.find_element(By.CLASS_NAME, "article-intro__date")
            date_news = datatime_news_elem.get_attribute("datetime")
            title_news_elem = driver.find_element(By.CLASS_NAME, "article-heading")
            title_news = title_news_elem.text
            body_news_elem = driver.find_elements(By.CLASS_NAME, "block-text")
            for text in body_news_elem:
                body_news += text.text

            news_data = {
                "link": data_news[item],
                "date": date_news,
                "title": title_news,
                "body": body_news
            }
            spook_json_file.append(news_data)
        else:
            print(f'Ссылка {data_news[item]} уже существует')
            continue

    all_data = merge_data(js_data, spook_json_file)
    write_data_to_json(all_data)
    driver.back()


# для переходов между сайтов
def web_paginator():
    links = driver.find_elements(By.CSS_SELECTOR, 'a.block-link.headline-link')
    for link in links:
        href = link.get_attribute('href')
        if href:
            data_new.append(href)  # Добавляем ссылку в множество
    # print(data_new)
    data_pars_new = data_new
    # driver.find_element(By.XPATH, "/html/body/main/div/div/section/main/section/div/div[3]/a").click()
    parse_news(data_pars_new)


if __name__ == '__main__':
    file = open("database_dynamics.json", "a")
    file.close()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.datacenterdynamics.com/en/')
    driver.execute_script("window.stop();")
    begin()
    web_paginator()
    driver.quit()