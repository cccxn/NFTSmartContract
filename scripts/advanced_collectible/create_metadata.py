from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri: dict[str, str] = {



}


def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        ipfs_url = 'http://127.0.0.1:5001'
        enpoint = '/api/v0/add'
        response = requests.post(ipfs_url + enpoint, files={'file': image_binary})
        ipfs_hash = response.json()['Hash']

        filename = filepath.split('/')[-1:][0]
        image_uri = f"""https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"""
        print(image_uri)
        return image_uri


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_iof_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"""You have created {number_iof_advanced_collectibles} collectibles!""")
    for token_id in range(number_iof_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (f"""./metadata{network.show_active()}/{token_id}-{breed}.json""")
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