import json
import time

from binance import Client
import requests
import pandas as pd

from datetime import datetime

# Коды не привязаны к личному кабинету в binance. Взяты из документации с апи.
# При работе со своим личным кабинетом, нужно вставить свои, но лучше их "спрятать" через denv.
# при данном коде данные берутся из апи напрямую, поэтому они по сути тут и не нужны.
# Только для теста следующих операция оставляю их тут.

apikey = 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
secret = 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j'
client = Client(apikey, secret)


# основной код

def get_data():
    """
    Обработка данных нужной нам валюты напрямую через ссылку апи.
    Возвращает значение список с float(ценой) и дату (дата для проверки кода)
    """

    link_api = requests.get('https://api3.binance.com/api/v3/ticker/price')
    price = link_api.json()[306]
    times = datetime.now().strftime("%H:%M:%S")
    data = [float(price['price']), times]
    return data


price_data = []


def write_data():
    """
    Запись полученных данных в список и перевод в json
    Стоит таймер, чтобы брать каждую секунду данные. Стоит 0.5 так как пинг от сервера еще ~ 0.5 сек
    Каждый раз идет дозапись в список price_data
    Если список стал слишком большой, то очищаю значения от 0 до 7200
    """
    if len(price_data) >= 10800:
        del price_data[0:7200]

    for _ in range(10):
        time.sleep(0.5)
        price_data.append(get_data())
    res_json = json.dumps(price_data)

    return res_json


def get_max_min(some_data):
    """
    Поиск максимальной/минимальной цены и разницы между ними
    """

    max_price = max(some_data[0])
    min_price = min(some_data[0])
    difference = max_price / 100 * 1

    return max_price, min_price, difference


def get_max():
    """
    Читаем json через pandas. Так как он позволяет лучше работать с огромным потоком данным.
    И удобно проверять только последние 3600 записей (столько записей будет в течение часа)
    - для отслеживания цены в течение часа.
    """

    stops = pd.read_json(write_data())
    if len(price_data) > 3600:
        last_line = stops.tail(3600)
        print('Проверяю последние строчки:\n', last_line)
        max_price = get_max_min(last_line)[0]
        min_price = get_max_min(last_line)[1]
        difference = get_max_min(last_line)[2]
        print('                         max_price', max_price)  # максимальное значение в столбце
        print('                         min_price', min_price)  # максимальное значение в столбце
        print(difference)
        if max_price - min_price >= difference:
            print('Внимание! Цена стала больше 1%')
    else:
        print('Проверка начальных')
        max_price = get_max_min(stops)[0]
        min_price = get_max_min(stops)[1]
        difference = get_max_min(stops)[2]
        print('                         max_price', max_price)  # максимальное значение в столбце
        print('                         min_price', min_price)  # максимальное значение в столбце
        print(difference)
        if max_price - min_price >= difference:
            print('Внимание! Цена стала больше 1%')


def main():
    get_max()


while True:
    if __name__ in '__main__':
        main()
