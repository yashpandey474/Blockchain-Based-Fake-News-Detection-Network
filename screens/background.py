from extra.config import START_TIME, BLOCK_VALIDATOR_CHOOSE_INTERVAL, PENALTY_NO_BLOCK
import time

# Background task that periodically checks if a block can be added


class Background:
    def __init__(self, p2pserver):
        self.time = None
        self.p2pserver = p2pserver

    def can_add_block(self, block):
        print("VOTES  = ", len(block.votes))
        print("PEERS = ", (self.p2pserver.accounts.get_count_of_validators()))

        return len(block.votes) >= (0.5 * self.p2pserver.accounts.get_count_of_validators())

    def run_forever(self):
        while True:
            current_time = int(time.time())
            time_elapsed = current_time - START_TIME.timestamp()

            if time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL == 0:
               
                # IF THERE WAS A RECEIVED BLOCK FROM PREVIOUS BLOCK PROPOSERR
                if self.p2pserver.received_block:
                    
                    # IF THE BLOCK HAD VOTES FROM MAJORITY
                    if self.can_add_block(self.p2pserver.received_block):
                        
                        print("RECEIVED BLOCK ADDED TO CHAIN\n")
                        
                        # ADD THE BLOCK TO THE BLOCKCHAIN
                        self.p2pserver.blockchain.append_block(
                            self.p2pserver.received_block,
                            self.p2pserver.transaction_pool,
                            self.p2pserver.accounts
                        )

                    else:
                        # PUNISH THE BLOCK PROPOSER FOR NO BLOCK!
                        self.p2pserver.accounts.reduce_balance(
                            self.p2pserver.block_proposer, PENALTY_NO_BLOCK, "RECEIVED BLOCK DID NOT GET ENOUGH VOTES")
                        print("As block proposer, your block didn't get enough votes\n")
                else:
                    if (self.p2pserver.transaction_pool.check_oldest_transaction(current_time-BLOCK_VALIDATOR_CHOOSE_INTERVAL)):
                        self.p2pserver.accounts.reduce_balance(
                            self.p2pserver.block_proposer, PENALTY_NO_BLOCK, "BLOCK PROPOSER DIDNT PROPOSE THE BLOCK IN TIME")
                        print("As block proposer, didn't propose a block in time\n")

                    else:
                        print(
                            "PROPOSER DIDNT GET ENOUGH TIME OR NO BLOCKS. NEXT CYCLE\n")
                # CHOOSE THE BLOCK PROPOSER AT THE START TO NOT HAVE DELAY BECAUSE OF APPENDING
                self.p2pserver.block_proposer = self.p2pserver.accounts.choose_validator(
                    current_time//10)

                # SET THE RECEIVED BLOCK TO NONE
                self.p2pserver.received_block = None

                # IF WAS ABLE TO CHOOSE A BLOCK PROPOSER
                if not self.p2pserver.block_proposer:
                    print("NO BLOCK PROPOSER CHOSEN.\n")

                # Wait for the next interval
                while int(time.time()) - START_TIME.timestamp() == time_elapsed:
                    time.sleep(0.1)  # Short sleep to prevent high CPU usage

            else:
                # Short sleep to prevent high CPU usage when not in the interval
                time.sleep(0.1)