from api.base_api import AbsApi
import variable, time, const
import hashlib
import json
import requests
import urllib.parse
from bean import Position
import util
import threading
import api.user_position as user_position


BASE_URL = 'https://www.bfx.nu'
ORDER_URL = BASE_URL + '/tradeApi/orders/place.do'
CLOSE_ORDER_URL = BASE_URL + '/tradeApi/positions/close.do'
ORDER_CANCEL_ALL_URL = BASE_URL + '/tradeApi/orders/batchCancel.do'
ORDER_CANCEL_URL = BASE_URL + '/tradeApi/orders/cancel.do'
USER_POSITION_URL = BASE_URL + '/tradeApi/positions.do'


def get_common_request_json():
    common = {
        "AppKey": variable.BFX_API_KEY,
        "Timestamp": str(int(time.time())),
    }
    return common


def convert_request(key_list, origin_dict):
    sign_content = ''
    for key in key_list:
        d = str(key) + '=' + urllib.parse.quote(str(origin_dict[key]))
        sign_content += d
        sign_content += '&'
    if len(sign_content) > 0:
        sign_content = sign_content[:-1]
    return sign_content


def do_api_request(method, url, content_json):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }
    common_json = get_common_request_json()
    request_json = dict(common_json, **content_json)
    key_list = sorted(request_json.keys(), reverse=False)
    url_content = convert_request(key_list, request_json)
    # print(url_content)
    sign_content = variable.BFX_SECRET + url_content.replace('=', '').replace('&', '') + variable.BFX_SECRET
    # print(sign_content)
    sign = hashlib.md5(sign_content.encode('utf8')).hexdigest()
    # print(sign)
    full_url = url + '?' + url_content + '&Signature=' + sign
    print(method, full_url)
    if method == const.POST:
        response = requests.post(full_url, headers=header)
    else:
        response = requests.get(full_url, headers=header)
    # print(headers)
    print(response.text)
    return response.json()


class BFXApi(AbsApi):

    def __init__(self):
        self.symbol = util.get_bfx_symbol(variable.CURRENT_ID)

    def double_check(self):
        time.sleep(1)
        user_position.set_target_position(self.get_user_position())
        print('Double check', user_position.get_target_position().value())

    def double_check_position(self):
        threading.Thread(target=self.double_check).start()

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        # threading.Thread(target=self.open_order, args=(price, amount, side)).start()
        self.open_order(price, amount, side)

    def open_order(self, price, amount, side):
        content_json = {
            'symbol': self.symbol,
            'operation': side.lower(),
            'amount': str(amount),
            'price': str(price),
            'multiple': 20
        }
        result = do_api_request(const.POST, ORDER_URL, content_json)
        order_id = result['data']
        time.sleep(0.8)
        threading.Thread(target=self.after_open, args=(order_id, )).start()
        # self.double_check_position()

    def after_open(self, order_id):
        if order_id is not None:
            self.cancel_order(order_id)
        user_position.set_target_position(self.get_user_position())
        print('After open', user_position.get_target_position().value())

    def close_order_async(self, price, amount, side, _id=None):
        print('************************** Close ', price, amount, '**************************')
        # threading.Thread(target=self.close_order, args=(price, amount, side, _id)).start()
        self.close_order(price, amount, side, _id)

    def close_order(self, price, amount, side, _id):
        content_json = {
            'symbol': self.symbol,
            'amount': str(amount),
            'price': str(price),
            'positionId': _id
        }
        do_api_request(const.POST, CLOSE_ORDER_URL, content_json)
        time.sleep(0.8)
        self.cancel_all()
        user_position.set_target_position(self.get_user_position())
        print('After close', user_position.get_target_position().value())
        self.double_check_position()

    def cancel_all(self):
        content_json = {
            'symbol': self.symbol,
            'side': "all"
        }
        do_api_request(const.POST, ORDER_CANCEL_ALL_URL, content_json)

    def cancel_order(self, order_id):
        content_json = {
            'symbol': self.symbol,
            'orderId': str(order_id)
        }
        do_api_request(const.POST, ORDER_CANCEL_URL, content_json)

    def get_user_position(self):
        content_json = {
            'symbol': self.symbol
        }
        response = do_api_request(const.POST, USER_POSITION_URL, content_json)
        if response['code'] == 0:
            data = response['data']
            for d in data:
                if d['symbol'] != self.symbol:
                    continue
                side = d['direction']
                position = Position()
                position.amount = d['holdCount']
                position.average_price = d['avgPrice']
                position.position_id = d['positionId']
                position.side = const.BUY if side == 1 else const.SELL
                return position
            return Position()
        else:
            return Position()


# bfx = BFXApi()
# bfx.get_user_position()
# bfx.open_order(1.55, 10, const.BUY)
# bfx.close_order(1.54, 10, const.SELL, 2851229)