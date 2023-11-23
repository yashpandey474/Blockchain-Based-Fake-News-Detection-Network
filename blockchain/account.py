import random
from blockchain.block import Block
import extra.config as config
import logging
from wallet.transaction import Transaction

# Setting up basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Account:
    def __init__(self, balance=config.DEFAULT_BALANCE["Reader"], stake=0, isValidator=False, clientPort=None, isActive=True, reputation_changes=None, sent_transactions=None, sent_blocks=None):
        self.balance = balance
        self.isValidator = isValidator
        self.isActive = isActive
        self.stake = stake
        self.clientPort = clientPort
        self.sent_transactions = sent_transactions if sent_transactions is not None else set()
        self.sent_blocks = sent_blocks if sent_blocks is not None else set()
        self.reputation_changes = reputation_changes if reputation_changes is not None else [
            ("Assigned Initial Reputation", balance)]

    def to_dict(self):
        return {
            "balance": self.balance,
            "isActive": self.isActive,
            "stake": self.stake,
            "clientPort": self.clientPort,
            "isValidator": self.isValidator,
            "sent_transactions": [tx.to_json() for tx in self.sent_transactions],
            "sent_blocks": [block.to_json()for block in self.sent_blocks],
            "reputation_changes": self.reputation_changes
        }


