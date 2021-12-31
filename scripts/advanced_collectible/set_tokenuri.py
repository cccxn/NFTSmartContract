from enum import Enum
from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account


class BREED(Enum):
    PUG = 0
    SHIBA_INU = 1
    ST_BERNARD = 2


dog_metadata_dict_eden: dict[BREED, str] = {
    BREED.PUG: 'https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=0-PUG.json',
    BREED.SHIBA_INU: 'https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=1-SHIBA_INU.json',
    BREED.ST_BERNARD: 'https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=2-ST_BERNARD.json'
}
dog_metadata_dict: dict[str, str] = {
    BREED.PUG.name: 'https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=0-PUG.json',
    BREED.SHIBA_INU.name: 'https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=1-SHIBA_INU.json',
    BREED.ST_BERNARD.name: 'https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=2-ST_BERNARD.json'
}
BREED_MAPPING = {e.value: e.name for e in BREED}

def main():
    print(f"""Working on {network.show_active()}""")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"""You have {number_of_collectibles} tokenIDs""")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"""Setting tokenURI of {token_id}""")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dict)


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    txn = nft_contract.setTokenURI(token_id, tokenURI, {'from': account})
    txn.wait(1)
    print(f"""Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}""")
    print('Please wait up to 20 minutes, and hit the refresh metadata button')