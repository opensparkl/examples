"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Sample SPARKL event filtering code.

Illustrates how to use the log framework.

The filters are set so as to only let through:
    - solicit events
    - named CheckPrime
    - that carry a field named n
    - where the value of n is between 1 and 14

The sample also introduces:
    - an on_event function:
        stop_services - On receiving an event (matching all above conditions):
                1. The event is put in a queue (shared with the main process)
                2. All SPARKL services are stopped in the Primes_expr folder
                3. The stream of events is closed
    - an on_exit function:
        logout - It simply closes the connection to SPARKL. Note, it is called
                 with the finally statement - i.e. gets executed no matter what
"""

from __future__ import print_function

import sys
from sparkl_cli.main import sparkl, CliException

from log_framework import log_frame
from log_exception import LogException
from sample_filters import (filter_tag, filter_field, filter_name,
                            filter_field_values)

# Import queue without upsetting either Py2 or Py3.
if sys.version_info.major == 3:
    import queue as queue_mod
else:
    import Queue as queue_mod

# Specify user and alias
FILTER_ALIAS = 'test_filter'
FILTER_USER = 'demo@sparkl.com'

# Level on which stop_services stops running services.
TARGET_FOR_STOP = 'Scratch/Primes_expr'

# Filters to be used in logging framework. The filter functions
# are imported from sample_filters.py. NOTE, the log framework inserts
# the event parameter for all filter functions as the first argument
SAMPLE_FILTERS = [
    # Filter only solicit events
    (filter_tag, ('solicit',), {}),
    # Whose name is CheckPrime
    (filter_name, ('CheckPrime',), {}),
    # Who send the 'n' field
    (filter_field, ('n',), {}),
    # And where the value of n is between 1 and 14
    (filter_field_values, ('n',), {'min_val': 1, 'max_val': 14})]


def logout(alias='default'):
    """
    Called on on_exit of logger frame.
    Closes the connection to SPARKL.
    """
    sparkl('close', alias=alias)


def stop_services(event, path, events, event_queue, alias='default'):
    """
    Called on on_event of logger frame.

    Prints the specified event, stops all
    running SPARKL services in path and
    closes the event generator.

    NOTE: The 'event' argument is inserted by the log framework.
    The function is sent to the framework thus:
        - ( stop_services, ( path, events, event_queue ), { 'alias': alias } )
    """
    print('Received stop event.')
    event_queue.put(event)
    sparkl('stop', path, alias=alias)
    events.close()


def login(user, alias):
    """
    Logs in specified user and starts the
    event logging.

    Returns either:
        - True, the events generator
        - False, an error message
    """
    try:
        sparkl('connect', 'http://localhost:8000', alias=alias)
        sparkl('login', user, alias=alias)

        # Specify a path to any configuration object to
        # narrow down the events you will be receiving.
        # E.g. sparkl listen Scratch/Primes/CheckPrime
        events = sparkl('listen', alias=alias)
        return True, events

    except CliException as error:
        return False, error


def read_queue(event_queue):
    """
    Tries to retrieve events from a queue.
    Immediately stops if the queue is empty.
    """
    try:
        event = event_queue.get(block=False)
        print(event)

    except queue_mod.Empty:
        print('No events collected.')


def main(user, filters, alias='default'):
    """
    Logs in the specified user, starts the event logging
    and hands down the events generator and the specified
    filters to the logging framework.

    Also specifies an on-event and on-exit function for this
    framework.

    The on-event function uses a queue to communicate with the
    main function.
    """
    # Try to login
    success, result = login(user, alias)

    # Log out on failure (e.g. wrong username/password/not running instance)
    if not success:

        try:
            sparkl('close', alias=alias)
            print(result)

        except CliException as error:
            print(error)
        return

    # If login was successful, evens generator is returned by login
    events = result

    # Create a queue shared between the main process and the on-event function
    event_queue = queue_mod.Queue()

    # Cleanup function to call when exiting from logging.
    on_exit = (logout,
               (),
               {'alias': alias})

    # Function to call on successful matching of event. The log framework
    # will insert 'event' as the first parameter
    on_event = (stop_services,
                (TARGET_FOR_STOP, events, event_queue),
                {'alias': alias})

    try:
        # Start logging using filters, on_event and on_exit functions
        log_frame(events, filters, on_exit=on_exit, on_event=on_event)

    except LogException as error:
        print(error.message)
        sparkl('close', alias=alias)
        raise

    # Go through queue after logging stopped
    read_queue(event_queue)


if __name__ == '__main__':

    # Call main function
    main(FILTER_USER, SAMPLE_FILTERS, alias=FILTER_ALIAS)
