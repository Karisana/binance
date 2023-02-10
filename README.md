# binance
Цель: отслеживать в реальном времени цену XPT/USDT на бирже binance.
Так как ключа для апи не было (не было возможности ждать подтвреждения 3 суток) сделала через ссылку их, без ключей и пакета binance.
Если цена падает на 1% от максимальной цены за час - идет предупреждение.

Сейчас каждый час файл и данные обнуляются.
В дальнейшем нужно будет придумать более удобным файл и быстрый. 

Модули: 
import requests
import json
from datetime import datetime
import time
import csv
import requests
import json
from datetime import datetime
import time
import csv
