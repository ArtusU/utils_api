import config, time, ccxt
from web3 import Web3
from flask import Flask, render_template

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))


def get_ethereum_price():
    binance = ccxt.binance()
    ethereum_price = binance.fetch_ticker('ETH/USDC')
    return ethereum_price



@app.route("/")
def index():
    eth = w3.eth
    eth_price = get_ethereum_price()
    latest_blocks = []
    for block_number in range(eth.block_number, eth.block_number-10, -1):
        block = eth.get_block(block_number)
        latest_blocks.append(block)

    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-10:]:
        transaction = eth.get_transaction(tx)
        latest_transactions.append(transaction)

    current_time = time.time()
    return render_template("ethsonar/index.html",
                           current_time=current_time,
                           eth=eth,
                           eth_price=eth_price, 
                           latest_blocks=latest_blocks,
                           latest_transactions=latest_transactions)


@app.route("/transaction/<hash>")
def transaction(hash):
    transaction = w3.eth.get_transaction(hash)
    return render_template("ethsonar/transaction.html", hash=hash, tx=transaction)


@app.route("/address/<addr>")
def address(addr):
    return render_template("ethsonar/address.html", addr=addr)


@app.route("/block/<block_number>")
def block(block_number):
    return render_template("ethsonar/block.html", block_number=block_number)


