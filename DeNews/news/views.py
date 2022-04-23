import imp
from django.shortcuts import render
import json

from web3 import Web3
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

url = "https://ropsten.infura.io/v3/5e23d056df8247cdbedc0a89a1c8040d"

web3 = Web3(Web3.HTTPProvider(url))