from brownie import network, AdvancedCollectible
import time
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only show for integration testing')

    # Act
    advanced_collectible, creation_txn = deploy_and_create()
    time.sleep(30)

    # Assert
    assert advanced_collectible.tokenCounter() == 1