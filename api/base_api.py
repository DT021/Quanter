class AbsApi:
    callbacks = []

    def get_position(self): pass

    def open_order(self, price, amount, side): pass

    def close_order(self, price, amount, side, _id): pass

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def send_callback(self):
        for callback in self.callbacks:
            callback()
