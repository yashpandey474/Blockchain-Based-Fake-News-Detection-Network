import random
import pyblock.config as config


class Account:
    def __init__(self, balance=config.DEFAULT_BALANCE["Reader"], stake=0, clientPort=None):
        self.balance = balance
        self.isActive = True
        self.isValidator = False
        self.stake = stake
        self.clientPort = clientPort
        self.sent_transactions = set()
        self.sent_blocks = set()
        self.reputation_changes = []
        self.reputation_changes.append(("Assigned Initial Reputation", balance))

class Accounts:
    def __init__(self):
        self.accounts = {}

    def initialize(self, address, balance=config.DEFAULT_BALANCE["Reader"], stake=0, clientPort=None):
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
        
        self.log_reputation_change(toaddress, f"Transaction Fee Reward from {fromaddress}",  amount)
        self.accounts[fromaddress].balance -= amount
        self.accounts[toaddress].balance += amount
        return True

    def add_sent_block(self, address, block):
        self.accounts[address].sent_blocks.add(block)

    def update_accounts(self, block):
        # REWARD THE BLOCK PROPOSER AS BLOCK IS ACCEPTED
        self.accounts[block.validator].balance += config.BLOCK_REWARD
        
        #LOG THE CHANGE FOR BLOCK PROPSER
        self.log_reputation_change(block.validator, "Reward for Confirmed Proposed Block",  config.BLOCK_REWARD)
        
        #FOR EACH TRANSACTION; REWARD/PENALISE SENDERS AND VOTERS
        for news_transaction in block.transactions:
            #TRANSFER AMOUNT FROM SENDER OF NEWS TO VALIDATOR [REPUTATION CHANGE LOGGED IN FUNCTION]
            self.send_amount(
                news_transaction.sender_address,
                block.validator,
                news_transaction.fee
            )
            # IF NEWS WAS TRUE; REWARD SENDER
            if len(news_transaction.positive_votes) > len(news_transaction.negative_votes):
                self.accounts[news_transaction.sender_address].balance += config.SENDER_REWARD
                self.log_reputation_change(
                    news_transaction.sender_address, "News Broadcasted Voted True", config.SENDER_REWARD)
                
            else:
                # PERCENTAGE TO STOP RICH GETTING RICHER
                penalty_amount = self.accounts[news_transaction.sender_address].balance * config.SENDER_PENALTY_PERCENT//100
                
                self.accounts[news_transaction.sender_address].balance -= (
                    penalty_amount
                )
                
                print("BALANCE OF SENDER = ", self.accounts[news_transaction.sender_address].balance)
                
                self.log_reputation_change(
                    news_transaction.sender_address, "News Broadcasted Voted Fake",penalty_amount)
        
            #IF MAJORITY VOTED "TRUE"
            if len(news_transaction.positive_votes) > len(news_transaction.negative_votes):
                # IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score < 0.5:
                    
                    #FOR THOSE THAT VOTED NEGATIVELY
                    for public_key in news_transaction.negative_votes:
                        penalty_amount = self.accounts[public_key].stake*config.PENALTY_STAKE_PERCENT//100
                        #PENALISE BY % OF STAKE
                        self.accounts[public_key].stake -= (
                            penalty_amount)
                        #LOG REPUTATION CHANGE
                        self.log_reputation_change(
                            public_key, f"Penalty for Voting Against Majority on {news_transaction.id}",
                            -penalty_amount
                        )
            # IF MAJORITY VOTED "FAKE"
            if len(news_transaction.negative_votes) > len(news_transaction.positive_votes):
                # IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score >= 0.5:
                    # FOR THOSE THAT VOTED POSITIVELY
                    for public_key in news_transaction.positive_votes:
                        penalty_amount = self.accounts[public_key].stake*config.PENALTY_STAKE_PERCENT//100
                            
                        # PENALISE BY % OF STAKE
                        self.accounts[public_key].stake -= penalty_amount
                        
                        # LOG REPUTATION CHANGE
                        self.log_reputation_change(
                            public_key, f"Penalty for Voting Against Majority on {news_transaction.id}",
                            -penalty_amount
                        )

                

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
    
    def log_reputation_change(self, address, change_string, change_amount):
        self.accounts[address].reputation_changes.append((change_string, change_amount))
        
    def makeAccountValidatorNode(self, address, stake):
        # IF ADDRESS IS NOT VALID
        if address not in self.accounts:
            raise ValueError("Account does not exist.")

        account = self.accounts[address]
        
        account.isValidator = True

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
        print(f"Adding a new client {address} with clientPort {clientPort}")
        if address in self.accounts:
            if self.accounts[address].isActive:
                raise ValueError(
                    "Client with this address already exists and is active.")

            else:
                self.accounts[address].isActive = True
                self.accounts[address].clientPort = clientPort

        self.initialize(address, clientPort=clientPort,
                        balance=config.DEFAULT_BALANCE[userType])

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
