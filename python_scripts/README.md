# Example Python scripts with SPARKL commands
To use any of the scripts, you need the following:
* Python 2.7 - get it from [here](https://www.python.org/downloads/)
* The SPARKL CLI - get it from [here](https://github.com/sparkl/cli)

## Available scripts
* `login_and_logout.py` - Use it to connect and log into a SPARKL instance or to log out and close a connection.
* `bulk_import.py` - Use it to import the sample configurations in the `examples` repository.  
* `tests` - Use it to run automated tests on the SPARKL configurations kept in the `examples` repository.
  
## Using the bulk_import script
The script imports all or only the specified SPARKL mixes in this repo into your configuration tree.

The mixes are imported into the `Scratch` folder.

The library mixes are imported into the `Lib` folder.

If the folders don't exist, the script creates them.
```
$ cd [PATH_TO_REPO]/examples/python_scripts
$ python bulk_import.py
```
The script will prompt you to:
1. Choose a running SPARKL instance to connect to (e.g. `http://localhost:8000`)
2. Specify an existing user name
3. Decide whether:
   * You want to import all sample SPARKL mixes into your configuration tree
   * You want to import only specific mixes

After importing the selected configurations, the script logs you out and closes the connection.
