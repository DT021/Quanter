import variable, const
from strategy.old_strategy import OldStrategy
from strategy.db_hedge_strategy import DBHedgeStrategy
from strategy.temp_biex_strategy import TempBiexStrategy

target_strategy = None


def get_strategy():
    global target_strategy
    if target_strategy is not None:
        return target_strategy

    if variable.TARGET_STRATEGY == const.STRATEGY_OLD:
        target_strategy = OldStrategy()
    elif variable.TARGET_STRATEGY == const.STRATEGY_DB_HEDGE:
        target_strategy = DBHedgeStrategy()
    elif variable.TARGET_STRATEGY == const.STRATEGY_TEMP_BIEX:
        target_strategy = TempBiexStrategy()

    if target_strategy is None:
        print('strategy init failed')
        return


def receive_price_change(buy_2_price, sell_2_price, ws_buy_1, ws_sell_1):
    strategy = get_strategy()
    if strategy is not None:
        strategy.on_price_change(sell_2_price, buy_2_price, ws_buy_1, ws_sell_1)
