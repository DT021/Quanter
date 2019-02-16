class Position:
    _id = -1
    average_price = -1
    amount = -1
    side = None

    def copy(self):
        position = Position()
        position._id = self._id
        position.average_price = self.average_price
        position.amount = self.amount
        position.side = self.side
        return position

    def print(self):
        return [self.amount, self.side]
