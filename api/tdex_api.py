from api.base_api import AbsApi
import json
from bean import Position
import variable, const, util
import time
import api.user_position as user_position
import threading
import requests
import hashlib
import time
import hmac


class Configs(object):
    def __init__(self):
        self.url = 'https://www.tdex.com/openapi/v1'
        self.headers = {
            'Content-Type': 'application/json',
        }

    def hmac_sign(self, path, expires, data=None):
        if data is None:
            data = ''
        msg = path + expires + data
        res = hmac.new(bytes(variable.TDEX_SECRET, 'utf-8'), bytes(msg, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        return res

    def verification(self, data, path):
        expires = str(int(int(round(time.time() * 1000)) / 100000))
        input = data
        curPath = path
        sign = self.hmac_sign(curPath, expires, input)
        self.headers['api-signature'] = sign
        self.headers['api-expires'] = expires

    def request(self, data, path, type):
        if type == 'get':
            res = requests.post(self.url + path, data, headers=self.headers).json()
        else:
            res = requests.put(self.url + path, data, headers=self.headers).json()
        return res


class Tdex(object):
    configs = Configs()

    def __init__(self):
        self.configs.headers['api-key'] = variable.TDEX_API_KEY

    def requestApi(self, input, path, type=None):
        self.configs.verification(input, path)
        res = self.configs.request(input, path, type)
        return res

    def futuresOpen(self, data={}):
        input = json.dumps(data)
        path = '/futures/open'
        res = self.requestApi(input, path)
        return res

    def futuresClose(self, data={}):
        input = json.dumps(data)
        path = '/futures/close'
        res = self.requestApi(input, path)
        return res

    def futuresGetOrders(self):
        input = json.dumps({})
        path = '/futures/orders'
        res = self.requestApi(input, path, type)
        return res

    def futuresGetPosition(self):
        input = json.dumps({})
        path = '/futures/position'
        res = self.requestApi(input, path, type)
        return res

    def futuresCancelOrders(self, data={}):
        input = json.dumps(data)
        path = '/futures/cancel'
        res = self.requestApi(input, path, type)
        return res

    def futuresScheme(self, data={}, type='get'):
        input = json.dumps(data)
        path = '/futures/scheme'
        res = self.requestApi(input, path, type)
        return res


def get_tdex_cid():
    return 1


class TdexApi(AbsApi):
    client = None

    def __init__(self):
        self.client = Tdex()
        options = {
                "shared": False,
                "merged": True
        }
        set_data = {
            "cid": get_tdex_cid(),
            "options": options
        }
        get_data = {
            "cid": get_tdex_cid(),
        }
        print(self.client.futuresScheme(data=set_data, type='set'))
        print(self.client.futuresScheme(data=get_data))

    def get_user_position(self):
        response = self.client.futuresGetPosition()
        print(response)
        return None

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        threading.Thread(target=self.open_order, args=(price, amount, side)).start()

    def open_order(self, price, amount, side):
        data = {
            "cid": get_tdex_cid(),
            "side": 0 if side == const.BUY else 1,
            "scale": 20,
            "volume": int(amount),
            "price": price
        }
        print(self.client.futuresOpen(data))

    def merge_order(self):
        pass

    def close_order(self, price, amount, side, _id=None):
        self.client.sell('BTC-PERPETUAL', amount, price)
        time.sleep(0.1)
        user_position.set_target_position(self.get_user_position())
        self.cancel_all_order()

    def cancel_all_order(self):
        return self.client.cancelall()


# tdex = TdexApi()
# tdex.open_order(3960, 1, const.BUY)
# tdex.get_user_position()