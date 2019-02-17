class AbsApi:
    callbacks = []

    def get_user_position(self): pass

    def open_order(self, price, amount, side): pass

    def close_order(self, price, amount, side, _id): pass

    def cancel_order(self, order_id): pass

    def get_order_info(self, order_id): pass

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def send_callback(self):
        for callback in self.callbacks:
            callback()
