import random
import pyblock.config as config


class Account:
    def __init__(self, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        self.balance = balance
        self.isActive = bool(clientPort)
        self.stake = stake
        self.clientPort = clientPort

class Accounts:
    def __init__(self):
        self.accounts = {}  # This will store address: Account mappings

    def initialize(self, address, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        if address not in self.accounts:
            self.accounts[address] = Account(balance=balance, stake=stake, clientPort=clientPort)

    def clientLeft(self, address):
        if address in self.accounts:
            account = self.accounts[address]
            account.isActive = False
            if account.stake is not None:
                account.balance += account.stake
            account.clientPort = None

    def get_account(self, address):
        return self.accounts.get(address)

    def get_balance(self, address):
        account = self.get_account(address)
        return account.balance if account else 0

    def get_stake(self, address):
        account = self.get_account(address)
        return account.stake if account else 0
    
    def makeAccountValidatorNode(self, address, stake):
        if address not in self.accounts:
            raise ValueError("Account does not exist.")
        
        account = self.accounts[address]
        if account.balance < stake:
            raise ValueError("Insufficient balance to become a validator.")
        if stake < config.MIN_STAKE:
            raise ValueError(f"Stake must be at least {config.MIN_STAKE} to become a validator.")

        account.balance -= stake
        account.stake = stake

    def becomeValidator(self, address, stake):
        self.makeAccountValidatorNode(address, stake)

    def addANewClient(self, address, clientPort):
        if address in self.accounts and self.accounts[address].isActive:
            raise ValueError("Client with this address already exists and is active.")
        self.initialize(address, clientPort=clientPort)

    def choose_validator(self, seed):
        # Filter out accounts with a stake less than the minimum stake
        eligible_accounts = {address: acc for address, acc in self.accounts.items() if acc.stake and acc.stake >= config.MIN_STAKE}

        if not eligible_accounts:
            return None

        sorted_accounts = sorted(eligible_accounts, key=lambda address: (eligible_accounts[address].stake, address))
        stakes = [eligible_accounts[address].stake for address in sorted_accounts]
        total_stake = sum(stakes)
        weights = [stake / total_stake for stake in stakes]
        random_generator = random.Random(seed)
        chosen_validator = random_generator.choices(sorted_accounts, weights=weights, k=1)[0]
        return chosen_validator
