from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account, get_breed
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local tetsing")

    # Act
    advacned_collectible, create_txn = deploy_and_create()
    requestId = create_txn.events['requestedCollectible']['requestId']
    random_number = 777
    get_contract('vrf_coordinator').callBackWithRandomness(
        requestId, random_number, advacned_collectible.address, {'from': get_account()}
    )

    # Assert
    assert advacned_collectible.tokenCounter() == 1
    assert advacned_collectible.tokenIdToBreed(0) == random_number % 3


def test_get_breed():
    # Arrange/Act
    breed = get_breed(0)
    assert breed == 'PUG'
