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

news_bytecode = compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["evm"]["bytecode"]["object"]
abi_news = json.loads(compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["metadata"])["output"]["abi"]
abi_acc = json.loads(compiled_sol["contracts"]["NewsFeed.sol"]["Accounts"]["metadata"])["output"]["abi"]
acc_bytecode = compiled_sol["contracts"]["NewsFeed.sol"]["Accounts"]["evm"]["bytecode"]["object"]

# print(bytecode)
# print(abi)
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))
# print(web3)
address = "0xf568C8059Ea2a38B9693E5f77902699AaE0e8886"
check_add = web3.isChecksumAddress("0x9E7D972391e460B1856576D91644d1c3Bd46a0bE")


AccContract = web3.eth.contract(abi = abi_acc,bytecode=acc_bytecode)
print(AccContract)
print(abi_acc)
# print(NewsContract.functions.storedValue().call())

acc_tx_hash = AccContract.constructor().transact(transaction={'from': web3.eth.accounts[0]})
print(acc_tx_hash)

acc_tx_receipt = web3.eth.wait_for_transaction_receipt(acc_tx_hash)
account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
# news.functions.greet().call()
# print(tx_receipt)
print(account)
acc_address = acc_tx_receipt.contractAddress
account.functions.accountAddRole(web3.eth.accounts[1],2).transact(transaction={'from': web3.eth.accounts[0]})

print(account.functions.accountHasRole(web3.eth.accounts[1],2).call())


NewsContract = web3.eth.contract(abi = abi_news,bytecode=news_bytecode)
print(NewsContract)
nonce = web3.eth.getTransactionCount(address)
print(nonce)
print(web3.eth.accounts)
chain_id = 1337
address = "0xf568C8059Ea2a38B9693E5f77902699AaE0e8886"

bal = web3.eth.get_balance(address)
print(web3.fromWei(bal, 'ether'))

tx_hash = NewsContract.constructor(acc_address).transact(transaction={'from': web3.eth.accounts[1]})
# print(tx_hash)

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
news.functions.addNews("hasjkdhkas","hasjhjkasdnj").transact(transaction={'from': web3.eth.accounts[1],"value": 5})
# print(tx_receipt)
# print(news)
print(news.functions.newsCount().call())
