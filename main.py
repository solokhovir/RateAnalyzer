import os

import requests
import time
import db
from web3 import Web3
from dotenv import load_dotenv

interval = 5

while True:
    headers = {"accept": "application/json"}

    load_dotenv()
    INFURA_KEY = os.getenv("INFURA_KEY")
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + f'{INFURA_KEY}'))


    def get_open_ocean():
        url_open_ocean = "https://open-api.openocean.finance/v3/eth/quote?inTokenAddress=0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599&outTokenAddress=0xdAC17F958D2ee523a2206206994597C13D831ec7&amount=1&gasPrice=5&slippage=1"
        response_open_ocean = requests.get(url_open_ocean, headers=headers)
        price_open_ocean = response_open_ocean.json()['data']['outAmount']
        gas_open_ocean = response_open_ocean.json()['data']['estimatedGas']
        return {"response_open_ocean": response_open_ocean,
                "price_open_ocean": price_open_ocean,
                "gas_open_ocean": gas_open_ocean}


    get_open_ocean = get_open_ocean()


    def get_1inch():
        url_1inch = "https://api.1inch.io/v5.0/1/quote?fromTokenAddress=0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599&toTokenAddress=0xdAC17F958D2ee523a2206206994597C13D831ec7&amount=100000000"
        response_1inch = requests.get(url_1inch, headers=headers)
        price_1inch = response_1inch.json()['toTokenAmount']
        gas_1inch = response_1inch.json()['estimatedGas']
        return {"response_1inch": response_1inch,
                "price_1inch": price_1inch,
                "gas_1inch": gas_1inch}


    get_1inch = get_1inch()

    gas_price = w3.eth.gas_price
    expected_profit = int(get_open_ocean["price_open_ocean"]) - int(get_1inch["price_1inch"])

    def open_ocean():
        data = db.Data(from_token_symbol=get_open_ocean["response_open_ocean"].json()['data']['inToken']['symbol'],
                       from_token_name=get_open_ocean["response_open_ocean"].json()['data']['inToken']['name'],
                       from_token_address=get_open_ocean["response_open_ocean"].json()['data']['inToken']['address'],
                       to_token_symbol=get_open_ocean["response_open_ocean"].json()['data']['outToken']['symbol'],
                       to_token_name=get_open_ocean["response_open_ocean"].json()['data']['outToken']['name'],
                       to_token_address=get_open_ocean["response_open_ocean"].json()['data']['outToken']['address'],
                       aggregator='OpenOcean',
                       price_USD=int(get_open_ocean["price_open_ocean"]) / 1e6,
                       final_price_with_gas_USD=(int(get_open_ocean["price_open_ocean"]) / 1e6) +
                                                (int(get_open_ocean["price_open_ocean"]) / 1e6) *
                                                (gas_price / 1e18 * float(get_open_ocean["gas_open_ocean"]) / 1e3)
                       )

        db.session.add(data)
        db.session.commit()


    def one_inch():
        data = db.Data(from_token_symbol=get_1inch["response_1inch"].json()['fromToken']['symbol'],
                       from_token_name=get_1inch["response_1inch"].json()['fromToken']['name'],
                       from_token_address=get_1inch["response_1inch"].json()['fromToken']['address'],
                       to_token_symbol=get_1inch["response_1inch"].json()['toToken']['symbol'],
                       to_token_name=get_1inch["response_1inch"].json()['toToken']['name'],
                       to_token_address=get_1inch["response_1inch"].json()['toToken']['address'],
                       aggregator='1inch',
                       price_USD=int(get_1inch["price_1inch"]) / 1e6,
                       final_price_with_gas_USD=(int(get_1inch["price_1inch"]) / 1e6) +
                                                (int(get_1inch["price_1inch"]) / 1e6) *
                                                (gas_price / 1e18 * float(get_1inch["gas_1inch"]) / 1e3)
                       )
        db.session.add(data)
        db.session.commit()


    if expected_profit > 0:
        open_ocean()
    elif expected_profit < 0:
        one_inch()
    else:
        pass

    print("Update")
    time.sleep(interval)

