import requests
import json
from datetime import datetime
import time
import csv


class Currency:
    link_api = requests.get('https://api3.binance.com/api/v3/ticker/price')
    MAX_PRICE = 0

    def __init__(self):
        self.difference = 0
        self.now_price = 0
        self.now_time = 0

    def get_data(self):
        time.sleep(1)
        price_in_api = json.loads(self.link_api.text)
        price = float(price_in_api[306]["price"])
        times = datetime.now().strftime("%H:%M:%S")
        self.now_price = price
        self.now_time = times
        return times, price

    def write_data(self):
        with open('data.txt', 'a') as out:
            out.write(f'{self.get_data()}\n')

    def check_now_price(self):
        res = self.MAX_PRICE - self.now_price
        res = round(res, 5)
        if self.difference <= res:
            print(f'Упало больше, чем на 1%. Сейчас цена {self.now_price} {self.difference}. '
                  f'Была цена {self.MAX_PRICE}')
            # максимум должен обновляться в течение часа.

    def check_max(self):

        with open('data.txt', 'r') as out:
            data = csv.reader(out)
            max_data_info = max(data, key=lambda x: x[1])
            max_prise_time = max_data_info[0].replace('(', '')
            max_prise = float(max_data_info[1].replace(' ', '').replace(')', ''))
            if self.MAX_PRICE < max_prise:
                self.MAX_PRICE = max_prise
                self.difference = float('{:f}'.format(self.MAX_PRICE / 100 * 1))
                print(f'    !!!Изменилось значение у {self.MAX_PRICE}!!!     ')

    def main(self):
        print()
        for _ in range(3600):
            self.get_data()
            self.write_data()
            self.check_max()
            self.check_now_price()

        print('End')


a = Currency()
a.main()

# list = [0, 2,2 ,45,6,6,7 ,7,2, 5,2, 5]
# a = list[-3:]
# print(a)
