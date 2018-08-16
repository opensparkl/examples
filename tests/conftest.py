"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test harness for testing SPARKL sample configs in examples repo.
"""
from multiprocessing import Process, Queue

import time
import uuid
import os
import json
import pytest

from sparkl_cli.main import sparkl

# Random generated alias used for SPARKL connection.
ALIAS = uuid.uuid4().hex

# Environment variable that points at the configuration file.
CONFIG_PATH = 'CFG_PATH'

# The folder in the user tree created for test configurations
IMPORT_DIR = 'Test'

# Keys used by the individual tests to specify their input and expected output.
OPERATION = 'operation'
INPUT_FIELDS = 'input_fields'
EXP_RESPONSE = 'exp_resp'
OUTPUT_FIELDS = 'output_fields'
CHECK_FUN = 'check_function'
STOP_OR_NOT = 'stop_or_not'

# Error messages
FLOAT_ERROR = 'The value of \'{}\' must be a float.'
ZERO_ERROR = 'The value of \'{}\' must not be zero.'


def read_from_config(cfg_key):
    """
    Reads a value from the configuration file. This file is
    kept outside the repo and is located using an environment
    variable.
    """

    config_path = os.environ[CONFIG_PATH]

    with open(config_path, 'r') as config:
        config_json = json.load(config)

    return config_json[cfg_key]


def check_float_value(float_value, field_name):
    """
    Checks whether float value is indeed a float
    and its value is larger than zero.

    If not, the test fails with a specific error message.
    """
    assert isinstance(float_value, float), FLOAT_ERROR.format(field_name)
    assert float_value != 0, ZERO_ERROR.format(field_name)


def format_response_data(sparkl_response):
    """
    Builds easy-access object from response data sent back by SPARKL.
    """

    # Get name of response/reply and list of output fields
    try:
        response_name = sparkl_response['attr']['name']
        fields_data_list = sparkl_response['content']

    # Return full response in case of error event (i.e. if mix fails to
    # execute)
    except KeyError:
        return sparkl_response

    # Build object from field name/value pairs
    fields_object = {}
    for field in fields_data_list:
        field_name = field['attr']['name']

        # Flag fields have no value, add value only if not FLAG
        field_value = None

        # If field has value, its value is first element of content list
        if 'content' in field:
            field_value = field['content'][0]

        # Add field name/value to fields dictionary
        name_value_pair = {field_name: field_value}
        fields_object.update(name_value_pair)

    return_data = {
        'response': response_name,
        'fields': fields_object
    }

    return return_data


def get_sparkl_result(operation, alias, fields=None):
    """
    Generic function used by tests. It sets the
    expected input fields, and calls the specified operation.

    It returns the response and the output fields.
    """
    # In case of FLAGS, no field values are needed.
    if fields:
        sparkl('vars', literal=fields, alias=alias)

    result = format_response_data(sparkl('call', operation, alias=alias))

    try:
        response = result['response']
        fields = result['fields']
        return response, fields

    except KeyError:
        error_msg = 'SPARKL error: {}'.format(json.dumps(result))
        assert False, error_msg


def compare_response(exp_resp, act_resp):
    """
    Checks whether the tested operation returns the expected response/reply.
    If not, the test using this function fails.
    """
    # Error message returned if the test fails.
    error_message = 'Expected response is {}, ' \
                    'not {}.'.format(exp_resp, act_resp)
    assert act_resp == exp_resp, error_message


def compare_values(exp_val, act_val):
    """
    Checks whether the expected field value matches the actual returned value.

    If not, the test using this function fails.
    """
    # Error message returned if the test fails.
    error_message = 'Expected value of {}, not {}.'.format(exp_val, act_val)
    assert exp_val == act_val, error_message


def run_tests(alias, **test_data):
    """
    Run once per test.
        - alias:
            The SPARKL alias used by the session
        - test_data:
            A dict containing the test data. It comprises:
                - OPERATION:
                    The name of the operation to call
                - INPUT_FIELDS (optional):
                    The input fields and their values
                - EXP_RESPONSE:
                    The expected response/reply
                - OUTPUT_FIELDS (optional):
                    One or more output fields with their expected value
                - CHECK_FUN (optional):
                    A function that makes extra assertions on the output values
                - STOP_OR_NOT (optional):
                    A flag to indicate all running services must be stopped
                    before the test is run
    """
    # Collect test data. Only operation name and expected response/reply are
    # mandatory.
    operation = test_data[OPERATION]
    exp_resp = test_data[EXP_RESPONSE]

    # Optional test values are None if not supported.
    fields = test_data.get(INPUT_FIELDS, None)
    exp_output_fields = test_data.get(OUTPUT_FIELDS, None)
    stop_or_not = test_data.get(STOP_OR_NOT, None)
    check_fun = test_data.get(CHECK_FUN, None)

    # Stop all services in test directory if test requires so.
    if stop_or_not:
        sparkl('stop', IMPORT_DIR, alias=alias)

    # Call SPARKL operation and gather results.
    response, out_fields = get_sparkl_result(operation, alias, fields=fields)

    # Check response/reply is as expected.
    compare_response(exp_resp, response)

    # If the test specifies expected output fields and values, check them.
    if exp_output_fields:
        for key, exp_value in exp_output_fields.items():
            act_value = out_fields[key]
            compare_values(exp_value, act_value)

    # If the test specifies an extra function to check the output values,
    # use that function.
    if check_fun:
        check_fun(out_fields)


def event_to_queue(alias, listen_path, event_queue):
    """
    Starts a listener process and puts each event
    in the supplied event queue.
        - alias:
             The SPARKL CLI alias used by the test suite.
        - listen_path:
            The path to the SPARKL resource targeted by
            the listener (e.g. a service or an operation).
        - event_queue:
            A queue used by the listener process to communicate
            with the main test process.
    """
    events = sparkl('listen', listen_path, alias=alias)

    for event in events:
        event_queue.put(event)


def start_listener_proc(listen_target, alias):
    """
    Starts a process that listens to events corresponding to
    the supplied target (e.g. a service or operation).
    The events are placed by the process in the queue created
    by this function.
    The function returns the queue and the process instance.
    """
    event_queue = Queue()

    # Start the listener in another process and feed events into the queue.
    listen_process = Process(target=event_to_queue,
                             args=(alias,
                                   listen_target,
                                   event_queue))
    listen_process.daemon = True
    listen_process.start()

    # Give the process time to come up properly.
    time.sleep(1)
    return event_queue, listen_process


@pytest.fixture(scope='module')
def setup_method(request):
    """
    Setup method used by tests. Called once per test modules.

    It collects the path to one or more SPARKL configurations
    specified in the test module (kept in the FILE_PATHS constant) and
    imports them into the test directory.

    This method collects the alias from the base_setup and hands down this
    alias to all the tests. The tests use the base_setup method only through
    setup_method.
    """
    path_to_files = getattr(request.module, 'FILE_PATHS')

    for file_path in path_to_files:
        sparkl('put', file_path, IMPORT_DIR, alias=ALIAS)

    yield ALIAS
    sparkl('stop', IMPORT_DIR, alias=ALIAS)


@pytest.fixture(scope='session')
def base_setup():
    """
    Sets the test environment for all test modules.
    """

    # Collect login details from test settings.
    sse_url = read_from_config('sse_url')
    sse_user = read_from_config('sse_user')
    sse_pwd = read_from_config('sse_pass')

    # Set test environment, connect, login, create test folder
    sparkl('connect', sse_url, alias=ALIAS)
    sparkl('login', sse_user, sse_pwd, alias=ALIAS)
    sparkl('mkdir', IMPORT_DIR, alias=ALIAS)

    yield

    # Clean up after all tests have run.
    sparkl('rm', IMPORT_DIR, alias=ALIAS)
    sparkl('logout', alias=ALIAS)
    sparkl('close', alias=ALIAS)


@pytest.fixture(scope='module')
def listener_setup(request):
    """
    Starts a listener and evaluates the events.
    """
    listen_target = getattr(request.module, 'LISTEN_TARGET')

    # Create a listener process that puts events in a queue.
    event_queue, listen_process = start_listener_proc(listen_target, ALIAS)

    # The tests can get events from the queue
    # using the .get method, preferably with a timeout.
    yield event_queue

    # Terminate the listener process.
    listen_process.terminate()
