from server import app, infura, system, defaultABI
from src.erc20 import Contract
from flask import url_for, render_template, request, redirect
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/find_token", methods=["GET", "POST"])
def find_token():
    if request.method == "GET":
        return render_template("find_token.html", defaultABI=defaultABI)
    else:
        address = request.form["address"]
        abi = request.form["abi"]
        try:
            address = Web3.toChecksumAddress(address)
            if system.token_exists(address):
                return redirect(url_for("token", address=address))
            system.create_token(address=address, abi=abi)
            if system.token_exists(address):
                return redirect(url_for("token", address=address))

        except BadFunctionCallOutput as err:
            return render_template("find_token.html", address=address, abi=abi, defaultABI=defaultABI, error="Could not find the token details. Are you sure this is an erc20 token?")
        except Exception as err:
            return render_template("find_token.html", address=address, abi=abi, defaultABI=defaultABI, error=err)

        return render_template("find_token.html", address=address, abi=abi, defaultABI=defaultABI, error="There was an unknown error")


@app.route("/token/<address>")
def token(address):
    try:
        address = Web3.toChecksumAddress(address)
        token = system.get_token_by_address(address)
        if token is None:
            raise Exception("Could not find token at address {}".format(address))
        name = token.name
        symbol = token.symbol
        decimals = token.decimals
        totalSupply = token.totalSupply
        return render_template("token.html", name=name, symbol=symbol, decimals=decimals, totalSupply=totalSupply, showToken=True)
    except BadFunctionCallOutput as err:
        return render_template("token.html", showToken=False, error="Could not get token details. Are you sure this is an erc20 token?")
    except Exception as err:
        return render_template("token.html", showToken=False, error=err)

@app.route("/list_tokens")
def list_tokens():
    tokens = system.get_tokens()
    tuples = []
    for token in tokens:
        tuple = {"address":url_for("token",address=token.address), "name":token.name}
        tuples.append(tuple)

    return render_template("list_tokens.html", tokens=tuples)


