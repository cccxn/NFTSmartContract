NFT Smart Contracts
-------------------

Initial Set-Up
==============
- Skip
    - brownie bake nft-mix ;
- brownie init ;
- git init ;
- touch README.rst ;
- git add .gitattributes .gitignore README.rst ;
- git commit -m "Initial Commit" . ;
- git branch -M master ;
- git remote add origin https://github.com/XXXXXX/NFTSmartContract.git ;

NFT Framework
=============
- brownie compile ;
- brownie run scripts/simple_collectible/deploy_and_create.py ;


Notes
=====
#. We didn't upload an image to IPFS ourselves
#. Why is IPFS decentralized?
#. Anyone can mint an NFT here - not verifiably scarce or random


Test
====
 - brownie test -k test_can_create_advanced_collectible ;
 - brownie test -k test_can_create_advanced_collectible_integration --network rinkeby

IPFS
====
#. Download and install IPFS from:
    - https://docs.ipfs.io/install/command-line/#official-distributions
#. Run the IPFS Daemon using:
    - ipfs init ;
    - ipfs daemon ;