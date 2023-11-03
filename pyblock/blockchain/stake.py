import pyblock.config as config
import random
 
class Stake:
    def __init__(self):
        self.balance = {"5aad9b5e21f63955e8840e8b954926c60e0e2d906fdbc0ce1e3afe249a67f614": 0}
        self.min_stake = config.MIN_STAKE
        
    def initialize(self, address, stake):
        if stake < self.min_stake:
            return False
        
        if address not in self.balance:
            self.balance[address] = stake

    def add_stake(self, from_address, amount):
        self.initialize(from_address)
        self.balance[from_address] += amount

    def get_balance(self, address):
        self.initialize(address)
        return self.balance[address]

    def choose_validator(self, seed):
        # Filter out addresses with a balance less than the minimum stake
        eligible_addresses = {address: balance for address, balance in self.balance.items() if balance >= self.min_stake}
        
        if not eligible_addresses:
            return None

        # Sort the addresses by their stake, and then by the address itself to ensure a deterministic order
        sorted_addresses = sorted(eligible_addresses, key=lambda address: (eligible_addresses[address], address))

        # Get the stakes for the sorted addresses
        stakes = [eligible_addresses[address] for address in sorted_addresses]
        total_stake = sum(stakes)

        # Normalize the stakes to sum to 1 for probability distribution
        weights = [stake / total_stake for stake in stakes]

        # Seed the random number generator
        random_generator = random.Random(seed)

        # Use random.choices to select an address based on the weighted distribution
        chosen_validator = random_generator.choices(sorted_addresses, weights=weights, k=1)[0]
        return chosen_validator

