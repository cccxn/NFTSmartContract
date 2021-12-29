from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    'hardhat', 'developmenet', 'ganache', 'ganache-local', 'mainnet-fork'
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: 'PUG', 1: 'SHIBU_INU', 3: 'ST_BERNARD'}

contract_to_mock = {'link_token': LinkToken, 'vrf_coordinator': VRFCoordinatorMock}


def get_breed(breed_number: int):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    if index is not None:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id is not None:
        return accounts.load(id)
    return accounts.add(config['wallets']['from_key'])


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"""The active network is {network.show_active()}""")
    print('Deploying mocks...')
    account = get_account()
    print('Deploying Mock LinkToken...')
    link_token = LinkToken.deploy({'form': account})
    print(f"""Link Token deployed to {link_token.address}""")
    print('Deploying Mock VRF Coordinator... ')
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {'from': account})
    print(f"""VRFCoordinator deployed to {vrf_coordinator}""")
    print('All done!')


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, 'ether')):
    account = get_account() if account is None else account
    link_token = get_account() if get_contract('link_token') is None else link_token
    funding_txn = link_token.transfer(contract_address, amount, {'from': account})
    funding_txn.wait(1)
    print(f"""Funded {contract_address}""")
    return funding_txn