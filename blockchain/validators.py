class Validators:
    def __init__(self):
        self.list = ["5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614"]

    def update(self, transaction):
        print(transaction)
        if transaction['output']['amount'] >= 25 and transaction['output']['to'] == "0":
            self.list.append(transaction['input']['from'])
            print("New Validator:", transaction['input']['from'])
            return True
        return False
