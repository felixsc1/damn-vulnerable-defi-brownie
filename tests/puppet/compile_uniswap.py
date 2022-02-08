from brownie import interface
from solcx import compile_standard


def main():

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                    }
                }
            }
        },
        solc_version="0.6.0",
    )
