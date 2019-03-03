from api.base_api import AbsApi
import api.bbx_cipher as cipher
import api.user_position as user_position
from bean import Position
import const, variable
import time
import requests
import json
import threading


BASE_URL = 'https://api.bbxapp.vip/v1/ifcontract/'
SUBMIT_ORDER = BASE_URL + 'submitOrder'
CANCEL_ORDER = BASE_URL + 'cancelOrders'
USER_ORDER = BASE_URL + 'userOrders'
USER_POSITION = BASE_URL + 'userPositions'


def get_header(time_stamp):
    ts = str(int(time_stamp * 1000)) + '000'
    sign = cipher.encrypt(variable.BBX_TOKEN, ts)
    headers = {'Bbx-Ver': '1.0',
               'Bbx-Dev': 'web',
               'Bbx-Ts': ts,
               'Bbx-Uid': variable.BBX_UID,
               'Bbx-Sign': sign}
    # print(const.UID, ' use token: ', const.TOKEN)
    return headers


def send_post_request(url, data, time_stamp):
    return requests.post(url, headers=get_header(time_stamp), data=data)


class BbxApi(AbsApi):
    def get_user_position(self):
        url = USER_POSITION + '?contractID=' + str(variable.CURRENT_ID) + '&status=3'
        response = requests.get(url, headers=get_header(time.time())).json()
        if response['errno'] == 'OK':
            position_result = Position()
            data = response['data']
            positions = data['positions']
            for p in positions:
                hold_vol = p['hold_vol']
                freeze_vol = p['freeze_vol']
                position_result.amount = int(hold_vol) - int(freeze_vol)
                _type = p['position_type']
                position_result.side = const.BUY if _type == 1 else const.SELL
                position_result.position_id = p['position_id']
                position_result.average_price = float(p['hold_avg_price'])
                break
            return position_result
        print('********************get position failed', response)
        return None

    def open_order(self, price, amount, side):
        time_stamp = time.time()
        body = {
            "contract_id": int(variable.CURRENT_ID),
            "category": 1,
            "way": 1 if side == const.BUY else 4,
            "open_type": 1,
            "leverage": 100,
            "price": price,
            "vol": amount,
            "nonce": int(time_stamp)
        }
        response = send_post_request(SUBMIT_ORDER, json.dumps(body), time_stamp).json()
        time.sleep(0.3)
        user_position.set_target_position(self.get_user_position())
        print('After open', user_position.get_target_position().value())
        if response['message'] == 'Success':
            data = response['data']
            order_id = data['order_id']
            self.cancel_order(order_id)

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        threading.Thread(target=self.open_order, args=(price, amount, side)).start()

    def close_order(self, price, amount, side, _id):
        time_stamp = time.time()
        body = {
            "contract_id": int(variable.CURRENT_ID),
            "category": 1,
            "way": 2 if side == const.BUY else 3,
            "position_id": int(_id),
            "price": price,
            "vol": amount,
            "nonce": int(time_stamp)
        }
        response = send_post_request(SUBMIT_ORDER, json.dumps(body), time_stamp).json()
        time.sleep(0.3)
        if response['message'] == 'Success':
            data = response['data']
            order_id = data['order_id']
            self.cancel_order(order_id)
        user_position.set_target_position(self.get_user_position())
        print('After close', user_position.get_target_position().value())

    def close_order_async(self, price, amount, side, _id):
        print('************************** Close ', price, amount, '**************************')
        threading.Thread(target=self.close_order, args=(price, amount, side, _id)).start()

    def cancel_order(self, order_id):
        time_stamp = time.time()
        orders = []
        contract_order = {
            'contract_id': int(variable.CURRENT_ID),
            'orders': [order_id]
        }
        orders.append(contract_order)
        body = {
            "orders": orders,
            "nonce": int(time_stamp)
        }
        response = send_post_request(CANCEL_ORDER, json.dumps(body), time_stamp)
        print(response.text)

    def get_order_info(self, order_id): pass


# variable.CURRENT_ID = const.ETH
# variable.BBX_UID = '100055833945'
# variable.BBX_TOKEN = '615b8f2232a811e980ff0242ac120004'
#
# bbx = BbxApi()
# bbx.open_order(125.5, 1, const.SELL)
