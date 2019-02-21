from api.base_api import AbsApi
import bitmex
import json
from bean import Position
import variable, const, util
import time
import api.user_position as user_position


class BitmexApi(AbsApi):
    client = None
    symbol = None

    def __init__(self):
        self.client = bitmex.bitmex(test=False, api_key=variable.BM_KEY, api_secret=variable.BM_SECRET)
        self.symbol = util.get_bm_ticker(variable.CURRENT_ID)

    def get_user_position(self):
        response = self.client.Position.Position_get(filter=json.dumps({'symbol': self.symbol})).result()
        position_list = response[0]
        if len(position_list) == 0:
            return Position()
        position = position_list[0]
        result_position = Position()
        average_price = position['avgEntryPrice']
        if average_price <= 0:
            return result_position
        result_position.average_price = average_price
        amount = position['execQty']
        result_position.side = const.BUY if amount > 0 else const.SELL
        result_position.amount = abs(amount)
        return result_position

    def open_order(self, price, amount, side):
        print('************bm ', side, price, amount, '****************')
        self.client.Order.Order_new(symbol=self.symbol, orderQty=amount, price=price, side=side).result()
        time.sleep(0.1)
        user_position.set_bm_position(self.get_user_position())
        print('after bm position:', user_position.get_bm_position().value())
        self.cancel_all_order()

    def close_order(self, price, amount, side, _id=None):
        self.open_order(price, amount, side)

    def cancel_all_order(self):
        return self.client.Order.Order_cancelAll().result()

    def cancel_order(self, order_id): pass

    def get_order_info(self, order_id): pass






