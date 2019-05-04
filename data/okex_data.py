from websocket import create_connection
import gzip
import zlib
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
    global last_price
    last_price = 1
    # LOCK.acquire()
    global buy_1_price, sell_1_price
    data = result['data']
    price_json = data[0]
    price = price_json['last']
    buy_1_price = float(price)
    sell_1_price = float(price)
    # buy_1_list.insert(0, buy_1_price)
    # sell_1_list.insert(0, sell_1_price)
    # if len(buy_1_list) > LIST_SIZE:
    #     buy_1_list.pop()
    # if len(sell_1_list) > LIST_SIZE:
    #     sell_1_list.pop()
    # print('OKEX --- ', util.get_print_datetime(), sell_1_price, buy_1_price)


def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return bytes.decode(inflated)


def open_thread():
    global last_price, retry_count
    try:
        ticker = util.get_okex_symbol(const.BTC)
        if ticker == '':
            print('can not find contract id')
            return
        ws = create_connection("wss://real.okex.com:10442/ws/v3")
        trade_str = {"op": "subscribe", "args": ["index/ticker:" + ticker]}
        ws.send(json.dumps(trade_str))
        while ws.connected:
            retry_count = 0
            compress_data = ws.recv()
            result = inflate(compress_data)
            if 'table' in result:
                result = json.loads(result)
                last_price = 1
                handle_data(result)
        ws.close()
        print('okex thread stop')
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


# variable.CURRENT_ID = const.EOS_REVERSE
# open_thread()