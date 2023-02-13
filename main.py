from binance import Client
import time


class BinanceCheckCurrencies:
    price_list = []
    res_price_list = []
    max_price_index = None

    def __init__(self, currencies, time_check):
        self.apikey = 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
        self.secret = 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j'
        self.client = Client(self.apikey, self.secret)
        self.currencies = currencies
        self.time_check = time_check
        self.start_str = self.time_check + ' minutes ago UTC'

    @staticmethod
    def search_difference(max_num, min_num, percent_difference):
        difference = max_num / 100 * percent_difference
        if max_num - min_num >= difference:
            return True

    def main(self):
        agg_trades = self.client.aggregate_trade_iter(symbol=self.currencies, start_str=self.start_str)

        for trade in agg_trades:
            if float(trade['p']) not in self.price_list:
                self.price_list.append(float(trade['p']))

            self.max_price_index = self.price_list.index(max(self.price_list))

            self.res_price_list = self.price_list
            del self.res_price_list[0:self.max_price_index]
            res = self.search_difference(max(self.res_price_list), min(self.res_price_list), 1)
            if res:
                return print(f'За час цена упала больше 1%. '
                             f'Было - {max(self.res_price_list)}, '
                             f'стало - {min(self.res_price_list)}')


while True:

    check_price = BinanceCheckCurrencies('XRPUSDT', '60')
    check_price.main()
    # print(check_price.price_list)
    # print(check_price.res_price_list)
    time.sleep(100)

