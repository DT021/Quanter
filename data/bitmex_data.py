from websocket import create_connection
import json
import copy
import threading
import variable, util, traceback
import wechat_notifier as wechat

LOCK = threading.Lock()

last_price = 0
order_list = {}
has_receive_partial = False
is_alive = True

buy_1_list = []
sell_1_list = []
LIST_SIZE = 5


def get_quote_1():
    LOCK.acquire()
    order_copy = copy.deepcopy(order_list)
    LOCK.release()
    sell_1 = -100
    buy_1 = -100
    for _id in order_copy:
        order = order_copy[_id]
        price = order['price']
        if order['side'] == 'Sell':
            if sell_1 == -100:
                sell_1 = price
            else:
                sell_1 = min(sell_1, price)
        else:
            if buy_1 == -100:
                buy_1 = price
            else:
                buy_1 = max(buy_1, price)
    return sell_1, buy_1


def get_compare_quote_1():
    sell_1, buy_1 = get_quote_1()
    return sell_1 + variable.PRICE_SHIFT, buy_1 + variable.PRICE_SHIFT


def get_amount_1():
    LOCK.acquire()
    order_copy = copy.deepcopy(order_list)
    LOCK.release()
    sell_1 = -1
    buy_1 = -1
    sell_1_amount = -1
    buy_1_amount = -1
    for _id in order_copy:
        order = order_copy[_id]
        price = order['price']
        amount = order['size']
        if order['side'] == 'Sell':
            if sell_1 == -1:
                sell_1_amount = amount
                sell_1 = price
            else:
                if sell_1 >= price:
                    sell_1_amount = amount
                    sell_1 = price
        else:
            if buy_1 == -1:
                buy_1 = price
                buy_1_amount = amount
            else:
                if price >= buy_1:
                    buy_1 = price
                    buy_1_amount = amount
    return sell_1_amount, buy_1_amount


def update_list():
    global buy_1_list, sell_1_list
    sell_1, buy_1 = get_quote_1()
    buy_1_list.insert(0, buy_1)
    sell_1_list.insert(0, sell_1)
    if len(buy_1_list) > LIST_SIZE:
        buy_1_list.pop()
    if len(sell_1_list) > LIST_SIZE:
        sell_1_list.pop()


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


def insert_order(result):
    LOCK.acquire()
    global order_list
    data = result['data']
    for d in data:
        _id = d['id']
        order_list[_id] = d
    LOCK.release()
    update_list()


def delete_order(result):
    LOCK.acquire()
    global order_list
    data = result['data']
    for d in data:
        _id = d['id']
        order_list.pop(_id)
    LOCK.release()
    update_list()


def update_order(result):
    LOCK.acquire()
    global order_list
    data = result['data']
    for d in data:
        _id = d['id']
        target = order_list[_id]
        target['size'] = d['size']
    LOCK.release()


def handle_trade_data(result):
    global last_price
    data = result['data']
    length = len(data)
    target = data[length - 1]
    last_price = target['price']


def handle_order_data(result):
    global has_receive_partial
    action = result['action']
    if action == 'partial':
        insert_order(result)
        has_receive_partial = True
    elif action == 'insert':
        if has_receive_partial:
            insert_order(result)
    elif action == 'delete':
        if has_receive_partial:
            delete_order(result)
    elif action == 'update':
        if has_receive_partial:
            update_order(result)


def open_bitmex():
    global last_price
    try:
        ticker = util.get_bm_ticker(variable.CURRENT_ID)
        if ticker == '':
            print('can not find contract id')
            return
        ws = create_connection('wss://www.bitmex.com/realtime?subscribe=orderBookL2_25:'+ticker+',trade:'+ticker)
        while ws.connected and is_alive:
            result = ws.recv()
            result = json.loads(result)
            if 'data' not in result:
                continue
            table = result['table']
            if table == 'trade':
                handle_trade_data(result)
            elif table == 'orderBookL2_25':
                handle_order_data(result)
        ws.close()
        print('bitmex thread stop')
        last_price = -1
    except Exception as e:
        traceback.print_exc()
        last_price = -1
        wechat.send_message(str(e))


def start():
    threading.Thread(target=open_bitmex).start()


# open_bitmex()