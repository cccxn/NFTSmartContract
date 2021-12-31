from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
from enum import Enum
import requests
import json
import os


def upload_to_ipfs(filepath):
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with filepath.open('rb') as fp:
        image_binary = fp.read()
        ipfs_url = 'http://127.0.0.1:5001'
        endpoint = '/api/v0/add'
        response = requests.post(ipfs_url + endpoint, files={'file': image_binary})
        ipfs_hash = response.json()['Hash']

        # filename = filepath.split('/')[-1:][0]
        filename = filepath.name
        image_uri = f"""https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"""
        print(image_uri)
        return image_uri


# import sys
# import os
# # sys.path.append('./metadata')
# # from sample_metadata import metadata_template
# from pathlib import Path
# from enum import Enum
#
# if Path(".").resolve().parent.stem == 'ProjectSmartContract':
#     PROJECT_PATH = Path(".").resolve().parent
# else:
#     PROJECT_PATH = Path(".").resolve()
#
# PROJECT_NFT = Path(PROJECT_PATH, 'NFTSmartContract')
# PROJECT_IMG = Path(PROJECT_NFT, 'img')
# PROJECT_MD = Path(PROJECT_NFT, 'metadata')
# PROJECT_RINKEBY = Path(PROJECT_MD, 'rinkeby')
#
#
class BREED(Enum):
    PUG = 0
    SHIBA_INU = 1
    ST_BERNARD = 2
#
# BREED_MAPPING = {e.value: e.name for e in BREED}
#
#
#
breed_to_image_uri: dict[BREED, str] = {
    BREED.PUG: 'https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png',
    BREED.SHIBA_INU: 'https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png',
    BREED.ST_BERNARD: 'https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png'
}
#
# def get_breed(breed_number: int):
#     return BREED_MAPPING[breed_number]
#
# token_id = 0
# breed = BREED.ST_BERNARD
# tmp_file_name = f"""{token_id}-{breed.name}.json"""
# metadata_file_name = Path(PROJECT_RINKEBY, tmp_file_name)
# collectible_metadata = metadata_template
# if metadata_file_name.exists():
#     print(f"""{metadata_file_name} already exists! Delete if to overwrite""")
# else:
#     print(f"""Creating Metadata file: {metadata_file_name}""")
#     collectible_metadata['name'] = breed.name
#     collectible_metadata['description'] = f"""An adorable {breed.name} pup!"""
#     image_path = Path(PROJECT_IMG, breed.name.lower().replace('_', '-') + '.png')
#     image_uri = None
#     if os.getenv('UPLOAD_IPFS') == 'true':
#         image_uri = upload_to_ipfs(image_path)
#     image_uri = breed_to_image_uri[breed] if image_uri is None else image_uri
#
#     collectible_metadata['image'] = image_uri
#     with open(metadata_file_name, 'w') as file:
#         json.dump(collectible_metadata, file)
#     if os.getenv('UPLOAD_IPFS') == 'true':
#         upload_to_ipfs(metadata_file_name)



def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"""You have created {number_of_advanced_collectibles} collectibles!""")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"""./metadata/{network.show_active()}/{token_id}-{breed}.json"""
        print(metadata_file_name)
        collectible_metadata = metadata_template

        if Path(metadata_file_name).exists():
            print(f"""{metadata_file_name} already exists! Delete if to overwrite""")
        else:
            print(f"""Creating Metadata file: {metadata_file_name}""")
            collectible_metadata['name'] = breed
            collectible_metadata['description'] = f"""An adorable {breed} pup!"""
            image_path = './img/' + breed.lower().replace('_', '-') + '.png'

            image_uri = None
            if os.getenv('UPLOAD_IPFS') == 'true':
                image_uri = upload_to_ipfs(image_path)
            image_uri = breed_to_image_uri[breed] if image_uri is None else image_uri

            collectible_metadata['image'] = image_uri
            with open(metadata_file_name, 'w') as file:
                json.dump(collectible_metadata, file)
            if os.getenv('UPLOAD_IPFS') == 'true':
                upload_to_ipfs(metadata_file_name)