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


def get_common_symbol(_id):
    if _id == const.BTC or _id == const.BTC_REVERSE:
        return 'BTCUSD'
    elif _id == const.ETH or _id == const.ETH_REVERSE:
        return 'ETHUSD'
    elif _id == const.EOS or _id == const.EOS_REVERSE:
        return 'EOSUSD'
    else:
        return ''


def get_bfx_symbol(_id):
    if _id == const.OKB:
        return 'okb'
    elif _id == const.BTC or _id == const.BTC_REVERSE:
        return 'btc'
    else:
        return ''


def get_okex_symbol(_id):
    if _id == const.BTC or _id == const.BTC_REVERSE:
        return 'BTC-USDT'
    elif _id == const.ETH or _id == const.ETH_REVERSE:
        return 'ETH-USDT'
    elif _id == const.EOS or _id == const.EOS_REVERSE:
        return 'EOS-USDT'
    elif _id == const.OKB:
        return 'OKB-USDT'
    else:
        return ''


def get_huobi_binance_symbol(_id):
    if _id == const.BTC or _id == const.BTC_REVERSE:
        return 'btcusdt'
    elif _id == const.ETH or _id == const.ETH_REVERSE:
        return 'ethusdt'
    elif _id == const.EOS or _id == const.EOS_REVERSE:
        return 'eosusdt'
    elif _id == const.ETC:
        return 'etcusdt'
    else:
        return ''


def get_target_site_url(site, _id):
    if site == const.BBX:
        return 'https://swap.bbx.com/?id=' + str(_id)
    elif site == const.DERIBIT:
        return 'https://www.deribit.com/main#/futures?tab=BTC-PERPETUAL'
    elif site == const.BIEX:
        return 'https://www.biex.com/contract/trade?exchangePair=' + get_biex_symbol(_id)
    elif site == const.BYBIT:
        return 'https://www.bybit.com/app/exchange/' + get_common_symbol(_id)
    elif site == const.TDEX:
        return 'https://www.tdex.com/trade/BTCUSD'
    elif site == const.BFX:
        return 'https://www.bfx.nu/trade/trade.do?transactionType=12'
