from strategy.base_strategy import AbsStrategy
import api.user_position as user_position
import api.core as api
import data.ui_data as ui_data
import data.ws_data as ws_data
import const, variable


class OldStrategy(AbsStrategy):
    ws_buy_1_price = -1
    ws_sell_1_price = -1

    def check_need_close(self):
        position = user_position.get_target_position()
        if position.amount <= 0:
            return
        available_amount = position.amount
        if self.ws_buy_1_price <= 0 or self.ws_sell_1_price <= 0:
            return

        buy_1_price = ui_data.get_buy_price(1)
        sell_1_price = ui_data.get_sell_price(1)
        print(variable.CLOSE_THRESHOLD, variable.CLOSE_DIFF, 'check close:', position.value(),
              [self.ws_buy_1_price, self.ws_sell_1_price], [buy_1_price, sell_1_price])
        print('Buy:', self.ws_sell_1_price - sell_1_price <= variable.CLOSE_THRESHOLD,
              sell_1_price - buy_1_price <= variable.CLOSE_DIFF,
              'Sell:', buy_1_price - self.ws_buy_1_price <= variable.CLOSE_THRESHOLD,
              sell_1_price - buy_1_price <= variable.CLOSE_DIFF)

        if buy_1_price < 0 or sell_1_price < 0:
            return

        if position.side == const.BUY:
            if (self.ws_sell_1_price - sell_1_price <= variable.CLOSE_THRESHOLD) \
                    and (sell_1_price - buy_1_price <= variable.CLOSE_DIFF):
                buy_1_amount = ui_data.get_buy_amount(1)
                if buy_1_amount < 0:
                    buy_1_amount = 999999
                api.get_site_api().close_order_async(buy_1_price, min(available_amount, buy_1_amount),
                                                     const.SELL, position.position_id)
        elif position.side == const.SELL:
            if (buy_1_price - self.ws_buy_1_price <= variable.CLOSE_THRESHOLD) \
                    and (sell_1_price - buy_1_price <= variable.CLOSE_DIFF):
                sell_1_amount = ui_data.get_sell_amount(1)
                if sell_1_amount < 0:
                    sell_1_amount = 999999
                api.get_site_api().close_order_async(sell_1_price, min(sell_1_amount, available_amount),
                                                     const.BUY, position.position_id)

    def check_need_open(self, sell_price, buy_price):
        result = False
        position = user_position.get_target_position()
        price_step = variable.PRICE_STEP
        threshold = variable.THRESHOLD
        if variable.COMPARE_WITH == const.COMPARE_WITH_TICK2:
            threshold = threshold - price_step
        if self.ws_sell_1_price - sell_price >= threshold and buy_price - self.ws_buy_1_price >= threshold:
            print('bitmex data is not stable')
            return result

        if self.ws_sell_1_price - sell_price >= threshold and position.side != const.SELL:
            next_sell_price = ui_data.get_sell_price(2 if variable.COMPARE_WITH == const.COMPARE_WITH_TICK1 else 3)
            if next_sell_price > 0 and self.ws_sell_1_price - next_sell_price >= threshold:
                api.get_site_api().open_order_async(next_sell_price, variable.MAX_AMOUNT, const.BUY)
            else:
                api.get_site_api().open_order_async(sell_price, variable.MAX_AMOUNT, const.BUY)
            result = True
        elif buy_price - self.ws_buy_1_price >= threshold and position.side != const.BUY:
            next_buy_price = ui_data.get_buy_price(2 if variable.COMPARE_WITH == const.COMPARE_WITH_TICK1 else 3)
            if next_buy_price > 0 and next_buy_price - self.ws_buy_1_price >= threshold:
                api.get_site_api().open_order_async(next_buy_price, variable.MAX_AMOUNT, const.SELL)
            else:
                api.get_site_api().open_order_async(buy_price, variable.MAX_AMOUNT, const.SELL)
            result = True
        return result

    def on_price_change(self, sell_price, buy_price, ws_buy_1, ws_sell_1):
        if variable.THRESHOLD < 0 or variable.CLOSE_THRESHOLD < 0:
            print('threshold need init')
            return

        if variable.WS_SOURCE == const.UI_SOURCE_BINANCE:
            self.ws_sell_1_price, self.ws_buy_1_price = ws_sell_1, ws_buy_1
        else:
            self.ws_sell_1_price, self.ws_buy_1_price = ws_data.get_source().get_compare_quote_1()
        if not self.check_need_open(sell_price, buy_price):
            self.check_need_close()