class Accounts:
    def __init__(self):
        self.accounts = {}

    def to_json(self):
        return {address: account.to_dict() for address, account in self.accounts.items()}

    def from_json(self, json_data):
        self.accounts = {}

        for address, account_data in json_data.items():
            serialized_transactions = account_data.get('sent_transactions', [])
            deserialized_transactions = [
                Transaction.from_json(tx_json) for tx_json in serialized_transactions]
            account_data['sent_transactions'] = set(deserialized_transactions)
            serialized_blocks = account_data.get("sent_blocks", [])
            deserialized_blocks = [Block.from_json(block) for block in serialized_blocks]
            account_data['sent_blocks'] = set(deserialized_blocks)
            self.accounts[address] = Account(**account_data)

    def initialize(self, address, balance=config.DEFAULT_BALANCE["Reader"], stake=0, clientPort=None):
        if address not in self.accounts:
            self.accounts[address] = Account(
                balance=balance, stake=stake, clientPort=clientPort)

    def reduce_balance(self, address, amount, reason):
        # Check if the decrement is successful
        if self.decrement_amount(address, amount):
            # Log the reputation change if the amount was successfully decremented
            self.log_reputation_change(address, reason, -amount)
        else:
            # Handle the case when decrement fails (e.g., due to insufficient balance)
            print(
                f"Failed to reduce balance for {address} due to insufficient funds.")

    def decrement_amount(self, address, amount):
        # Check if the account exists and has sufficient balance
        if address in self.accounts and amount <= self.accounts[address].balance:
            self.accounts[address].balance -= amount
            return True
        else:
            return False

    def send_amount(self, fromaddress, toaddress, amount):
        if (amount > self.accounts[fromaddress].balance):
            return False

        self.log_reputation_change(
            toaddress, f"Transaction Fee Reward from {fromaddress}",  amount)
        self.log_reputation_change(
            fromaddress, f"Transaction Fee deducted",  -amount)

        self.accounts[fromaddress].balance -= amount
        self.accounts[toaddress].balance += amount
        return True

    def add_sent_block(self, address, block):
        self.accounts[address].sent_blocks.add(block)

    def update_accounts(self, block):
        # REWARD THE BLOCK PROPOSER AS BLOCK IS ACCEPTED
        self.accounts[block.validator].balance += config.BLOCK_REWARD

        # LOG THE CHANGE FOR BLOCK PROPSER
        self.log_reputation_change(
            block.validator, "Reward for Confirmed Proposed Block",  config.BLOCK_REWARD)

        # FOR EACH TRANSACTION; REWARD/PENALISE SENDERS AND VOTERS
        for news_transaction in block.transactions:
            # TRANSFER AMOUNT FROM SENDER OF NEWS TO VALIDATOR [REPUTATION CHANGE LOGGED IN FUNCTION]
            self.send_amount(
                news_transaction.sender_address,
                block.validator,
                news_transaction.fee
            )
            # IF MAJORITY VOTED "TRUE"
            if len(news_transaction.positive_votes) > len(news_transaction.negative_votes):
                self.accounts[news_transaction.sender_address].balance += config.SENDER_REWARD
                self.log_reputation_change(
                    news_transaction.sender_address, "News Broadcasted Voted True", config.SENDER_REWARD)
                # IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score < 0.5:
                    # FOR THOSE THAT VOTED NEGATIVELY
                    for public_key in news_transaction.negative_votes:
                        penalty_amount = self.accounts[public_key].stake * \
                            config.PENALTY_STAKE_PERCENT//100
                        # PENALISE BY % OF STAKE
                        self.accounts[public_key].stake -= (
                            penalty_amount)
                        # LOG REPUTATION CHANGE
                        self.log_reputation_change(
                            public_key, f"Penalty for Voting Against Majority on {news_transaction.id}",
                            -penalty_amount
                        )
            # IF MAJORITY VOTED "FAKE"
            if len(news_transaction.negative_votes) > len(news_transaction.positive_votes):
                penalty_amount = self.accounts[news_transaction.sender_address].balance * config.SENDER_PENALTY_PERCENT//100

                self.accounts[news_transaction.sender_address].balance -= (
                    penalty_amount
                )

                self.log_reputation_change(
                    news_transaction.sender_address, "News Broadcasted Voted Fake", -penalty_amount)

                # IF MODEL AGREED WITH MAJORITY
                if news_transaction.model_score >= 0.5:
                    # FOR THOSE THAT VOTED POSITIVELY
                    for public_key in news_transaction.positive_votes:
                        penalty_amount = self.accounts[public_key].stake * \
                            config.PENALTY_STAKE_PERCENT//100

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
        self.accounts[transaction.sender_address].sent_transactions.add(
            transaction)

    def log_reputation_change(self, address, change_string, change_amount):
        self.accounts[address].reputation_changes.append(
            (change_string, change_amount))

        # self.accounts[address].reputation_changes[change_string] = change_amount

    def makeAccountValidatorNode(self, address, stake):
        # IF ADDRESS IS NOT VALID
        if address not in self.accounts:
            raise ValueError("Account does not exist.")

        account = self.accounts[address]

        # IF NOT ENOUGH BALANCE
        if account.balance < stake:
            raise ValueError("Insufficient balance to become a validator.")

        # IF NOT ENOUGH STAKE
        if stake < config.MIN_STAKE:
            raise ValueError(
                f"Stake must be at least {config.MIN_STAKE} to become a validator.")

        # ADJUST BALANCE & STAKE OF ACCOUNT
        account.balance = account.balance - stake + account.stake
        account.stake = stake
        account.isValidator = True
        print(f"Account is now a validator node {account.isValidator}")

    def addANewClient(self, address, clientPort, userType):
        print(f"Adding a new client {address} with clientPort {clientPort}")
        if address in self.accounts:
            if self.accounts[address].isActive:
                raise ValueError(
                    "Client with this address already exists and is active.")

            else:
                #MAKE HIM ACTIVE AND SET THE CLIENT PORT
                self.accounts[address].isActive = True
                self.accounts[address].clientPort = clientPort

        #INITIALISE THE ACCOUNT
        self.initialize(address, clientPort=clientPort,
                        balance=config.DEFAULT_BALANCE[userType])

    def choose_validator(self, seed=None):
        """
        Selects a validator from the list of eligible accounts based on their stake.

        Parameters:
        - seed (Optional[int]): An optional seed for the random number generator to ensure reproducibility.

        Returns:
        - str: The address of the chosen validator.

        Raises:
        - ValueError: If no eligible validators are available.
        """
        try:
            # Filter accounts eligible for validation based on minimum stake and isValidator flag
            eligible_accounts = {address: acc for address, acc in self.accounts.copy().items()
                                 if acc.stake >= config.MIN_STAKE and acc.isValidator and acc.isActive}
            print(f"Accounts: {self.accounts}")
            if len(eligible_accounts) == 0:
                print("No eligible validators available.")
                return None
            print(f"Seed used {seed}")
            print(f"Eligible validators: {eligible_accounts}")

            # Sort accounts by stake
            sorted_accounts = sorted(
                eligible_accounts.items(), key=lambda a: a[1].stake)

            # Calculate the total stake and weights for each eligible account
            stakes = [account.stake for address, account in sorted_accounts]
            total_stake = sum(stakes)
            weights = [stake / total_stake for stake in stakes]

            # Use a random generator for selection
            random_generator = random.Random(seed)
            chosen_validator = random_generator.choices(
                sorted_accounts, weights=weights, k=1)[0][0]

            print(
                f"Chosen validator: {self.accounts[chosen_validator].clientPort}")
            return chosen_validator
        except Exception as e:
            logging.error(f"Error in choosing validator: {e}")
            raise ValueError("Error in selecting validator") from e

    # VERIFY EACH TRANSACTION'S SENDER HAS ENOUGH BALANCE FORR THE FEE

    def verify_transactions_balance(self, transactions):
        for transaction in transactions:
            # IF BALANCE NOT ENOUGH FOR FEE; RETURN FALSE
            if self.accounts[transaction.sender_address].balance < transaction.fee:
                return False

        return True

    def make_inactive(self, address):
        if (address in self.accounts):
            print(f"Making {address} inactive in accounts")
            self.accounts[address].isActive = False
            return True

    def get_count_of_validators(self):
        count = 0
        for address, account in self.accounts.copy().items():
            if account.isValidator and account.isActive:
                count += 1
        return count