# Sample Logging Framework for SPARKL

## Dependencies
* The [SPARKL CLI](https://github.com/sparkl/cli)
* The [PrimesExpr](https://github.com/sparkl/examples/tree/master/Examples/PrimesExpr) mix imported into the `demo@sparkl.com` user's library

## Usage
1. Start the logging framework.
   ```
   $ cd examples/python_scripts/log_framework
   $ python main.py
   Password: *********
   ws://localhost:8000/sse_listen/websocket//
   Filters set:
   filter_wrapper
   filter_wrapper
   filter_wrapper
   filter_wrapper
   On matched event call:
   stop_services
   ```
   > The framework tries to log you in as the `demo@sparkl.com` user.
2. Fire the `CheckPrime` solicit with an input `n` of `33`.
3. Fire the `CheckPrime` solicit with an input `n` of `3`.
```python
Received stop event.
Exiting...
Calling exit function: logout
{u'content': [{u'tag': u'field', u'attr': {u'type': u'integer', u'name': u'n', u'value': 3}}], u'tag': u'solicit', u'attr': {u'name': u'CheckPrime', u'svc': u'Sequencer'}}
```
The framework only reacts to `CheckPrime` events where the value of `n` falls between `1` and `14`. 

When it receives an event matching these conditions, the framework calls an `on_event` function that amongst others stops the event stream. 

Closing the event stream makes the framework exit. On exiting, the framework also calls its `on_exit` function to log you out of SPARKL.

## Customising the framework
The framework is the `log_frame` function in `log_framework.py`. The function accepts the following arguments:
* `events` - The generator returned by the `sparkl('listen')` command
* `filter_funs` - A list of filter functions with arguments. They must return either `True` or `False`
* `on_event` - **optional** - A function called if an event succeeds on all filters
* `on_exit` - **optional** - A function called when the events stream closes

Each function - filter, on_event, on_exit functions - must follow a pattern:
```python
( 
 fun_name, # Name of function,
 ( ),      # Positional arguments
 { }       # Keyword arguments
)

# For example ( my_fun, (2, ), {} )

def my_fun(n):
  print(n)
```
For the `on_event` and filter functions, the log framework inserts `event` as the first positional argument. `event` is the current event log.
```python
from sparkl_cli.main import sparkl
from log_framework import log_frame

SAMPLE_ALIAS = 'sample_alias'


def close_sparkl(alias='deault'):
    """
    Closes the connection to SPARKL.
    """
    sparkl('close', alias=alias)
   

def filter_error_events(event, tag):
    """
    Return True if the event's tag matches the tag
    parameter.
  
    Otherwise, return False.
    """
    return event['tag'] == tag

my_filters = [
  (filter_error_events, ('error',) {} )
]

exit_fun = ( close_sparkl, (), {'alias': SAMPLE_ALIAS} )

if __name__ == '__main__':
    sparkl('connect', 'http://localhost:8000', alias=SAMPLE_ALIAS)
    sparkl('login', 'demo@sparkl.com', alias=SAMPLE_ALIAS)
    events = sparkl('listen', alias=SAMPLE_ALIAS)
    log_framework(events, my_filters, on_exit=exit_fun)
```

