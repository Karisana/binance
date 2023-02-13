from binance import Client
import time


class BinanceCheckCurrencies:
    apikey = 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
    secret = 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j'
    client = Client(apikey, secret)
    currencies = 'XRPUSDT'
    time_check = '60'
    start_str = time_check + ' minutes ago UTC'
    price_list = []
    res_price_list = []
    max_price_index = None

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
                print('max_price_index ->', self.max_price_index,
                      'Была максимальная цена за час', max(self.res_price_list))

                return print(f'Была максимальная цена за час {max(self.res_price_list)}. '
                             f'Минимальная цена за час {min(self.res_price_list)}')

                # return print(f'За час цена упала больше 1%. Было {max(self.res_price_list)}')


sheck = BinanceCheckCurrencies()

while True:
    try:
        sheck.main()
        # print(sheck.price_list)
        # print(sheck.res_price_list)
        time.sleep(3600)
    except Exception as err:
        print(err)

# print(sheck.price_list)
# print(sheck.res_price_list)
