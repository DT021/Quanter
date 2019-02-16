from strategy.base_strategy import AbsStrategy


class HedgeStrategy(AbsStrategy):

    def on_price_change(self, sell_2, buy_2):
        pass