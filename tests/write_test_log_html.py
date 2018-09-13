"""
Author <miklos@sparkl.com> Miklos Duma
Copyright 2018 SPARKL Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Utility functions for formatting and writing
the received events to the test log.
"""
import os
import time
import json


def writer(log_file_handle):
    """
    A co-routine that writes what it receives to a file.
        - log_file_handle:
            A handle to the file the co-routine writes to.
            The file must be opened in append mode.
    """
    while True:
        to_write = (yield)
        log_file_handle.write(to_write)


def start_test_log(path_to_log):
    """
    Creates the specified file or wipes its content if
    it already exists.
    Starts a co-routine that writes to this file, and sends the
    co-routine the current time.
    Returns the co-routine instance and a handle to
    the opened file.
    """
    # Wipe content of file.
    open(path_to_log, 'w').close()

    # Open file in append mode.
    log_handle = open(path_to_log, 'a')
    print('Create log file: {}'.format(os.path.abspath(path_to_log)))

    # Get current system time.
    current_time = time.asctime(time.localtime(time.time()))

    # Create co-routine and kick it off.
    log_writer = writer(log_handle)
    log_writer.send(None)

    # Send the co-routine the date with a header to write to file.
    log_writer.send('<h1>Tests started at:' + '\n' + current_time + '</h1>')

    # Return the co-routine and the file handle.
    return log_writer, log_handle


def get_separator(indent):
    """
    Returns a string separator with the
    specified number of spaces.
    """
    sep = ''

    for _i in range(0, indent):
        sep += ' '

    return sep


def format_value(value):
    """
    Returns a formatted version of value.
    """

    # If the value is None (e.g. in the case of model events) replace
    # the value with a string representation of None.
    if not value:
        return 'None'

    # If it is serialised, de-serialise it.
    try:
        value = json.loads(value)
        return value

    # Otherwise send it back as it is.
    except TypeError:
        return value

    except json.JSONDecodeError:
        return value


def write_html(event, log_writer, event_no=None, level=0):
    if level:
        style = ' style=\"margin-left:{}em;\"'.format(level * 1.5)

    else:
        style = ''

    try:
        log_writer.send('<div{}>'.format(style))

        if event_no:
            log_writer.send('<h3>' + str(event_no) + '. ' + event['tag'] + '</h3>')
            event_keys = [key for key in event.keys() if key != 'tag']

        else:
            event_keys = event.keys()

        for key in event_keys:
            # Write the key to file.

            # Get formatted value based on key.
            value = format_value(event[key])

            # If the value is a list, invoke the same
            # function on all elements of the list with
            # increased indentation.
            if isinstance(value, list):
                log_writer.send('<div>')
                log_writer.send(key + '<button onclick=\"click_me(this)\">&#x25B2;</button>')
                for item in value:
                    write_html(item, log_writer, level=level + 1)
                log_writer.send('</div>')

            # If the value is a dictionary, split it using
            # the same function with increased indentation.
            elif isinstance(value, dict):
                log_writer.send('<div>')
                log_writer.send(key + '<button onclick=\"click_me(this)\">&#x25B2;</button>')
                write_html(value, log_writer, level=level + 1)
                log_writer.send('</div>')

            # Format simple values as string and send them.
            else:
                log_writer.send('<div>' + key + ': ' + str(value) + '</div>')

    finally:
        log_writer.send('</div>')


def write_event(event, log_writer, indent=0, event_no=None):
    """
    A recursive function that splits an event into
    small write-able chunks sending each to the writer co-routine.
        - event:
            The received event to be written to file.
        - writer:
            A co-routine that writes everything it receives
            to the test log file.
        - indent:
            An integer. It specifies the indentation for a line.
            An indent of 0 means no space, an indent of 4 means
            4 spaces. Increment it on each successive call of the
            function.
        - event_no:
            The number of the event. Each test sequence comprises
            one or more events. It is used to give the event a header
            with its serial number. Only use it on the first call of
            the function, not when it is called recursively.
    """
    # Get indentation based on value of indent keyword.
    key_indent = get_separator(indent)

    # event_no should only be given on first invocation of the function.
    # In this case use the event tag as a header for the event with the
    # serial number of the event.
    if event_no:
        log_writer.send('#' + str(event_no) + '. ' + event['tag'] + '\n')
        event_keys = [key for key in event.keys() if key != 'tag']

    else:
        event_keys = event.keys()

    # Iterate through all keys.
    for key in event_keys:

        # Write the key to file.
        log_writer.send('\n' + key_indent + key + ':' + ' ')

        # Get formatted value based on key.
        value = format_value(event[key])

        # If the value is a list, invoke the same
        # function on all elements of the list with
        # increased indentation.
        if isinstance(value, list):
            for item in value:
                write_event(item, log_writer, indent=indent + 4)

        # If the value is a dictionary, split it using
        # the same function with increased indentation.
        elif isinstance(value, dict):
            write_event(value, log_writer, indent=indent + 4)

        # Format simple values as string and send them.
        else:
            log_writer.send(str(value))


def write_log(event, name, received, log_writer):
    """
    Writes the received event into the log file.
        - event:
            The event received.
        - name:
            The name of the test function being run.
        - received:
            The number of events received during the test.
        - log_writer:
            The co-routine function that does the actual
            writing.
    """
    # When the first event is received use the name of the test as a header.
    if received == 1:
        log_writer.send('<head><link rel=\"stylesheet\" type=\"text/css\" '
                        'href=\"test_log.css\">'
                        '<script src=\"collapse.js\"></script></head>')

        log_writer.send('<h2>Events received during {}</h2>'.format(name))

    # Write formatted event to test log.
    write_html(event, log_writer, event_no=received)

    # Place two new lines between each event.
    log_writer.send('\n\n')
