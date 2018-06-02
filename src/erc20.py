from web3 import Web3, HTTPProvider

class Connection():
    def __init__(self, address):
        self.__address = address
        self.__w3 = Web3(HTTPProvider(address))

    @property
    def w3(self):
        return self.__w3

class Contract():
    def __init__(self, address=None, abi=None, source=None, connection=None):
        if not Web3.isAddress(address):
            raise ValueError("'{}' is not a valid address".format(address))
        if source is None and abi is None:
            raise Exception("Either source OR abi must not be none")
        if not isinstance(connection, Connection):
            raise TypeError("Connection was invalid")

        self.__connection = connection
        self.__address = Web3.toChecksumAddress(address)
        self.__source = None
        self.__code = None
        self.__abi = None
        if source is not None:
            self.source = source
            # todo: self.source also sets self.__code. Change this
            self.__abi = self.__code["abi"]
        else:
            assert(abi is not None)
            self.__abi = abi
        self.__contract = self.__connection.w3.eth.contract(address=self.__address, abi=self.__abi)

        self.__decimals = None
        self.__symbol = None
        self.__name = None
        self.__totalSupply = None

    def refresh(self):
        self.__decimals = self.function("decimals")
        self.__symbol = self.function("symbol")
        self.__name = self.function("name")
        self.__totalSupply = self.function("totalSupply")
        self.__code = self.__connection.w3.eth.getCode(self.__address)

    @property
    def code(self):
        if self.__code == None:
            self.__code = self.__connection.w3.eth.getCode(self.__address)
        return self.__code

    @property
    def totalSupply(self):
        if self.__totalSupply == None:
            self.__totalSupply = self.function("totalSupply")
        return self.__totalSupply

    @property
    def name(self):
        if self.__name == None:
            self.__name = self.function("name")
        return self.__name

    @property
    def symbol(self):
        if self.__symbol == None:
            self.__symbol = self.function("symbol")
        return self.__symbol

    @property
    def decimals(self):
        if self.__decimals == None:
            self.__decimals = self.function("decimals")
        return self.__decimals

    @property
    def address(self):
        return self.__address

    @property
    def abi(self):
        return self.__abi

    @property
    def source(self):
        return self.__source
    @source.setter
    def source(self,val):
        compiled = compile_source(val)
        compiled_interface = compiled["<stdin>:{}".format(self.name)]
        compiled_code = compiled_interface["bin"]
        if compiled_code != self.code:
            raise ValueError("Compiled source code does not match blockchain version")
        self.__source = compiled_code
        self.__code = compiled_interface

    @property
    def bin(self):
        if self.__code == None:
            return None
        return self.__code["bin"]


    def balanceOf(self, address):
        if not Web3.isAddress(address):
            raise ValueError("'{}' is not a valid address".format(address))
        return self.__contract.functions.balanceOf(address).call()

    def allowance(self, onwer, spender):
        if not Web3.utils.isAddress(owner):
            raise ValueError("'{}' is not a valid address".format(owner))
        if not Web3.utils.isAddress(spender):
            raise ValueError("'{}' is not a valid address".format(spender))
        return self.__contract.functions.allowance(owner, spender).call()

    def function(self, function, *args):
        f = self.__contract.functions[function]
        return f(*args).call()
