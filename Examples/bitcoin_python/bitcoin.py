"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Python implementation of the rest version of the bitcoin library mix.

Supports Python3 only.
"""

import requests
import json


BTC_URL = 'https://blockchain.info/ticker'
POLONIEX_URL = 'https://poloniex.com/public?command=returnTicker'


def get_last_value(url, currency):
    """
    Tries to get the last value of the specified currency
    using the url to a bitcoin exchange API url.
    """
    values = json.loads(requests.get(url).text)

    try:
        return True, values[currency]['last']

    except KeyError:
        return False, '{} is not a valid currency.'.format(currency)


def get_btc(request, callback):
    """
    Provides the logic behind the GetBTC operation.
    """
    currency = request['data']['currency'].upper()

    success, value = get_last_value(BTC_URL, currency)

    if success:
        return callback({
            'reply': 'Ok',
            'data': {
                'btc_price': value
            }
        })

    return callback({
        'reply': 'Error',
        'data': {
            'error': value
        }
    })


def get_crypto(request, callback):
    """
    Provides the logic behind the GetCrypto operation.
    """
    crypto_currency = request['data']['crypto_currency'].upper()
    crypto_key = 'BTC_' + crypto_currency

    success, value = get_last_value(POLONIEX_URL, crypto_key)

    if success:
        return callback({
            'reply': 'Ok',
            'data': {
                'price_in_btc': value
            }
        })

    return callback({
        'reply': 'Error',
        'data': {
            'error': value
        }
    })


def convert(request, callback):
    """
    Provides the logic behind the Convert operation.
    """
    price_in_btc = request['data']['price_in_btc']
    btc_price = request['data']['btc_price']
    crypto_price = btc_price * price_in_btc
    callback({
        'reply': 'Ok',
        'data': {
            'crypto_price': crypto_price
        }
    })


def onopen(service):
    """
    Called when the websocket connection to the
    rest service is established. It maps the logic
    to the operations on the rest service.
    """

    impl = {
        'Mix/Bitcoin/GetBTC': get_btc,
        'Mix/Bitcoin/GetCrypto': get_crypto,
        'Mix/Bitcoin/Convert': convert}

    service.impl = impl
    print('Serving {}...'.format(service.service))
