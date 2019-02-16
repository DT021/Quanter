import variable, const
from const import Command

site = None


def init(browser):
    global site
    if variable.TARGET_SITE == const.BBX:
        site = BBXUiImpl(browser)
    elif variable.TARGET_SITE == const.DERIBIT:
        site = DeribitUiImpl(browser)
    elif variable.TARGET_SITE == const.BIEX:
        site = BiexUiImpl(browser)


def get_buy_price(which):
    try:
        if site is None:
            print('site is None')
            return -1
        return float(site.find_element_by_command(Command.BUY_PRICE, which).text)
    except Exception:
        return -1


def get_sell_price(which):
    try:
        if site is None:
            print('site is None')
            return -1
        return float(site.find_element_by_command(Command.SELL_PRICE, which).text)
    except Exception:
        return -1


def get_buy_amount(which):
    try:
        if site is None:
            print('site is None')
            return -1
        return float(site.find_element_by_command(Command.BUY_AMOUNT, which).text.replace(',', ''))
    except Exception:
        return -1


def get_sell_amount(which):
    try:
        if site is None:
            print('site is None')
            return -1
        return float(site.find_element_by_command(Command.SELL_AMOUNT, which).text.replace(',', ''))
    except Exception:
        return -1


def get_element(command):
    if site is None:
        print('site is None')
        return None
    return site.find_element_by_command(command)


class AbsUiData:
    def __init__(self, browser):
        self.browser = browser

    def find_element_by_command(self, command, which=None): pass


class BBXUiImpl(AbsUiData):

    def find_element_by_command(self, command, which=None):
        if command == Command.SELL_PRICE:
            which = 8 - which
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="__layout"]/div/div/div/div[2]/div[2]/div/ul[1]/li[' + which + ']/div/div[3]/p[1]')

        elif command == Command.SELL_AMOUNT:
            which = 8 - which
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="__layout"]/div/div/div/div[2]/div[2]/div/ul[1]/li[' + which + ']/div/div[3]/p[2]')

        elif command == Command.BUY_PRICE:
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="__layout"]/div/div/div/div[2]/div[2]/div/ul[2]/li[' + which + ']/div/div[3]/p[1]')

        elif command == Command.BUY_AMOUNT:
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="__layout"]/div/div/div/div[2]/div[2]/div/ul[2]/li[' + which + ']/div/div[3]/p[2]')


class DeribitUiImpl(AbsUiData):
    pass


class BiexUiImpl(AbsUiData):

    def find_element_by_command(self, command, which=None):
        if command == Command.SELL_PRICE:
            which = 8 - which
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="deepSellInner"]/div[' + which + ']/span[1]')

        elif command == Command.SELL_AMOUNT:
            which = 8 - which
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="deepSellInner"]/div[' + which + ']/span[2]')

        elif command == Command.BUY_PRICE:
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="deepBuy"]/div[' + which + ']/span[1]')

        elif command == Command.BUY_AMOUNT:
            which = str(which)
            return self.browser.find_element_by_xpath(
                '//*[@id="deepBuy"]/div[' + which + ']/span[2]')

        elif command == Command.BUY_BTN:
            return self.browser.find_element_by_xpath(
                '//*[@id="buyButton"]')

        elif command == Command.SELL_BTN:
            return self.browser.find_element_by_xpath(
                '//*[@id="sellButton"]')

        elif command == Command.PRICE_EDIT:
            return self.browser.find_element_by_xpath(
                '//*[@id="entrustPrice"]')

        elif command == Command.AMOUNT_EDIT:
            return self.browser.find_element_by_xpath(
                '//*[@id="entrustAmt"]')
