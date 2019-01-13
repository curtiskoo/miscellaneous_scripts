#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 21:53:08 2018

@author: curtiskoo
"""

import requests

def get_premium(pr,per):
    newp = pr * (1 + per/100)
    return newp

cmclistings = requests.get("https://api.coinmarketcap.com/v2/listings/")
cmclistings_data = cmclistings.json()
cmc_eth = list(filter(lambda x: x['name'] == 'Ethereum', cmclistings_data['data']))[0]
cmc_eth_id = cmc_eth['id']

cmc_eth_price = requests.get("https://api.coinmarketcap.com/v2/ticker/{}/?convert=CAD".format(cmc_eth_id))
cmc_eth_price = cmc_eth_price.json()
#print(cmc_eth_price)
cmc_eth_price = cmc_eth_price['data']['quotes']['CAD']['price']
print("Current CMC Price: ${} CAD/ETH".format(cmc_eth_price))
in_var = eval(input("Premium %: "))
price = get_premium(cmc_eth_price, in_var)
print("Sell Price: ${} CAD/ETH".format(price))

vol_sell = eval(input("Sell Volume: $"))
amt = vol_sell/price
print("Amount of ETH: {} ETH\n".format(amt))

def float_all(lstlst):
    lstlst = list(map(lambda x: list(map(lambda x1: float(x1), x)) , lstlst))
    return lstlst

krak_response = requests.get("https://api.kraken.com/0/public/Depth?pair=XETHZCAD")
krak_data = krak_response.json()
krak_bids = krak_data['result']['XETHZCAD']['bids']
krak_asks = krak_data['result']['XETHZCAD']['asks']
krak_asks = list(map(lambda x: x[:2], krak_asks))
krak_asks = float_all(krak_asks)
#print(krak_asks)
#print("\n")

qcx_response = requests.get("https://api.quadrigacx.com/v2/order_book?book=eth_cad")
qcx_data = qcx_response.json()
qcx_bids = qcx_data['bids']
qcx_asks = qcx_data['asks']
qcx_bids = float_all(qcx_bids)
#print(qcx_bids)

def get_spread(a,b):
    d = (1 - a/b) * 100
    sd = str(d)
    sd = sd[:sd.index(".")+4]
    sd = eval(sd)
    return sd
krak_pair = krak_asks[0]
#print(krak_pair)
qcx_pair = qcx_bids[0]
#print(qcx_pair)

krak = krak_pair[0]
qcx = qcx_pair[0]
sd = get_spread(krak,qcx)

vol = min(krak_pair[1], qcx_pair[1])

print("{}[KRAK], {}[QUAD], {}%, {} ETH [VOLUME]".format(krak,qcx,sd, vol))
buy_back = eval(input("Trading Fees %: "))
amt_after = get_premium(amt, buy_back)

print("After Trading Fees: {} ETH".format(amt_after))

krak_cost = amt_after * krak
qcx_cost = amt_after * qcx
print("KRAK Cost: ${}  |  QCX Cost: ${}".format(krak_cost, qcx_cost))

krak_profit = vol_sell - krak_cost
qcx_profit = vol_sell - qcx_cost
print("KRAK Profit: ${}  |  QCX Profit: ${}".format(krak_profit, qcx_profit))







