class Position:
    position_id = -1
    average_price = -1
    amount = -1
    side = None

    def copy(self):
        position = Position()
        position.position_id = self.position_id
        position.average_price = self.average_price
        position.amount = self.amount
        position.side = self.side
        return position

    def value(self):
        return [self.average_price, self.amount, self.side]
