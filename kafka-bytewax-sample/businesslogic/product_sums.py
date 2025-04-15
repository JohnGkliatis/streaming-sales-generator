from bytewax.operators import StatefulLogic

class SumLogic(StatefulLogic):
    def __init__(self):
        self.transactions = {}
        self.quantities = {}
        self.sales = {}

    def on_item(self, item):
        key = item["key"]
        temp = self.transactions.get(item["key"])
        if temp is None:
            temp = 0

        self.transactions[item["key"]] = sum + item["value"].transactions

        temp = self.quantities.get(item["key"])
        if temp is None:
            temp = 0

        self.quantities[item["key"]] = sum + item["value"].quantities

        temp = self.sales.get(item["key"])
        if temp is None:
            temp = 0

        self.sales[item["key"]] = sum + item["value"].sales

        return [
            (
                key,
                {
                    "transactions": self.transactions[key],
                    "quantities": self.quantities[key],
                    "sales": self.sales[key],
                },
            )
        ], False

    def snapshot(self):
        # Return the current state to be saved
        return (self.transactions, self.quantities, self.sales)

    def restore(self, snapshot):
        # Restore the state from the snapshot
        self.transactions, self.quantities, self.sales = snapshot