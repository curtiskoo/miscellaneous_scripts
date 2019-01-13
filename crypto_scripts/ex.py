#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:32:03 2018

@author: curtiskoo
"""
import krakenex
import requests

def float_all(lstlst):
    lstlst = list(map(lambda x: list(map(lambda x1: float(x1), x)) , lstlst))
    return lstlst

def get_spread(a,b):
    d = (1 - a/b) * 100
    sd = str(d)
    sd = sd[:sd.index(".")+4]
    sd = eval(sd)
    return sd

pairs_dic = {'ETH': ['XETHZCAD', 'eth_cad'],
             'BTC': ['XXBTZCAD', 'btc_cad']}

for pair in pairs_dic:
    k1 = pairs_dic[pair][0]
    q1 = pairs_dic[pair][1]

    krak_response = requests.get("https://api.kraken.com/0/public/Depth?pair={}".format(k1))
    krak_data = krak_response.json()
    #print(krak_data)
    krak_bids = krak_data['result'][k1]['bids']
    krak_asks = krak_data['result'][k1]['asks']
    krak_asks = list(map(lambda x: x[:2], krak_asks))
    krak_asks = float_all(krak_asks)
    #print(krak_asks)
    #print("\n")

    qcx_response = requests.get("https://api.quadrigacx.com/v2/order_book?book={}".format(q1))
    qcx_data = qcx_response.json()
    qcx_bids = qcx_data['bids']
    qcx_asks = qcx_data['asks']
    qcx_bids = float_all(qcx_bids)
    #print(qcx_bids)

    krak_pair = krak_asks[0]
    #print(krak_pair)
    qcx_pair = qcx_bids[0]
    #print(qcx_pair)

    krak = krak_pair[0]
    qcx = qcx_pair[0]
    sd = get_spread(krak,qcx)

    vol = min(krak_pair[1], qcx_pair[1])

    print("{}[KRAK] | {}[QUAD] | {}% | {} {} [VOLUME] | ${} Cost | ${} Profit".format(krak,qcx,sd, vol, pair, round(krak*vol, 2),round((qcx-krak)*vol, 2)))

    
