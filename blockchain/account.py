#TODO: check this
class Account:
    def __init__(self):
        self.addresses = ["5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614"]
        self.balance = {"5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614": 1000}

    def initialize(self, address):
        if address not in self.balance:
            self.balance[address] = 0
            self.addresses.append(address)

    def transfer(self, from_address, to_address, amount):
        self.initialize(from_address)
        self.initialize(to_address)
        self.increment(to_address, amount)
        self.decrement(from_address, amount)

    def increment(self, to_address, amount):
        self.balance[to_address] += amount

    def decrement(self, from_address, amount):
        self.balance[from_address] -= amount

    def get_balance(self, address):
        self.initialize(address)
        return self.balance[address]

    def update(self, transaction):
        amount = transaction['output']['amount']
        from_address = transaction['input']['from']
        to_address = transaction['output']['to']
        self.transfer(from_address, to_address, amount)

    def transfer_fee(self, block, transaction):
        amount = transaction['output']['fee']
        from_address = transaction['input']['from']
        to_address = block['validator']
        self.transfer(from_address, to_address, amount)
