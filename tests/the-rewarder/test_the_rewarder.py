from brownie import (accounts, Wei, chain, AccountingToken,
                     FlashLoanerPool, RewardToken, TheRewarderPool, DamnValuableToken, AttackTheRewarder)

TOKENS_IN_LENDER_POOL = Wei('1000000 ether')


def test_the_rewarder():

    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **
    deployer, alice, bob, charlie, david, attacker = accounts[0:6]
    users = [alice, bob, charlie, david]

    # accounting_token = AccountingToken.deploy({"from": deployer})
    liquidity_token = DamnValuableToken.deploy({"from": deployer})
    # eward_troken = RewardToken.deploy({"from": deployer})
    flash_loaner_pool = FlashLoanerPool.deploy(
        liquidity_token.address, {"from": deployer})
    the_rewarder_pool = TheRewarderPool.deploy(
        liquidity_token.address, {"from": deployer})

    liquidity_token.transfer(flash_loaner_pool.address,
                             TOKENS_IN_LENDER_POOL, {"from": deployer})

    accounting_token = AccountingToken.at(the_rewarder_pool.accToken())
    reward_token = RewardToken.at(the_rewarder_pool.rewardToken())

    # Alice, Bob, Charlie and David deposit 100 liquidity tokens to the rewarder pool each
    amount = Wei('100 ether')
    for user in users:
        liquidity_token.transfer(user, amount, {"from": deployer})
        liquidity_token.approve(
            the_rewarder_pool.address, amount, {"from": user})
        the_rewarder_pool.deposit(amount, {"from": user})
        # they should have received the corresponding amount of accounting tokens
        assert accounting_token.balanceOf(user) == amount

    # Advance time 5 days so that depositors can get rewards
    chain.sleep(5*24*60*60)
    # chain.mine(1)   # block.time only gets affected with the next transaction or mined block

    # each user gets reward = deposit * 100 / total deposits  = 25 tokens
    for user in users:
        the_rewarder_pool.distributeRewards({"from": user})
        assert reward_token.balanceOf(user) == Wei('25 ether')
    assert reward_token.totalSupply() == Wei('100 ether')
    assert the_rewarder_pool.roundNumber() == 2

    # ** CODE YOUR EXPLOIT HERE **

    # not solved yet ....
    chain.sleep(5*24*60*60)
