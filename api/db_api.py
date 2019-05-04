from api.base_api import AbsApi
from deribit_api import RestClient
import json
from bean import Position
import variable, const, util
import time
import api.user_position as user_position
import threading


class DeribitApi(AbsApi):
    client = None

    def __init__(self):
        self.client = RestClient(variable.DB_API_KEY, variable.DB_SECRET)

    def double_check(self):
        time.sleep(1)
        user_position.set_target_position(self.get_user_position())
        print('Double check', user_position.get_target_position().value())

    def double_check_position(self):
        threading.Thread(target=self.double_check).start()

    def get_user_position(self):
        response = self.client.positions()
        print(response)
        position_result = Position()
        for position in response:
            position_result.average_price = position['averagePrice']
            position_result.amount = position['size']
            position_result.side = const.BUY if position['direction'] == 'buy' else const.SELL
            break
        return position_result

    def open_order_async(self, price, amount, side):
        print('************************** Open ', side, price, '**************************')
        threading.Thread(target=self.open_order, args=(price, amount, side)).start()

    def open_order(self, price, amount, side):
        if side == const.BUY:
            self.client.buy('ETH-PERPETUAL', amount, price)
        else:
            self.client.sell('ETH-PERPETUAL', amount, price)
        time.sleep(0.2)
        user_position.set_target_position(self.get_user_position())
        print('After open', user_position.get_target_position().value())
        self.double_check_position()

    def close_order_async(self, price, amount, side, _id=None):
        print('************************** Close ', price, amount, '**************************')
        self.close_order(price, amount, side, _id)

    def close_order(self, price, amount, side, _id=None):
        if side == const.BUY:
            self.client.buy('ETH-PERPETUAL', amount, price)
        else:
            self.client.sell('ETH-PERPETUAL', amount, price)
        time.sleep(0.2)
        user_position.set_target_position(self.get_user_position())
        print('After close', user_position.get_target_position().value())
        self.double_check_position()

    def cancel_all_order(self):
        return self.client.cancelall()
