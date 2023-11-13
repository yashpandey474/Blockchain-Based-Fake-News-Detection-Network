import random
import pyblock.config as config


class Account:
    def __init__(self, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        self.balance = balance
        self.isActive = True
        self.stake = stake
        self.clientPort = clientPort
        self.sent_transactions = set()
        self.sent_blocks = set()


class Accounts:
    def __init__(self):
        self.accounts = {}  # This will store address: Account mappings
        # self.accounts[config.VM_PUBLIC_KEY] = Account(balance=50, stake = 0, clientPort=None)

    def initialize(self, address, balance=config.STARTING_BALANCE, stake=0, clientPort=None):
        if address not in self.accounts:
            self.accounts[address] = Account(
                balance=balance, stake=stake, clientPort=clientPort)

    def decrement_amount(self, address, amount):
        if (amount > self.accounts[address].balance):
            return False

        self.accounts[address].balance -= amount
        return True

    def send_amount(self, fromaddress, toaddress, amount):
        if (amount > self.accounts[fromaddress].balance):
            return False
        self.accounts[fromaddress].balance -= amount
        self.accounts[toaddress].balance += amount
        return True
    
    def add_sent_block(self, address, block):
        self.accounts[address].sent_blocks.add(block)
        
    def update_accounts(self, block):
        
        for transaction in block.transactions:
            #TRANSFER AMOUNT FROM SENDER OF NEWS TO VALIDATOR
            self.send_amount(
                transaction.sender_address,
                block.validator,
                transaction.fee
            )
            
        # CREATE TRANSACTIONS FOR REPUTATION CHANGE
        for news_transaction in block.transactions:
            #IF MAJORITY VOTED "TRUE"
            if len(news_transaction.positive_votes) > len(news_transaction.negative_votes):
                #IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score < 0.5:
                    #FOR THOSE THAT VOTED NEGATIVELY
                    for public_key in news_transaction.negative_votes:
                        #PENALISE BY % OF STAKE
                        self.accounts[public_key].stake -= (
                            self.accounts[public_key].stake*config.PENALTY_STAKE_PERCENT//100)
                        
            # IF MAJORITY VOTED "FAKE"
            if len(news_transaction.negative_votes) > len(news_transaction.positive_votes):
                # IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score >= 0.5:
                    # FOR THOSE THAT VOTED POSITIVELY
                    for public_key in news_transaction.positive_votes:
                        # PENALISE BY % OF STAKE
                        self.accounts[public_key].stake -= (
                            self.accounts[public_key].stake*config.PENALTY_STAKE_PERCENT//100)


                

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

    def get_sent_transactions(self, address):
        account = self.get_account(address)
        return account.sent_transactions if account else []
    
    def add_transaction(self, transaction):
        self.accounts[transaction.sender_address].sent_transactions.add(transaction)
        
    def makeAccountValidatorNode(self, address, stake):
        # IF ADDRESS IS NOT VALID
        if address not in self.accounts:
            raise ValueError("Account does not exist.")

        account = self.accounts[address]

        # IF NOT ENOUGH BALANCE
        if account.balance < stake:
            print("Insufficient balance to become a validator.")

        # IF NOT ENOUGH STAKE
        if stake < config.MIN_STAKE:
            print(
                f"Stake must be at least {config.MIN_STAKE} to become a validator.")

        # ADJUST BALANCE & STAKE OF ACCOUNT
        
        account.balance = account.balance - stake + account.stake
        account.stake = stake

    def addANewClient(self, address, clientPort, userType):
        if address in self.accounts:
            if self.accounts[address].isActive:
                raise ValueError(
                    "Client with this address already exists and is active.")

            else:
                self.accounts[address].isActive = True
                self.accounts[address].clientPort = clientPort

        self.initialize(address, clientPort=clientPort, balance = config.DEFAULT_BALANCE[userType])

    def choose_validator(self, seed=None):
        eligible_accounts = {address: acc for address, acc in self.accounts.items()
                             if acc.stake >= config.MIN_STAKE}

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

    # VERIFY EACH TRANSACTION'S SENDER HAS ENOUGH BALANCE FORR THE FEE
    def verify_transactions_balance(self, transactions):
        for transaction in transactions:
            # IF BALANCE NOT ENOUGH FOR FEE; RETURN FALSE
            if self.accounts[transaction.sender_address].balance < transaction.fee:
                return False

        return True
