class Stake:
    def __init__(self):
        self.addresses = ["5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614"]
        self.balance = {"5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614": 0}

    def initialize(self, address):
        if address not in self.balance:
            self.balance[address] = 0
            self.addresses.append(address)

    def add_stake(self, from_address, amount):
        self.initialize(from_address)
        self.balance[from_address] += amount

    def get_balance(self, address):
        self.initialize(address)
        return self.balance[address]

    def get_max(self, addresses):
        max_balance = -1
        leader = None
        for address in addresses:
            if self.get_balance(address) > max_balance:
                leader = address
        return leader

    def update(self, transaction):
        amount = transaction['output']['amount']
        from_address = transaction['input']['from']
        self.add_stake(from_address, amount)
