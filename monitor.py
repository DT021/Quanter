import time
import data.ui_data as ui
from selenium import webdriver
import variable, util, const
import data.ws_data as ws_data
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
    temp_ws_sell_1 = 0
    temp_ws_buy_1 = 0
    temp_buy_price = 0
    temp_sell_price = 0
    while True:
        last_price = ws_data.get_source().get_last_price()
        if last_price < 0:
            wechat.send_message('ws掉线了')
            break
        elif last_price == 0:
            print('ws暂时没有数据')
            time.sleep(3)
            continue
        start_time = time.time()
        which = variable.COMPARE_WITH
        buy_price = ui.get_buy_price(which)
        sell_price = ui.get_sell_price(which)
        if buy_price < 0 or sell_price < 0 or buy_price > sell_price:
            continue
        ws_sell_1, ws_buy_1 = ws_data.get_source().get_compare_quote_1()
        if ws_buy_1 < 0 or ws_sell_1 < 0 or ws_buy_1 > ws_sell_1:
            continue
        ui_time = time.time() - start_time
        data_time = time.time() - start_time - ui_time
        if temp_ws_sell_1 != ws_sell_1 or temp_ws_buy_1 != ws_buy_1 \
                or temp_buy_price != buy_price or temp_sell_price != sell_price:
            strategy.receive_price_change(buy_price, sell_price, ws_buy_1, ws_sell_1)
            print(util.get_print_datetime(), 'ws:'+str([ws_buy_1, ws_sell_1]),
                  '买卖'+str(which), str([buy_price, sell_price]), position.get_target_position().value(),
                  '耗时:', int((time.time() - start_time)*1000),
                  ws_data.get_source().get_buy_1_list(), ws_data.get_source().get_sell_1_list())

        temp_ws_sell_1 = ws_sell_1
        temp_ws_buy_1 = ws_buy_1
        temp_buy_price = buy_price
        temp_sell_price = sell_price


def run():
    try:
        position.set_target_position(api.get_site_api().get_user_position())
        print('target position: ', position.get_target_position().value())
        if variable.TARGET_STRATEGY == const.STRATEGY_DB_HEDGE:
            position.set_bm_position(api.get_bitmex_api().get_user_position())
            print('bm position: ', position.get_bm_position().value())
        ws_data.get_source().start()
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
        elif input_text == 'biex' or input_text == 'db' or input_text == 'by' or input_text == 'bfx':
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
        elif input_text == 'p':
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



