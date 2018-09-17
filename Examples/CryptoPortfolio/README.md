# Cryptocurrencies example
_In this example we use SPARKL to get the latest price of Bitcoin and a set of other cryptocurrencies._

## Prerequisites
* The SPARKL CLI - [get it](https://github.com/opensparkl/sse_cli)

## Getting the code
1. Save the source code of the example by:
    * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Examples/CryptoPortfolio/CryptoPortfolio.xml)
    * Clicking **Save Link As...**
2. Save the source code of the Bitcoin library by: 
   * Right-clicking [this link](https://raw.githubusercontent.com/opensparkl/examples/master/Library/lib_bitcoin/lib_bitcoin.xml)
   * Clicking **Save Link As...**
3. Import both into your SPARKL user account.
    > See [link](https://github.com/opensparkl/examples#use_examples) for further details.

## Getting the event logs
1. Use the SPARKL CLI to connect to your user account.
    ```
    $ sparkl connect http://localhost:8000
    $ sparkl login [YOUR_USERNAME]
    password: ******
    ```
4. Read the event logs.
    ```
    $ sparkl listen
    ```
    > See the [SPARKL CLI wiki](https://github.com/opensparkl/sse_cli/wiki/Analysing-SPARKL-event-logs) for further details on reading and filtering SPARKL event logs.

## Running the mix

### Managing your portfolio
Use the operations below to specify which cryptocurrencies you are interested in and in what currency you want to get their prices.
> Once an instance of the Portfolio service is up, check the information kept in the service instance, such as the currency used for the conversions or the latest price of Bitcoin.

![crypto_port_manage](https://user-images.githubusercontent.com/17043451/27142436-f0e6aeae-5122-11e7-96c6-99b6180c2e7b.png)

* **`AddRecord`** - Adds the specified cryptocurrency to your portfolio. For example : `eth` or `ltc`.
   > See the [Poloniex website](https://poloniex.com/exchange) on supported currencies.
* **`DeleteRecord`** - Deletes a specified cryptocurrency from your portfolio. Use `GetRecords` to see what you have in your portfolio. For example: `eth` or `ltc`.
* **`GetRecords`** - Returns the list of cryptocurrencies in your portfolio.
* **`GetCurrency`** - Returns the currency used for conversions.
* **`ChangeCurrency`** - Changes the currency used for conversions. For example: `usd` or `gbp`.
   > The default value is `usd`.
* **`BulkAdd`** - Adds a list of cryptocurrencies to your portfolio. For example: `["etc","eth","ltc"]`.
   > Use `BulkAdd` to restore your portfolio from file. For example, the `setCrypto.sh` script uses the content of the `crypto.erl` file to update the portfolio.

### Getting price updates

1. Select the `Timer` service.
2. Click the play symbol to start an instance of it.

As long as this service is up, the `Update` operation is fired every 10 seconds to get the latest prices of Bitcoin and all cryptocurrencies in your portfolio. 
> Remember, the prices are in the currency you specify through `ChangeCurrency`. The default value is `usd`.

![crypto_port_timer](https://user-images.githubusercontent.com/17043451/27142458-00c9455c-5123-11e7-8c46-d11f80559ab3.png)

The `Compare` operation calculates the percentage change between the current and the previous prices of each cryptocurrency in your portfolio. 

The `LogChanges` operation logs all changes and also updates your portfolio with the latest prices.

The `SetPrice` operation logs the latest price of Bitcoin. 
