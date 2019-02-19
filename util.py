import const
import datetime


def get_print_datetime():
    time = str(datetime.datetime.now())
    return time[11:-3]


def get_bm_ticker(_id):
    if _id == const.BTC or _id == const.BTC_REVERSE:
        return 'XBTUSD'
    elif _id == const.ETH or _id == const.ETH_REVERSE:
        return 'ETHUSD'
    else:
        return ''


def get_bbx_contract_id(_id):
    if _id == const.BTC:
        return 1
    elif _id == const.BTC_REVERSE:
        return 10
    elif _id == const.ETH:
        return 2


def get_biex_symbol(current_id):
    if current_id == const.BTC:
        return 'BTC2USDT_LSWAP'
    elif current_id == const.BTC_REVERSE:
        return 'BTC2USD_ISWAP'
    elif current_id == const.ETH:
        return 'ETH2USD_LSWAP'
    elif current_id == const.ETH_REVERSE:
        return 'ETH2USD_ISWAP'


def get_target_site_url(site, _id):
    if site == const.BBX:
        return 'https://swap.bbx.com/?id=' + str(_id)
    elif site == const.DERIBIT:
        return 'https://www.deribit.com/main#/futures?tab=BTC-PERPETUAL'
    elif site == const.BIEX:
        return 'https://www.biex.com/contract/trade?exchangePair=' + get_biex_symbol(_id)
