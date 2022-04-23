from audioop import add
from django.shortcuts import redirect, render
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib import messages
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

# address = "0xf568C8059Ea2a38B9693E5f77902699AaE0e8886"


url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))
address =  web3.eth.accounts[1]
NewsContract = web3.eth.contract(abi = abi_news,bytecode=news_bytecode)
AccContract = web3.eth.contract(abi = abi_acc,bytecode=acc_bytecode)

acc_tx_hash = AccContract.constructor().transact(transaction={'from': web3.eth.accounts[0]})
acc_tx_receipt = web3.eth.wait_for_transaction_receipt(acc_tx_hash)

news_tx_hash = NewsContract.constructor(acc_tx_receipt.contractAddress).transact(transaction={'from': web3.eth.accounts[1]})
tx_receipt = web3.eth.wait_for_transaction_receipt(news_tx_hash)





def index(request):
    if request.method=="POST":
        address = request.POST.get('address')
        # news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
        account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
        is_reader = account.functions.accountHasRole(address,0).call()
        is_validator = account.functions.accountHasRole(address,1).call()
        is_publisher = account.functions.accountHasRole(address,2).call()

        if(is_reader):
            return redirect("reader")
        if(is_validator):
            return redirect("validator")
        if(is_publisher):
            return redirect("publisher")

        return redirect("creator")

    return render(request,"signin.html")



def home(request):
    context = {}
    context['address'] = address

    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)

    account.functions.accountAddRole(web3.eth.accounts[1],2).transact(transaction={'from': web3.eth.accounts[0]})
    print(account.functions.accountHasRole(web3.eth.accounts[1],2).call())
    
    # news.functions.addNews("hasjkdhkas","hasjhjkasdnj").transact(transaction={'from': web3.eth.accounts[1],"value": 5})

    
    news_feed=[]
    all_news=[]
    news_count = news.functions.newsCount().call()
    print(news_count)
    for i in range(news_count):
        all_news.append(news.function.news_feed(i+1).call())
    news_feed.append(news.functions.getFeed().call())
    news_feed=news_feed[0]
    print(news_feed)
    # for i in range(news_count):
    role = []

    is_validator=account.functions.accountHasRole(address,1).call()
    context['acc_tx'] = acc_tx_receipt
    context['news_tx'] = tx_receipt
    context['news_count'] = news_count
    context['news_feed'] = news_feed
    context['is_validator'] = is_validator 
    # context['news']
    print(is_validator)
    # context['news_role'] 
    if(request.method=="POST"):
        title=request.POST.get('title')
        description=request.POST.get('description')
        news.functions.addNews(title,description).transact(transaction={'from': web3.eth.accounts[1],"value": 5})
        return render(request,'home.html',context)
    return render(request,'home.html',context)

def createNews(request):
    context = {}
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    if(request.method=="POST"):
        title=request.POST.get('title')
        description=request.POST.get('description')
        account.functions.accountAddRole(web3.eth.accounts[1],2).transact(transaction={'from': web3.eth.accounts[0]})
        print(account.functions.accountHasRole(web3.eth.accounts[1],2).call())
        # news.functions.addNews(title,description).transact(transaction={'from': web3.eth.accounts[1],"value": 6})
        if account.functions.accountHasRole(web3.eth.accounts[1],2).call():
            news.functions.addNews(title,description).transact(transaction={'from': web3.eth.accounts[1],"value": 5})
            messages.success(request,"News added successfully with 5 ether stake")
        else:
            messages.warning(request,"Insufficient Permission")
        return redirect('publisher')
    news_count = news.functions.newsCount().call()
    print(news_count)
    return render(request,'create_news.html')

def validation_news(request):
    context= {}
    global address
    context['address']=address
    print(address)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)

    news_to_valid=news.functions.assignedArticle(address).call()

    context['news']=news_to_valid
    print(news_to_valid[0])
    context['news_id']=news_to_valid[0]
    return render(request,'news_to_valid.html',context=context)

def assign_role(request):
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    if(request.method=="POST"):
        address=request.POST.get('account')
        print(address)
        role=request.POST.get('role')
        role=int(role)
        print(news.functions.getFeed().call())
        account.functions.accountAddRole(address,role).transact(transaction={'from': web3.eth.accounts[0]})
        messages.success(request,"Assignment successfull")
    return render(request,'assign_role.html')

def assign_news(request):
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    if(request.method=="POST"):
        address=request.POST.get('account')
        role=request.POST.get('role')
        role=int(role)
        print(news.functions.getFeed().call())
        print(news.functions.news_feed(role).call())
        print(address)
        print(role)
        news.functions.asvalid(address,role).transact(transaction={'from': web3.eth.accounts[0]})
        print(news.functions.news_feed(role).call())
        print(news.functions.assignedArticle(address).call())
        messages.success(request,"News assigned successfully")
        return render(request,'assign_news.html')
    else:
        return render(request,'assign_news.html')

def validate(request,id,nid):
    type=id
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    if(type==1):
        news.functions.addUpvote(nid).transact(transaction={'from': web3.eth.accounts[1]})
    else:
        news.functions.addUpvote(nid).transact(transaction={'from': web3.eth.accounts[1]})
    return redirect('news_home')

def report(request,nid):
    account = web3.eth.contract(address=acc_tx_receipt.contractAddress,abi=abi_acc)
    news = web3.eth.contract(address=tx_receipt.contractAddress,abi=abi_news)
    news.functions.report(nid).transact(transaction={'from': web3.eth.accounts[1]})
    return redirect('news_home')

    
def readerView(request):
    return render(request,"reader.html")

def validatorView(request):
    return render(request,"validator.html")

def publisherView(request):
    return render(request,"publisher.html")

def creatorView(request):
    return render(request,"creator.html")