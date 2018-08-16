# Bitcoin Python Rest example
_In this example we use SPARKL with a small Python widget to get the current price of Bitcoin and other crypto currencies._

### 1. Getting the code
1. Clone the whole repository from git.
2. Import the `bitcoin_python.xml` mix into the Developer Console.

### 2. Running the mix
1. Start the Python widget.
  ```
  cd examples/Examples/bitcoin_python
  python3 __main__.py
  ```
2. Populate the **Service path** field of the widget with the full user tree path to the `Bitcoin` service prepended by your user name. 
   > For example: `miklos@sparkl.com/Scratch/bitcoin_python/Bitcoin`
3. Click **Connect**.
- To get the price of Bitcoin, on the **Bitcoin** panel select a FIAT currency from the drop-down menu and click **Get**. 
- To get the price of another crypto currency, on the **Other crypto coins** panel select both a FIAT currency and a crypto currency and click **Get**.

![bitcoin_rest](https://user-images.githubusercontent.com/17043451/38095019-47a83af6-3367-11e8-874c-1a4026e21354.png)
