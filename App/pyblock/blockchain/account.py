import random
import pyblock.config as config


class Account:
    def __init__(self, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        self.balance = balance
        self.isActive = True
        self.stake = stake
        self.clientPort = clientPort


class Accounts:
    def __init__(self):
        self.accounts = {}  # This will store address: Account mappings

    def initialize(self, address, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        if address not in self.accounts:
            self.accounts[address] = Account(
                balance=balance, stake=stake, clientPort=clientPort)

    def clientLeft(self, clientport):
        for address, account in self.accounts.items():
            if account.clientPort == clientport:
                account.isActive = False
                if account.stake is not None:
                    account.balance += account.stake
                account.clientPort = None
                break  # Assuming only one account can have this clientPort, we can break after finding it

    def get_account(self, address):
        return self.accounts.get(address)

    def get_balance(self, address):
        account = self.get_account(address)
        return account.balance if account else 0

    def get_stake(self, address):
        account = self.get_account(address)
        return account.stake if account else 0

    def makeAccountValidatorNode(self, address, stake):
        #IF ADDRESS IS NOT VALID
        if address not in self.accounts:
            raise ValueError("Account does not exist.")

        account = self.accounts[address]
        
        #IF NOT ENOUGH BALANCE
        if account.balance < stake:
            print("Insufficient balance to become a validator.")
        
        #IF NOT ENOUGH STAKE
        if stake < config.MIN_STAKE:
            print(f"Stake must be at least {config.MIN_STAKE} to become a validator.")

        #ADJUST BALANCE & STAKE OF ACCOUNT
        account.balance -= stake
        account.stake = stake

    def addANewClient(self, address, clientPort):
        if address in self.accounts:
            if self.accounts[address].isActive:
                raise ValueError(
                    "Client with this address already exists and is active.")

            else:
                self.accounts[address].isActive = True
                self.accounts[address].clientPort = clientPort

        self.initialize(address, clientPort=clientPort)

    def choose_validator(self, seed):
        # Filter out accounts with a stake less than the minimum stake
        eligible_accounts = {address: acc for address, acc in self.accounts.items(
        ) if acc.stake and acc.stake >= config.MIN_STAKE}

        if not eligible_accounts:
            return None

        sorted_accounts = sorted(eligible_accounts, key=lambda address: (
            eligible_accounts[address].stake, address))
        stakes = [eligible_accounts[address].stake for address in sorted_accounts]
        total_stake = sum(stakes)
        weights = [stake / total_stake for stake in stakes]
        random_generator = random.Random(seed)
        chosen_validator = random_generator.choices(
            sorted_accounts, weights=weights, k=1)[0]
        return chosen_validator

    def get_active_accounts(self, public_key):

        # Return a dictionary of accounts that have an active clientPort (i.e., are connected)
        active = {address: account for address, account in self.accounts.items(
        ) if account.isActive and address != public_key}
        # print("OWN: ", public_key)
        # print("ACTIVE: ", active.keys())

        return active

    def check_if_active(self, address):
        account = self.get_account(address)
        return account.isActive if account else False
