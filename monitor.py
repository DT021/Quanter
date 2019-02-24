import time
import data.ui_data as ui
from selenium import webdriver
import variable, util, const
import data.bitmex_data as bitmex_data
import wechat_notifier as wechat
import strategy.strategy_core as strategy
import api.user_position as position
import api.core as api
import traceback
import api.bbx_login as bbx_login
import threading


def init_browser():
    browser = webdriver.Firefox()
    browser.get(variable.TARGET_SITE_URL)
    print(variable.TARGET_SITE_URL)
    ui.init(browser)


def start_monitor():
    temp_bitmex_sell_1 = 0
    temp_bitmex_buy_1 = 0
    temp_buy_2_price = 0
    temp_sell_2_price = 0
    while True:
        if bitmex_data.last_price < 0:
            wechat.send_message('bitmex掉线了')
            break
        elif bitmex_data.last_price == 0:
            print('bitmex暂时没有数据')
            time.sleep(3)
            continue
        start_time = time.time()
        buy_2_price = ui.get_buy_price(2)
        sell_2_price = ui.get_sell_price(2)
        if buy_2_price < 0 or sell_2_price < 0:
            continue
        bitmex_sell_1, bitmex_buy_1 = bitmex_data.get_compare_quote_1()
        if bitmex_buy_1 < 0 or bitmex_sell_1 < 0:
            continue
        ui_time = time.time() - start_time
        data_time = time.time() - start_time - ui_time
        if temp_bitmex_sell_1 != bitmex_sell_1 or temp_bitmex_buy_1 != bitmex_buy_1 \
                or temp_buy_2_price != buy_2_price or temp_sell_2_price != sell_2_price:
            strategy.receive_price_change(buy_2_price, sell_2_price)
            print(util.get_print_datetime(), 'ws:'+str([bitmex_buy_1, bitmex_sell_1]),
                  # 'web:'+str([bitmex_last_price, bitmex_sell_1, bitmex_buy_1]),
                  '买卖二:'+str([buy_2_price, sell_2_price]), position.get_target_position().value(),
                  '耗时:', int((time.time() - start_time)*1000), bitmex_data.get_buy_1_list(), bitmex_data.get_sell_1_list())

        temp_bitmex_sell_1 = bitmex_sell_1
        temp_bitmex_buy_1 = bitmex_buy_1
        temp_buy_2_price = buy_2_price
        temp_sell_2_price = sell_2_price


def run():
    try:
        position.set_target_position(api.get_site_api().get_user_position())
        print('target position: ', position.get_target_position().value())
        if variable.TARGET_STRATEGY == const.STRATEGY_DB_HEDGE:
            position.set_bm_position(api.get_bitmex_api().get_user_position())
            print('bm position: ', position.get_bm_position().value())
        bitmex_data.open_bitmex_asyn()
        start_monitor()
    except Exception as e:
        traceback.print_exc()
        wechat.send_message(str(e))


def ready():
    init_browser()
    while True:
        input_text = input('开始监控:')
        if input_text == 'y':
            pass
        elif input_text == 'biex' or input_text == 'db' or input_text == 'by':
            threading.Thread(target=run).start()
        elif input_text == 'bbx':
            _type = input('Run type(a/A as auto, m/M as manual):')
            if _type == 'a':
                bbx_login.get_token_uid()
                if variable.BBX_TOKEN == '':
                    print('login failed')
                else:
                    threading.Thread(target=run).start()
            elif _type == 'm':
                token = input('token: ')
                variable.BBX_TOKEN = token
                uid = input('uid')
                variable.BBX_UID = uid
                threading.Thread(target=run).start()
        elif input_text == 'position':
            position.set_target_position(api.get_site_api().get_user_position())
            print('target position: ', position.get_target_position().value())
            if variable.TARGET_STRATEGY == const.STRATEGY_DB_HEDGE:
                position.set_bm_position(api.get_bitmex_api().get_user_position())
                print('bm position: ', position.get_bm_position().value())
            print('manual update position!')
        elif input_text == 'shift':
            value = input('value: ')
            print('before:', variable.PRICE_SHIFT)
            variable.PRICE_SHIFT = float(value)
            print('after:', variable.PRICE_SHIFT)



