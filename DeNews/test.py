from calendar import c
import json
from web3 import Web3
from solcx import compile_standard, install_solc
install_solc("0.8.0")
# url = "https://mainnet.infura.io/v3/5e23d056df8247cdbedc0a89a1c8040d"


# contract = web3.eth.contract(address=address,abi=abi)

# print(contract)

with open("../contracts/NewsFeed.sol", "r") as file:
    contact_list_file = file.read()
    # print(contact_list_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"NewsFeed.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["evm"]["bytecode"]["object"]
abi = abi = json.loads(compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["metadata"])["output"]["abi"]

# print(bytecode)
# print(abi)
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))
# print(web3)
address = "0x9E7D972391e460B1856576D91644d1c3Bd46a0bE"
check_add = web3.isChecksumAddress("0x9E7D972391e460B1856576D91644d1c3Bd46a0bE")
# abi = json.loads('''[=]''')
# print(address)
contract = web3.eth.contract(abi = abi,bytecode=bytecode)
print(contract)
nonce = web3.eth.getTransactionCount(address)
print(nonce)