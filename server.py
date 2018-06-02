# SERVER
from flask import Flask
from src.erc20 import Connection
from src.system import System

app = Flask(__name__)
f = open("secretkey", "r")
secretkey = f.read().rstrip()
f.close()

app.secret_key = secretkey

f = open("infuraapi", "r")
apikey = f.read().rstrip()
f.close()
infura_url = "https://mainnet.infura.io/{}".format(apikey)

infura = Connection(infura_url)

f = open("bdc.abi")
bdcabi = f.read().rstrip()
f.close()

f = open("default.abi")
defaultABI = f.read().rstrip()
f.close()

bdcaddress = "0x8b84715c41bfb75f8E8CE47447180450758332b3"

system = System()
system.add_connection(infura)
system.create_token(bdcaddress, bdcabi)
