from api.base_api import AbsApi
import variable, time, const
import hashlib
import hmac
import base64
import requests
import urllib.parse
from bean import Position
import util
import threading
import api.user_position as user_position


BASE_URL = 'https://api.bybit.com'
ORDER_URL = BASE_URL + '/open-api/order/create'
ORDER_LIST_URL = BASE_URL + '/order/list'
ORDER_CANCEL_URL = BASE_URL + '/order/cancel'
USER_POSITION_URL = BASE_URL + '/position/list'


def get_common_request_json():
    common = {
        "api_key": variable.BY_API_KEY,
        "timestamp": str(int(time.time() * 1000)),
    }
    return common


def get_order_state(response):
    if response['status'] == 'ok':
        data = response['data']
        return data['state']


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
    common_json = get_common_request_json()
    request_json = dict(common_json, **content_json)
    key_list = sorted(request_json.keys(), key=str.lower, reverse=False)
    sign_content = convert_request(key_list, request_json)
    sha256 = hmac.new(bytes(variable.BY_SECRET, 'utf-8'), bytes(sign_content, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
    full_url = url + '?' + sign_content + '&sign=' + sha256
    if method == const.POST:
        response = requests.post(full_url)
    else:
        response = requests.get(full_url)
    print(method, full_url)
    print(response.text)
    return response.json()


class BybitApi(AbsApi):

    def __init__(self):
        self.symbol = util.get_by_symbol(variable.CURRENT_ID)

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        threading.Thread(target=self.open_order, args=(price, amount, side)).start()

    def open_order(self, price, amount, side):
        content_json = {
            'symbol': self.symbol,
            'order_type': 'Limit',
            'side': side,
            'qty': int(amount),
            'price': price,
            'time_in_force': 'ImmediateOrCancel'
        }
        do_api_request(const.POST, ORDER_URL, content_json)
        time.sleep(0.3)
        user_position.set_target_position(self.get_user_position())
        print('After open', user_position.get_target_position().value())

    def close_order_async(self, price, amount, side, _id=None):
        print('************************** Close ', price, amount, '**************************')
        self.close_order(price, amount, side, _id)

    def close_order(self, price, amount, side, _id):
        content_json = {
            'symbol': self.symbol,
            'order_type': 'Limit',
            'side': side,
            'qty': int(amount),
            'price': price,
            'time_in_force': 'ImmediateOrCancel'
        }
        do_api_request(const.POST, ORDER_URL, content_json)
        time.sleep(0.4)
        user_position.set_target_position(self.get_user_position())
        print('After close', user_position.get_target_position().value())

    def get_user_position(self):
        content_json = {
            # 'symbol': self.symbol
        }
        response = do_api_request(const.GET, USER_POSITION_URL, content_json)
        if response['ret_code'] == 0:
            data = response['result']
            for d in data:
                if d['symbol'] != self.symbol:
                    continue
                side = d['side']
                if side == 'None':
                    return Position()
                position = Position()
                position.amount = d['size']
                position.average_price = d['entry_price']
                position.side = side
                return position
            return Position()
        else:
            return Position()
