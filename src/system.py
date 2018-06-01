from src.erc20 import Contract, Connection

class System():
    def __init__(self):
        self.__tokens = {}
        self.__connections = []

    def add_connection(self, connection):
        if not isinstance(connection, Connection):
            raise TypeError("Must be of type Connection")
        self.__connections.append(connection)

    def __add_token(self, token):
        if not isinstance(token, Contract):
            raise TypeError("Token must be of type Contract")
        if token.address in self.__tokens:
            raise ValueError("Token was already added to list")
        print("adding token to {}".format(token.address))
        self.__tokens[token.address] = token

    def create_token(self, address, abi):
        token = None
        for connection in self.__connections:
            try:
                token = Contract(address=address, abi=abi, connection=connection)
            except:
                continue
            break
        if token is None:
            raise Exception("Could not create token with any connection.")
        self.__add_token(token)

    def get_token_by_address(self, address):
        return self.__tokens.get(address)

    def get_connections(self):
        return self.__connections

