# Bitcoin price lookup library mix
This library mix can be used to get the price of Bitcoin and other cryptocurrencies in various currencies.

## Supported cryptocurrencies and currencies:
* **Cryptocurrencies** - Bitcoin and all cryptocurrencies traded on [Poloniex](https://poloniex.com/exchange#btc_eth).
* **Currencies** - See the [Blockchain API](https://blockchain.info/ticker) on supported currencies.

## Using the library mix
1. Add a service that imports the functionality of the `lib_bitcoin` library:
   * With the `subr.import` property
   * With the key `lib.bitcoin.Bitcoin`

   ```xml
   <service name="LibBitcoin" provision="subr">
      <prop name="subr.import" key="lib.bitcoin.Bitcoin"/>
   </service>
   ```

2. Add a request/reply operation that retrieves the latest price of Bitcoin in a specified currency:
   * Have it implemented by the service just added
   * Name it `GetBTC`
   * Give it two replies - `Ok` and `Error`
   * Give it an input string: `currency`
   * Make it send either a term -`error`, or a float - `btc_price`
   
   ```xml
   <request name="GetBTC" service="LibBitcoin" fields="currency">
      <reply name="Ok" fields="btc_price"/>
      <reply name="Error" fields="error"/>
   </request>
   ```
   
3. Add another request/reply operation that retrieves the latest price of a specified cryptocurrency in the specified currency:
   * Have it implemented by the service just added
   * Name it `GetCrypto`
   * Give it two strings as input: `currency` and `crypto_currency`
   * Give it two replies - `Ok` and `Error`
   * Make it send either a term - `error`, or a float - `crypto_price`
  
   ```xml
   <request name="GetCrypto" service="LibBitcoin" fields="crypto_currency currency">
      <reply name="Ok" fields="crypto_price"/>
      <reply name="Error" fields="error"/>
   </request>
   ```

## Example
See the [CryptoPortfolio example](../../Examples/CryptoPortfolio) on how to integrate and use this library.
