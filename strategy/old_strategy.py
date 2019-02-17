from strategy.base_strategy import AbsStrategy
import api.user_position as user_position
import api.core as api
import data.ui_data as ui_data
import data.bitmex_data as bitmex_data
import const, variable


class OldStrategy(AbsStrategy):
    bitmex_buy_1_price = -1
    bitmex_sell_1_price = -1

    def check_need_close(self):
        position = user_position.get_target_position()
        if position.amount <= 0:
            return
        available_amount = position.amount
        if self.bitmex_buy_1_price <= 0 or self.bitmex_sell_1_price <= 0:
            return

        buy_1_price = ui_data.get_buy_price(1)
        sell_1_price = ui_data.get_sell_price(1)

        if buy_1_price < 0 or sell_1_price < 0:
            return

        if position.side == const.BUY:
            if (self.bitmex_sell_1_price - sell_1_price <= variable.CLOSE_THRESHOLD) \
                    and (sell_1_price - buy_1_price <= variable.CLOSE_DIFF):
                buy_1_amount = ui_data.get_buy_amount(1)
                if buy_1_amount < 0:
                    buy_1_amount = 999999
                api.get_site_api().close_order(const.SELL, buy_1_price, min(available_amount, buy_1_amount))
        elif position.side == const.SELL:
            if (buy_1_price - self.bitmex_buy_1_price <= variable.CLOSE_THRESHOLD) \
                    and (sell_1_price - buy_1_price <= variable.CLOSE_DIFF):
                sell_1_amount = ui_data.get_sell_amount(1)
                if sell_1_amount < 0:
                    sell_1_amount = 999999
                    api.get_site_api().close_order(const.BUY, sell_1_price, min(sell_1_amount, available_amount))

    def check_need_open(self, sell_2_price, buy_2_price):
        result = False
        position = user_position.get_target_position()
        if self.bitmex_sell_1_price - sell_2_price >= variable.THRESHOLD and position.side != const.SELL:
            sell_3_price = ui_data.get_sell_price(3)
            if sell_3_price > 0 and self.bitmex_sell_1_price - sell_3_price >= variable.THRESHOLD:
                api.get_site_api().open_order(const.BUY, sell_3_price)
            else:
                api.get_site_api().open_order(const.BUY, sell_2_price)
            result = True
        elif buy_2_price - self.bitmex_buy_1_price >= variable.THRESHOLD and position.side != const.BUY:
            buy_3_price = ui_data.get_buy_price(3)
            if buy_3_price > 0 and buy_3_price - self.bitmex_buy_1_price >= variable.THRESHOLD:
                api.get_site_api().open_order(const.SELL, buy_3_price)
            else:
                api.get_site_api().open_order(const.SELL, buy_2_price)
            result = True
        return result

    def on_price_change(self, sell_2, buy_2):
        if variable.THRESHOLD < 0 or variable.CLOSE_THRESHOLD < 0:
            print('threshold need init')
            return

        self.bitmex_sell_1_price, self.bitmex_buy_1_price = bitmex_data.get_quote_1()
        if not self.check_need_open(sell_2, buy_2):
            self.check_need_close()