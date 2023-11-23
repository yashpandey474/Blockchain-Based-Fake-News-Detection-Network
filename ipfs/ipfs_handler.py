import requests
import uuid


class IPFSHandler:

    base_url = "https://api.web3.storage"
    auth = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk0Nzk1MzBmMTFkMmI0MWE5NTFlNjA0NjhlN0M5OTc3ZmVCYjQ2QTgiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2OTc1Nzc4MTkzOTYsIm5hbWUiOiJibG9ja2NoYWlucHJvamVjdCJ9.ibPZ2NWkxew2CwI0xfL3-RIq4ctds95RIexDk__uL_U"
    }

    @staticmethod
    def put_to_ipfs(content):
        # putting data to IPFS and returns a ipfs address
        url = f"{IPFSHandler.base_url}/upload"
        files = {"file": content}
        print(content)

        try:
            res = requests.post(url, files=files, headers=IPFSHandler.auth)
            return res.json()["cid"]
        except Exception as e:
            print(e)
            return ""

        # try:
        #     print(res.json())
        #     ipfs_address = res.json()["cid"]
        # except Exception as e:
        #     print("Error: ", e)
        #     return ""

        # '''{'cid': 'bafkreidb6otjwgl5xuwbzzixoc7oz5maojjpj7sfuzrobyawiafwxeo524',
        #     'carCid': 'bagbaieragbvch2fxvhiir3bxiidxa7fxrr5cgobtyqq6o6dy3nnjezbijera'}'''
        # return "bafkreidb6otjwgl5xuwbzzixoc7oz5maojjpj7sfuzrobyawiafwxeo524"

    @staticmethod
    def get_from_ipfs(ipfs_address):
        # fetching from IPFS and returns data
        try:
            res = requests.get(
                f"https://{ipfs_address}.ipfs.dweb.link", headers=IPFSHandler.auth)
            return res.text
        except Exception as e:
            print(e)
            return ""

        return res.text

        # # RETURN DEMO TEXT
        # with open("nan.txt", "r") as file:
        #     file_content = file.read()
        #     return file_content

        # return """nan
# Did they post their votes for Hillary already?"""


if __name__ == "__main__":
    ipfs_address = 'bafkreig5stfj2plvltwxi7cl3hbknde2a2nyuf5kpheinzkcmiid43mutq'
    print(ipfs_address)
    print(IPFSHandler.get_from_ipfs(ipfs_address))
