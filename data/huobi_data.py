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


def get_quote_1():
    return sell_1_price, buy_1_price


def get_compare_quote_1():
    return sell_1_price + variable.PRICE_SHIFT, buy_1_price + variable.PRICE_SHIFT


def get_sell_1_list():
    LOCK.acquire()
    list_copy = copy.deepcopy(sell_1_list)
    LOCK.release()
    return list_copy


def get_buy_1_list():
    LOCK.acquire()
    list_copy = copy.deepcopy(buy_1_list)
    LOCK.release()
    return list_copy


def handle_data(result):
    LOCK.acquire()
    global buy_1_price, sell_1_price
    tick = result['tick']
    bids = tick['bids']
    asks = tick['asks']
    buy_1 = bids[0]
    sell_1 = asks[0]
    buy_1_price = buy_1[0]
    sell_1_price = sell_1[0]
    buy_1_list.insert(0, buy_1_price)
    sell_1_list.insert(0, sell_1_price)
    if len(buy_1_list) > LIST_SIZE:
        buy_1_list.pop()
    if len(sell_1_list) > LIST_SIZE:
        sell_1_list.pop()
    LOCK.release()


def open_thread():
    global last_price, retry_count
    try:
        ticker = util.get_huobi_symbol(variable.CURRENT_ID)
        if ticker == '':
            print('can not find contract id')
            return
        ws = create_connection("wss://api.huobi.pro/ws")
        trade_str = {"sub": "market."+ticker+".depth.step0"}
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
                print('huobi send pong:', count)
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


# open_thread()