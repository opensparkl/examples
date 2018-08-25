# SPARKL test framework
The `tests` folder comes with a fully-operational test framework using the `pytest` Python library and the SPARKL CLI tool. Run existing tests or write your own tests based on the ones already written.

## Dependencies
* The SPARKL command-line tool - get it from [here](https://github.com/opensparkl/sse_cli)
* The `pytest` Python library - `pip[3] install pytest`
* A `json` test settings file.

### The settings file
All tests rely on a settings file. As a minimum, the settings must specify:
* The URL of your SPARKL instance
* An existing SPARKL user account
* The password to that account
 
Based on the required settings, the tests are divided into two folders:
* `no_auth` - These tests only need the minimum settings
* `with_auth` - These tests need additional settings, such as an existing slack channel webhook.
```json
{
	  "sse_url": "http://localhost:8000",
	  "sse_user": "test@sparkl.com",
	  "sse_pass": "INSERT PASSWORD",
	  "slack_channel": "",
	  "twilio_sid": "",
	  "twilio_pass": "",
	  "twilio_number": "",
	  "test_number": ""
}
```
**IMPORTANT** - Keep the settings file outside your repositories.

## Running tests
1. Point the `CFG_PATH` environment variable at your test settings file.
   ```
   $ export CFG_PATH=~/my_projects/my_credentials/sparkl_settings.json 
   ```
2. (**Optional**) Use the `PYTHON_VERSION` variable to set the Python execution environment. By default, all `make` targets use Python2.
   ```
   $ export PYTHON_VERSION=3
   ```
3. Use the `make` targets to run either all tests or just specific ones.
   ```
   # Run from root of repository
   $ cd examples
   
   # Run only tests in the no_auth folder
   $ make test_basic
   
   # Run only tests in the with_auth folder
   $ make test_auth
   
   # Run all tests
   $ make test
   ```

## Adding tests
Use our template to write your own tests and add them to the existing framework. 

1. Duplicate [this](template.py) test template.
2. Name it `test_*.py`. For example: `test_my_mix.py`
3. Edit the file with the help of the comments in it.
4. Save it inside the `no_auth` folder.
5. Run the tests to see if your new addition is working.
