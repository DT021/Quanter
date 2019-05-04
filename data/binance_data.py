from binance.websockets import BinanceSocketManager
from binance.client import Client
import threading
import copy
import variable, util, const

MAX_TRY_COUNT = 5
retry_count = 0

last_price = 0
LOCK = threading.Lock()

buy_1_price = 0
sell_1_price = 0

buy_1_list = []
sell_1_list = []
LIST_SIZE = 5


def get_last_price():
    return last_price


def get_quote_1():
    return sell_1_price, buy_1_price


def get_compare_quote_1():
    return sell_1_price + variable.PRICE_SHIFT, buy_1_price + variable.PRICE_SHIFT


def get_sell_1_list():
    # LOCK.acquire()
    # list_copy = copy.deepcopy(sell_1_list)
    # LOCK.release()
    # return list_copy
    return []


def get_buy_1_list():
    # LOCK.acquire()
    # list_copy = copy.deepcopy(buy_1_list)
    # LOCK.release()
    # return list_copy
    return []


def process_message(msg):
    global last_price
    if msg['e'] == 'error':
        print('error!!!!!!', msg)
        last_price = 0
        start()
    else:
        last_price = 1
        # LOCK.acquire()
        global buy_1_price, sell_1_price
        price = msg['p']
        buy_1_price = float(price)
        sell_1_price = float(price)
        # buy_1_list.insert(0, buy_1_price)
        # sell_1_list.insert(0, sell_1_price)
        # if len(buy_1_list) > LIST_SIZE:
        #     buy_1_list.pop()
        # if len(sell_1_list) > LIST_SIZE:
        #     sell_1_list.pop()
        # print('BINANCE --- ', util.get_print_datetime(), sell_1_price, buy_1_price)
        # LOCK.release()


def open_thread():
    ticker = util.get_huobi_binance_symbol(variable.CURRENT_ID)
    if ticker == '':
        print('can not find contract id')
        return
    client = Client('Zdmpb20LvVlpF1HxJBhj4JXotjNtX0hT8qKOCr29eCwtuKopeoJG3Xb3XkPo7Lqg',
                    'LVvXZ6wvW2hxkvQhTFBI5jII5The3SSvinK3sNK0pc05UprnW6E9pklOWHQuX2XP')
    bm = BinanceSocketManager(client)
    bm.start_aggtrade_socket(ticker, process_message)
    bm.start()


def start():
    threading.Thread(target=open_thread).start()


# variable.CURRENT_ID = const.EOS
# open_thread()