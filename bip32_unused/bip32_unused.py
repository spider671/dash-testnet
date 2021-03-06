#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io, os, sys
import simplejson as json
import datetime
import time
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# https://github.com/chaeplin/bip32utils
from bip32utils import BIP32Key

def getaddresstxids(address):
    try:
        params = {
            "addresses": [address]
        }
        r = access.getaddresstxids(params)
        return r

    except Exception as e:
        p#rint('rpc error : ', e)
        return None

def bip32_getaddress(xpub, index_no):
    assert isinstance(index_no, int)
    acc_node = BIP32Key.fromExtendedKey(xpub)
    addr_node = acc_node.ChildKey(index_no)
    address = addr_node.Address()
    return address

def get_bip32_unused(xpub):
    i = 0
    m = 0 
    while True:
        child_address = bip32_getaddress(xpub, i)
        check_unused = None
        while check_unused == None:
        	x = getaddresstxids(child_address)
        	if x != None:
        		check_unused = len(x)
        	else:
        		check_unused = None
        		time.sleep(1)

        if check_unused == 0:
        	m = m + 1
        	yield i, m, child_address
        
        else:
        	m = 0

        i = i + 1

        if i > max_child_index :
           sys.exit() 
        if m > max_unused_key:
           sys.exit()

# for testnet
rpcuser         = 'dashmnb'
rpcpassword     = 'iamok'
rpcbindip       = 'test.stats.dash.org'
rpcport         = 587
max_unused_key  = 30
max_child_index = 2000

serverURL = 'https://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + ':' + str(rpcport)
access = AuthServiceProxy(serverURL)

# http://chaeplin.github.io/bip39/
# tpub of m/44'/1'/0'/0

BIP32_EXTENDED_KEY = input("Please enter BIP32 Extended Public Key: ")

if not BIP32_EXTENDED_KEY.startswith('tpub'):
	sys.exit("\n\t===> not bip32 ext pub key for testnet\n")

try:
	bip32_tpub = get_bip32_unused(BIP32_EXTENDED_KEY)
	print('index\tseq\taddress')
	while True:
		bip32_unused_index, bip32_unused_seq, bip32_unused_address = bip32_tpub.__next__()
		print("%s\t%s\t%s" % (bip32_unused_index, bip32_unused_seq, bip32_unused_address))
		if bip32_unused_index > max_child_index :
			break
		if bip32_unused_seq > max_unused_key:
			break


except KeyboardInterrupt:
    sys.exit()
