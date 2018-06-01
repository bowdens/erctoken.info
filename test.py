from web3 import Web3, HTTPProvider

f = open("infuraapi")
apikey = f.read().rstrip()
f.close()

#print(apikey)

infura = "https://mainnet.infura.io/{}".format(apikey)
#print("'{}'".format(infura))

w3 = Web3(HTTPProvider(infura))

print("Latest block number = {}".format(w3.eth.blockNumber))

f = open("bdc.abi")
bdcabi = f.read().rstrip()
f.close()

bdcaddress = "0x8b84715c41bfb75f8E8CE47447180450758332b3"

bowdencoin = w3.eth.contract(address=bdcaddress, abi=bdcabi)
name = bowdencoin.functions.name().call()
symbol = bowdencoin.functions.symbol().call()
decimals = bowdencoin.functions.decimals().call()
totalSupply = bowdencoin.functions.totalSupply().call()

print("Total supply of {} is {} {}".format(name, totalSupply/(10**decimals), symbol))
