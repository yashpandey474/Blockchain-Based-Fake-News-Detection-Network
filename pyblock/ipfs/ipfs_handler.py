class IPFSHandler:
    @staticmethod
    def put_to_ipfs(data):
        # Simulates putting data to IPFS and returns a dummy address
        return f"ipfs://dummy_address/{hash(data)}"

    @staticmethod
    def get_from_ipfs(ipfs_address):
        # Simulates fetching from IPFS and returns dummy data
        return f"Data for address: {ipfs_address}"
