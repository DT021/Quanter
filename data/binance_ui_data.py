from selenium import webdriver
import variable, const
import threading, copy
import time, datetime

site = None

LOCK = threading.Lock()
last_price = 0

buy_1_list = []
sell_1_list = []
LIST_SIZE = 5


def get_bn_url():
    if variable.CURRENT_ID == const.BTC_REVERSE or variable.CURRENT_ID == const.BTC:
        return 'https://www.binance.co/en/trade/BTC_USDT'
    elif variable.CURRENT_ID == const.ETH or variable.CURRENT_ID == const.ETH_REVERSE:
        return 'https://www.binance.co/en/trade/ETH_USDT'
    elif variable.CURRENT_ID == const.EOS or variable.CURRENT_ID == const.EOS_REVERSE:
        return 'https://www.binance.co/en/trade/EOS_USDT'
    elif variable.CURRENT_ID == const.LTC:
        return 'https://www.binance.co/en/trade/LTC_USDT'
    elif variable.CURRENT_ID == const.ETC:
        return 'https://www.binance.co/en/trade/ETC_USDT'
    elif variable.CURRENT_ID == const.BCH:
        return 'https://www.binance.co/en/trade/BCHABC_USDT'


def get_quote_1():
    try:
        sell_1_price = float(site.find_element_by_xpath(
            '//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]').text)
        buy_1_price = sell_1_price
        # sell_1_price = float(site.find_element_by_xpath(
        #     '/html/body/div[1]/div/main/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[19]/div[2]/span').text)
        # buy_1_price = float(site.find_element_by_xpath(
        #     '/html/body/div[1]/div/main/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div[4]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/span').text)
        return sell_1_price, buy_1_price
    except Exception:
        return -1, -1


def get_compare_quote_1():
    sell_1_price, buy_1_price = get_quote_1()
    return sell_1_price + variable.PRICE_SHIFT, buy_1_price + variable.PRICE_SHIFT


def get_sell_1_list():
    LOCK.acquire()
    list_copy = copy.deepcopy(sell_1_list)
    LOCK.release()
    return list_copy


def get_buy_1_list():
    LOCK.acquire()
    list_copy = copy.deepcopy(buy_1_list)
    LOCK.release()
    return list_copy


def open_thread():
    global site, last_price
    site = webdriver.Firefox()
    site.get(get_bn_url())
    time.sleep(3)
    last_price = 1


def start():
    threading.Thread(target=open_thread).start()
