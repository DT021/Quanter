from strategy.base_strategy import AbsStrategy
import api.user_position as user_position
import api.core as api
import data.ui_data as ui_data
import data.bitmex_data as bitmex_data
import const, variable
import wechat_notifier as wechat
import threading

RATIO = 0.1


def wechat_notify():
    wechat.send_message('db position:'+str(user_position.get_target_position().value())
                        + 'bm hedge:'+str(user_position.get_bm_position().value()))


def get_cal_amount(position):
    if position.amount <= 0:
        target_amount = 0
    else:
        if position.side == const.BUY:
            target_amount = position.amount
        else:
            target_amount = -position.amount
    return target_amount


class DBHedgeStrategy(AbsStrategy):
    bitmex_buy_1_price = -1
    bitmex_sell_1_price = -1
    bitmex_real_sell_1 = -1
    bitmex_real_buy_1 = -1

    def check_need_close(self):
        if self.bitmex_buy_1_price <= 0 or self.bitmex_sell_1_price <= 0:
            return
        target_position = user_position.get_target_position()
        bm_position = user_position.get_bm_position()
        target_amount = get_cal_amount(target_position)
        bm_amount = int(get_cal_amount(bm_position) * RATIO)
        available_amount = target_amount + bm_amount
        if available_amount == 0:
            return
        if available_amount < 0:
            side = const.SELL
        else:
            side = const.BUY
        available_amount = abs(available_amount)

        buy_1_price = ui_data.get_buy_price(1)
        sell_1_price = ui_data.get_sell_price(1)

        print('****db amount:', target_amount, 'bm amount:', bm_amount, 'result:', side, available_amount)
        print('check close:', target_position.value(), bm_position.value(),
              [self.bitmex_buy_1_price, self.bitmex_sell_1_price], [buy_1_price, sell_1_price])

        sell_1_amount, buy_1_amount = bitmex_data.get_amount_1()

        if side == const.BUY:
            if (self.bitmex_sell_1_price - sell_1_price <= variable.CLOSE_THRESHOLD) \
                    and (self.bitmex_real_sell_1 - self.bitmex_real_buy_1 <= variable.BM_CLOSE_DIFF):
                if buy_1_amount < 0:
                    return
                api.get_bitmex_api().close_order(self.bitmex_real_buy_1, int(min(available_amount, buy_1_amount)/RATIO),
                                                 const.SELL)
                threading.Thread(target=wechat_notify).start()

        elif side == const.SELL:
            if (buy_1_price - self.bitmex_buy_1_price <= variable.CLOSE_THRESHOLD) \
                    and (self.bitmex_real_sell_1 - self.bitmex_real_buy_1 <= variable.BM_CLOSE_DIFF):
                if sell_1_amount < 0:
                    return
                api.get_bitmex_api().close_order(self.bitmex_real_sell_1, int(min(sell_1_amount, available_amount)/RATIO),
                                                 const.BUY)
                threading.Thread(target=wechat_notify).start()

    def check_need_open(self, sell_2_price, buy_2_price):
        result = False
        if self.bitmex_sell_1_price - sell_2_price >= variable.THRESHOLD:
            diff = self.bitmex_sell_1_price - sell_2_price - variable.THRESHOLD
            if diff > 2:
                diff = 2
            api.get_site_api().open_order_async(sell_2_price + diff, variable.MAX_AMOUNT, const.BUY)
            result = True
        elif buy_2_price - self.bitmex_buy_1_price >= variable.THRESHOLD:
            diff = buy_2_price - self.bitmex_buy_1_price - variable.THRESHOLD
            if diff > 2:
                diff = 2
            api.get_site_api().open_order_async(buy_2_price - diff, variable.MAX_AMOUNT, const.SELL)
            result = True
        return result

    def on_price_change(self, sell_2, buy_2):
        if variable.THRESHOLD < 0 or variable.CLOSE_THRESHOLD < 0:
            print('threshold need init')
            return

        self.bitmex_sell_1_price, self.bitmex_buy_1_price = bitmex_data.get_compare_quote_1()
        self.bitmex_real_sell_1, self.bitmex_real_buy_1 = bitmex_data.get_quote_1()
        if not self.check_need_open(sell_2, buy_2):
            self.check_need_close()