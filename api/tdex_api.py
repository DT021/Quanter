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


BASE_URL = 'https://api.biex.com/api/v1'
ORDER_URL = BASE_URL + '/order/order'
ORDER_INFO_URL = BASE_URL + '/order/order_info'
ORDER_CANCEL_URL = BASE_URL + '/order/order_cancel'
ORDER_CANCEL_ALL_URL = BASE_URL + '/order/order_cancel_all'
USER_POSITION_URL = BASE_URL + '/fund/contractAccountPosition'


def get_common_request_json():
    common = {
        "charset": "UTF-8",
        "api_key": variable.TDEX_API_KEY,
        "format": "json",
        "version": "1.0",
        "sign_type": "HmacSHA256",
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
    sha256 = hmac.new(bytes(variable.TDEX_SECRET, 'utf-8'), bytes(sign_content, 'utf-8'), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(sha256)
    signature = bytes.decode(signature)
    common_json['sign'] = signature
    full_url = url + '?' + convert_request(common_json.keys(), common_json)
    if method == const.POST:
        response = requests.post(full_url, data=content_json)
    else:
        full_url = full_url + '&' + convert_request(content_json.keys(), content_json)
        response = requests.get(full_url)
    print(method, full_url)
    # print(response.text)
    return response.json()


class TdexApi(AbsApi):

    def __init__(self):
        self.symbol = util.get_common_symbol(variable.CURRENT_ID)

    def get_position(self):
        pass

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        threading.Thread(target=self.open_order, args=(price, amount, side)).start()

    def open_order(self, price, amount, side):
        content_json = {
            'symbol': self.symbol,
            'type': 'limitPrice',
            'side': 'sell' if side == const.SELL else 'buy',
            'amount': amount,
            'price': price
        }
        do_api_request(const.POST, ORDER_URL, content_json)
        time.sleep(0.8)
        self.cancel_all_order()
        time.sleep(0.8)
        user_position.set_target_position(self.get_user_position())
        print('After open', user_position.get_target_position().value())

    def close_order_async(self, price, amount, side, _id=None):
        print('************************** Close ', price, amount, '**************************')
        self.close_order(price, amount, side, _id)

    def close_order(self, price, amount, side, _id):
        content_json = {
            'symbol': self.symbol,
            'type': 'limitPrice',
            'side': 'sell' if side == const.SELL else 'buy',
            'amount': amount,
            'price': price
        }
        do_api_request(const.POST, ORDER_URL, content_json)
        time.sleep(0.8)
        self.cancel_all_order()
        time.sleep(0.8)
        user_position.set_target_position(self.get_user_position())
        print('After close', user_position.get_target_position().value())

    def get_order_info(self, order_id):
        content_json = {
            'symbol': self.symbol,
            'orderId': int(order_id),
        }
        return do_api_request(const.GET, ORDER_INFO_URL, content_json)

    def cancel_order(self, order_id):
        content_json = {
            'symbol': self.symbol,
            'orderId': int(order_id),
        }
        return do_api_request(const.POST, ORDER_CANCEL_URL, content_json)

    def cancel_all_order(self):
        content_json = {
            'symbol': self.symbol,
        }
        return do_api_request(const.POST, ORDER_CANCEL_ALL_URL, content_json)

    def get_user_position(self):
        content_json = {
            'symbol': self.symbol,
        }
        response = do_api_request(const.GET, USER_POSITION_URL, content_json)
        if response['status'] == 'ok':
            data = response['data']
            for d in data:
                amount = int(d['position'])
                if amount <= 0:
                    return Position()
                position = Position()
                position.amount = amount
                position.average_price = float(d['avgCost'])
                position.side = const.BUY if d['side'] == 'Long' else const.SELL
                return position
            return Position()
        else:
            return Position()


# variable.CURRENT_ID = const.ETH_REVERSE
# biex = BiexApi()
# # biex.open_order(144, 1, const.BUY)
# biex.open_order(143, 1, const.SELL)
# biex.open_order(122, 1, const.BUY)
# biex.cancel_all_order()
# biex.cancel_order(190744117611995138)
# print(biex.get_user_position().value())
