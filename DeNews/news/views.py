import imp
from django.shortcuts import render
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
install_solc("0.8.0")

# Create your views here.
with open("../contracts/NewsFeed.sol", "r") as file:
    contact_list_file = file.read()

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

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

news_bytecode = compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["evm"]["bytecode"]["object"]
abi_news = json.loads(compiled_sol["contracts"]["NewsFeed.sol"]["NewsFeed"]["metadata"])["output"]["abi"]
abi_acc = json.loads(compiled_sol["contracts"]["NewsFeed.sol"]["Accounts"]["metadata"])["output"]["abi"]
acc_bytecode = compiled_sol["contracts"]["NewsFeed.sol"]["Accounts"]["evm"]["bytecode"]["object"]

address = "0xf568C8059Ea2a38B9693E5f77902699AaE0e8886"

url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))

NewsContract = web3.eth.contract(abi = abi_news,bytecode=news_bytecode)
AccContract = web3.eth.contract(abi = abi_acc,bytecode=acc_bytecode)

acc_tx_hash = AccContract.constructor().transact(transaction={'from': web3.eth.accounts[0]})
acc_tx_receipt = web3.eth.wait_for_transaction_receipt(acc_tx_hash)

news_tx_hash = NewsContract.constructor(acc_tx_receipt.contractAddress).transact(transaction={'from': web3.eth.accounts[1]})
tx_receipt = web3.eth.wait_for_transaction_receipt(news_tx_hash)


def home(request):
    context = {}
    context['address'] = address

    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)

    account.functions.accountAddRole(web3.eth.accounts[1],2).transact(transaction={'from': web3.eth.accounts[0]})
    print(account.functions.accountHasRole(web3.eth.accounts[1],2).call())
    
    # news.functions.addNews("hasjkdhkas","hasjhjkasdnj").transact(transaction={'from': web3.eth.accounts[1],"value": 5})

    
    news_feed=[]
    news_count = news.functions.newsCount().call()
    print(news_count)
    news_feed.append(news.functions.getFeed().call())
    news_feed=news_feed[0]
    print(news_feed)
    # for i in range(news_count):
    role = []
     

    context['acc_tx'] = acc_tx_receipt
    context['news_tx'] = tx_receipt
    context['news_count'] = news_count
    context['news_feed'] = news_feed
    context['news_role'] 
    if(request.method=="POST"):
        title=request.POST.get('title')
        description=request.POST.get('description')
        news.functions.addNews(title,description).transact(transaction={'from': web3.eth.accounts[1],"value": 5})
        return render(request,'home.html',context)
    return render(request,'home.html',context)

