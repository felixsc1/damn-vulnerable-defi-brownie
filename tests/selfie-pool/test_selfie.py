from brownie import (accounts, Wei, SelfiePool,
                     SimpleGovernance, DamnValuableTokenSnapshot)


TOKEN_INITIAL_SUPPLY = Wei("2000000 ether")
TOKENS_IN_POOL = Wei("1500000 ether")

# ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **


def test_selfie():

    deployer, attacker = accounts[0:2]

    token = DamnValuableTokenSnapshot.deploy(
        TOKEN_INITIAL_SUPPLY, {"from": deployer})
    governance = SimpleGovernance.deploy(token.address, {"from": deployer})
    pool = SelfiePool.deploy(
        token.address, governance.address, {"from": deployer})

    token.transfer(pool.address, TOKENS_IN_POOL)


# ** CODE YOUR EXPLOIT HERE **


# ** SUCCESS CONDITIONS **

assert token.balanceOf(attacker) == TOKENS_IN_POOL
