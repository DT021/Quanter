from api.base_api import AbsApi
from deribit_api import RestClient
import json
from bean import Position
import variable, const, util
import time
import api.user_position as user_position


class DeribitApi(AbsApi):
    client = None

    def __init__(self):
        self.client = RestClient(variable.DB_API_KEY, variable.DB_SECRET)

    def get_user_position(self):
        response = self.client.positions()
        position_result = Position()
        for position in response:
            position_result.average_price = position['averagePrice']
            position_result.amount = position['size']
            position_result.side = const.BUY if position['direction'] == 'buy' else const.SELL
            break
        return position_result

    def open_order(self, price, amount, side):
        self.client.buy('BTC-PERPETUAL', amount, price)
        time.sleep(0.1)
        user_position.set_target_position(self.get_user_position())
        self.cancel_all_order()

    def close_order(self, price, amount, side, _id=None):
        self.client.sell('BTC-PERPETUAL', amount, price)
        time.sleep(0.1)
        user_position.set_target_position(self.get_user_position())
        self.cancel_all_order()

    def cancel_all_order(self):
        return self.client.cancelall()

