# Damn Vulnerable DeFi

This is a fork of [damn vulnerable defi](https://github.com/tinchoabbate/damn-vulnerable-defi/tree/v2.0.0), an ethereum wargame consisting of a series of challenges in which DeFi smart contracts need to be hacked.

Here, I implemented everything in python / brownie instead of the javascript used in the original repo. It also contains my solutions (beware of spoilers).

See <https://www.damnvulnerabledefi.xyz/> for the descriptions of the challenges.

## Notes

- Challenges added and solved so far (more to follow):
    - #1 Unstoppable
    - #2 Naive Receiver
    - #3 Truster (shows how to call another function via the 'data' argument)
    - #4 Side Entrance (example of a reentrancy attack)
    - #5 The Rewarder (snapshots, timestamps)
    - #6 Selfie (governance contract)


- Make sure you have openzeppelin-contracts (4.4.2) imported via the brownie package manager.