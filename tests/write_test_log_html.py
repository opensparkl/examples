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

DOC_START_TAG = '<!DOCTYPE html><html><head>{}{}</head><body>'.format(
    CSS_LINK, JS_LINK)

DOC_STOP_TAG = '</body></html>'

H1_STRING = '<h1>Tests started at: {}</h1>'.format(
    time.asctime(
        time.localtime(
            time.time())))


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

    # Create and start co-routine.
    log_writer = writer(log_handle)
    log_writer.send(None)

    # Add doc-type declaration, link CSS and JavaScript.
    log_writer.send(DOC_START_TAG)

    # Add title with current date.
    log_writer.send(H1_STRING)

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
    log_writer.send(DOC_STOP_TAG)

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


def html_wrapper(writer_fun, def_start_tag='<div>', def_end_tag='</div>'):
    """
    Decorator for HTML writer functions. It wraps the
    HTML content in start and end tags.
    """
    def wrapper(log_writer, *args, **kwargs):
        """
        Calls the original function with its arguments, places
        the start tag before the function is called and closes
        the HTML with the end tag.
        """
        log_writer.send(kwargs.get('start_tag', def_start_tag))
        try:
            writer_fun(log_writer, *args, **kwargs)

        finally:
            log_writer.send(kwargs.get('end_tag', def_end_tag))

    return wrapper


def write_test_header(log_writer, test_name):
    """
    Writes a test-level header once per test case.
    """
    log_writer.send('<h2>Events received during {}</h2>'.format(test_name))


@html_wrapper
def write_list_content(log_writer, key, list_value, level, **kwargs):
    """
    Writes list content to HTML. For example, the fields content of an event.
    The html_wrapper decorator puts a start and end tag
    (possibly specified in kwargs) around the content written by this function.

        - log_writer:
            The co-routine that writes the test log.
        - key:
            An event key, such as 'attr' or 'value'.
        - list_value:
            A list, the value that corresponds to 'key'.
        - level:
            The level of the div children used in calculating the
            right margin.
    """
    # Write key inside the div as it is and insert a collapsible button.
    log_writer.send(key + COLLAPSE_BUTTON)
    level += 1

    # Calculate the margin for the list elements.
    start_div = get_margin('div', level)

    # Call recursive function on each list element.
    for item in list_value:
        write_html(log_writer, item,
                   event_no=kwargs.get('event_no', None),
                   start_tag=start_div,
                   level=level)


@html_wrapper
def write_dict_content(log_writer, key, dict_value, level, **kwargs):
    """
    Writes dict content to HTML. For example, the attributes of an event.
    The html_wrapper decorator puts a start and end tag
    (possibly specified in kwargs) around the content written by this function.

        - log_writer:
            The co-routine that writes the test log.
        - key:
            An event key, such as 'attr' or 'value'.
        - dict_value:
            A dict, the value that corresponds to 'key'.
        - level:
            The level of the div children used in calculating the
            right margin.
        """
    log_writer.send(key + COLLAPSE_BUTTON)
    level += 1

    start_div = get_margin('div', level)
    write_html(log_writer, dict_value,
               event_no=kwargs.get('event_no', None),
               start_tag=start_div,
               level=level)


@html_wrapper
def write_string_content(log_writer, key, value):
    """
    Writes a single string content wrapped in div tags.
    """
    log_writer.send(key + ': ' + str(value))


@html_wrapper
def write_html(log_writer, event, **kwargs):
    """
    A recursive function that writes the SPARKL event to
    the test log HTML file.
    """

    # Each event gets a header with event's serial number and type.
    # Only write a header for the first call of this recursive function.
    if 'event_no' in kwargs and kwargs['event_no']:
        write_event_header(log_writer, kwargs['event_no'], event)

        # Do not write the event type twice (filter tag key).
        event_keys = [key for key in event.keys() if key != 'tag']

    else:
        event_keys = event.keys()

    for key in event_keys:

        # Get formatted value based on key.
        value = format_value(event[key])

        # Get indentation level.
        level = kwargs.get('level', 0)

        if isinstance(value, list):
            write_list_content(log_writer, key, value, level)

        elif isinstance(value, dict):
            write_dict_content(log_writer, key, value, level)

        else:
            write_string_content(log_writer, key, value)


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

    write_html(log_writer, event, event_no=received)
