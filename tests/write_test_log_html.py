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


CSS_LINK = '<link rel=\"stylesheet\" type=\"text/css\" href=\"test_log.css\">'
JS_LINK = '<script src=\"collapse.js\"></script>'
COLLAPSE_BUTTON = '<button onclick=\"click_me(this)\">&#x25B2;</button>'


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
    # Create/wipe content of file.
    open(path_to_log, 'w').close()

    # Open file in append mode.
    log_handle = open(path_to_log, 'a')
    print('Create log file: {}'.format(os.path.abspath(path_to_log)))

    # Get current system time.
    current_time = time.asctime(time.localtime(time.time()))

    # Create and start co-routine.
    log_writer = writer(log_handle)
    log_writer.send(None)

    # Add doc-type declaration, link CSS and JavaScript.
    log_writer.send('<!DOCTYPE html><html><head>{}{}</head><body>'.format(
        CSS_LINK, JS_LINK))

    # Add title with current date.
    log_writer.send('<h1>Tests started at: {}</h1>'.format(current_time))

    # Return the co-routine and the file handle.
    return log_writer, log_handle


def stop_test_log(log_writer, log_handle):
    """
    Closes the test log file and stops the writer
    co-routine.
        - log_writer:
            The log writer co-routine.
        - log_handle:
            A handle to the test log file.
    """

    # Close outer HTML tags.
    log_writer.send('</body></html>')

    # Stop co-routine.
    log_writer.close()

    # Close log file.
    log_handle.close()


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


def get_margin(element, level):
    """
    Calculates right margin of element based on its level.
    I.e., embedded divs gradually shift to the right.
    """
    if level:
        style = ' style=\"margin-left:{}em;\"'.format(level * 1.5)

    else:
        style = ''

    return '<{}{}>'.format(element, style)


def write_event_header(log_writer, event_no, event):
    """
    Writes a header for the event. The header comprises:
        - event_no:
            The serial number of the event.
        - event['tag']:
            The type of the event.
    """
    header = '<h3>{}. {}</h3>'.format(str(event_no), event['tag'])
    log_writer.send(header)


def html_wrapper(writer_fun):
    def wrapper(log_writer, *args, **kwargs):

        log_writer.send(kwargs.get('start_tag', '<div>'))
        try:
            writer_fun(log_writer, *args, **kwargs)

        finally:
            log_writer.send(kwargs.get('end_tag', '</div>'))

    return wrapper


def write_test_header(log_writer, test_name):
    """
    Writes a test-level header once per test case.
    """
    log_writer.send('<h2>Events received during {}</h2>'.format(test_name))


@html_wrapper
def write_list_content(log_writer, list_value, level, **kwargs):
    start_tag = get_margin('div', level)
    start_div = get_margin('div', level)
    log_writer.send(start_div)

    for item in list_value:
        write_html(item, log_writer, level=level + 1)


@html_wrapper
def write_dict_content(log_writer, dict_value, level, **kwargs):
    write_html(dict_value, log_writer, level=level + 1)


@html_wrapper
def write_string_content(log_writer, key, value):
    log_writer.send(key + ': ' + str(value))


def write_html(event, log_writer, event_no=None, level=0):
    """
    Recursively writes an event to the HTML log file.
        - event:
            The SPARKL event it writes to the log file.
        - log_writer:
            A co-routine that writes to the log file.
        - event_no:
            The serial number of the event. Only given on the
            first call of the function. It is used for writing
            a header with the event type and the serial number.
        - level:
            The left margin, increased on successive calls.
    """
    start_div = get_margin('div', level)
    try:
        log_writer.send(start_div)

        if event_no:
            write_event_header(log_writer, event_no, event)
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
                start_tag = '<div>' + key + COLLAPSE_BUTTON
                end_tag = '</div>'
                write_list_content(log_writer, value, level,
                                   start_tag=start_tag,
                                   end_tag=end_tag)

            # If the value is a dictionary, split it using
            # the same function with increased indentation.
            elif isinstance(value, dict):
                start_tag = '<div>' + key + COLLAPSE_BUTTON
                end_tag = '</div>'
                write_dict_content(log_writer, value, level,
                                   start_tag=start_tag,
                                   end_tag=end_tag)

            # Format simple values as string and send them.
            else:
                write_string_content(log_writer, key, value)

    finally:
        log_writer.send('</div>')


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
        write_test_header(log_writer, name)

    # Write formatted event to test log.
    write_html(event, log_writer, event_no=received)
