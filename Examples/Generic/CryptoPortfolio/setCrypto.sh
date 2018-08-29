#!/bin/bash

# See the readme of the CryptoCurrency example on intended usage
# It takes the arguments:
# 	URL - The URL that points at your instance of the Developer Console
# 	USER - Your username

URL=$1
USER=$2

sparkl connect ${URL}
sparkl login ${USER}

echo Logging in to ${URL} as ${USER}

sparkl vars -r crypto_currencies crypto.erl

echo Using the content of crypto.erl as value of crypto_currencies field 

sparkl call Scratch/CryptoPortfolio/Mix/API/BulkAdd

echo invoking Scratch/CryptoPortfolio/Mix/API/BulkAdd operation

sparkl logout
sparkl close