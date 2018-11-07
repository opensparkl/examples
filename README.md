# OpenSPARKL Examples
[OpenSPARKL Project Home](http://opensparkl.org)
# To use an example
1. Save it to your local file system as an `xml` file.
> See shortcut [below](#bulk-importing-all-example-configurations) on how to import **all** example configurations in one go.
2. Open the SPARKL Developer Console
3. Log into an existing account or create a new one
   * To create a new account: 
     1. Click **Create a New Account**
     2. Enter your e-mail address
     3. Enter your chosen password twice
     4. Try not to forget it
4. Import the `xml` file
5. Run it in the Developer Console
 
 # Bulk importing all example configurations
 ### Dependencies
 * Python 2.7 - get it from [here](https://www.python.org/downloads/)
 * Git - get it from [here](https://git-scm.com/downloads)
 * The SPARKL CLI - get it from [here](https://github.com/opensparkl/sse_cli)
 * An existing SPARKL user account
### Procedure
1. Clone the `examples` repository.
  ```
  $ git clone https://github.com/opensparkl/examples.git
  ```
2. From the `python_scripts` directory run the `bulk_import.py` script.
  ```
  $ cd examples/python_scripts
  $ python bulk_import.py
  ```
3. Follow the instructions on the terminal screen. 
> If you choose **not** to import all examples, the script offers them one by one for importing.
  ```
  Enter your SPARKL instance URL: http://localhost:8000
  Connected to http://localhost:8000 using alias this_import_alias
  Enter your username: miklos@sparkl.com
  Password: **************
  Logged in as miklos@sparkl.com
  Import all examples? y/n y
  ```
All the selected SPARKL example configurations are imported to your user tree at the specified SPARKL instance. The script also creates the `Scratch` and `Lib` folders in your SPARKL user tree if they are not already there.
> See [this readme](https://github.com/opensparkl/examples/tree/master/Library) on the library configurations saved under the `Lib` folder.
