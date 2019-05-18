from websocket import create_connection
import gzip
import time
import json
import traceback
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


def handle_data(result):
    global buy_1_price, sell_1_price
    tick = result['tick']
    data = tick['data']
    target = data[len(data) - 1]
    # print(len(data), target)
    buy_1_price = target['price']
    sell_1_price = target['price']
    # print(buy_1_price, sell_1_price)


def open_thread():
    global last_price, retry_count
    try:
        ticker = util.get_huobi_binance_symbol(variable.CURRENT_ID)
        if ticker == '':
            print('can not find contract id')
            return
        ws = create_connection("wss://api.huobi.pro/ws")
        trade_str = {"sub": "market."+ticker+".trade.detail"}
        ws.send(json.dumps(trade_str))
        count = 0
        while ws.connected:
            retry_count = 0
            compress_data = ws.recv()
            result = gzip.decompress(compress_data).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":' + ts + '}'
                ws.send(pong)
                # print('huobi send pong:', count)
                count = 0
            elif 'tick' in result:
                count += 1
                result = json.loads(result)
                last_price = 1
                handle_data(result)
        ws.close()
        print('huobi thread stop')
        last_price = 0
        if retry_count <= MAX_TRY_COUNT:
            retry_count += 1
            open_thread()
        else:
            last_price = -1
    except Exception as e:
        traceback.print_exc()
        last_price = 0
        if retry_count <= MAX_TRY_COUNT:
            retry_count += 1
            open_thread()
        else:
            last_price = -1


def start():
    threading.Thread(target=open_thread).start()


# variable.CURRENT_ID = const.HT
# open_thread()