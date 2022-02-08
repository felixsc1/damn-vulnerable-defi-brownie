from brownie import (accounts, Wei, interface, PuppetPool, DamnValuableToken)

UNISWAP_INITIAL_TOKEN_RESERVE = Wei("10 ether")
UNISWAP_INITIAL_ETH_RESERVE = Wei("10 ether")

ATTACKER_INITIAL_TOKEN_BALANCE = Wei("1000 ether")
ATTACKER_INITIAL_ETH_BALANCE = Wei("25 ether")
POOL_INITIAL_TOKEN_BALANCE = Wei("100000")


def test_puppet_pool():

    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **

    deployer, attacker = accounts[0:2]

    token = DamnValuableToken.deploy({"from": deployer})

    token.transfer(ATTACKER_INITIAL_TOKEN_BALANCE)
    excess_balance = attacker.balance() - ATTACKER_INITIAL_ETH_BALANCE
    attacker.transfer(excess_balance, accounts[9])
