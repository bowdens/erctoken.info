from server import app, infura, system
from src.erc20 import Contract
from flask import url_for, render_template, request
import requests

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/find_token", methods=["GET", "POST"])
def find_token():
    if request.method == "GET":
        return render_template("find_token.html")
    else:
        address = request.form["address"]
        abi = request.form["abi"]
        print("address is '{}'\nabi is {}".format(address, abi))
        try:
            coin = Contract(address=address, abi=abi, connection=infura)
            print("Coin got! Address is {}".format(coin))
        except Exception as err:
            return render_template("find_token.html", address=address, abi=abi, error=err)

        return render_template("find_token.html", address=address, abi=abi, token=coin)


@app.route("/token/<address>")
def token(address):
    token = system.get_token_by_address(address)
    return render_template("token.html", token=token)


