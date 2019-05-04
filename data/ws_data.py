import data.huobi_data as huobi
import data.bitmex_data as bitmex
import data.binance_ui_data as binance_ui
import data.binance_data as binance
import data.okex_data as okex
import variable, const


def get_source():
    if variable.WS_SOURCE == const.WS_SOURCE_BITMEX:
        return bitmex
    elif variable.WS_SOURCE == const.WS_SOURCE_HUOBI:
        return huobi
    elif variable.WS_SOURCE == const.UI_SOURCE_BINANCE:
        return binance_ui
    elif variable.WS_SOURCE == const.WS_SOURCE_BINANCE:
        return binance
    elif variable.WS_SOURCE == const.WS_SOURCE_OKEX:
        return okex
