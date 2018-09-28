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

Test harness for testing SPARKL sample configs in examples repo.
"""
import subprocess
from multiprocessing import Process, Queue
from queue import Empty
from time import sleep

import tempfile
import uuid
import os
import json
import pytest

from sparkl_cli.main import sparkl
from tests.write_test_log_html import start_test_log, write_log, stop_test_log

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
TEST_NAME = 'name'
MINERS = 'miners'
MINER_FUN = 'miner_fun'
MINER_ARGS = 'miner_args'
MINER_KWARGS = 'miner_kwargs'
EXP = 'exp'
MATCHED = 'matched'
ERROR = 'error'

# Error messages
FLOAT_ERROR = 'The value of \'{}\' must be a float.'
ZERO_ERROR = 'The value of \'{}\' must not be zero.'


class ChDir:
    """
    Context manager for stepping into a directory temporarily.

    Usage:

    with ChDir(path):
        do_stuff()
    """

    def __init__(self, path):
        """
        Saves the old and new directory.
        """
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        """
        Enters into the new directory.
        """
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        """
        Returns to the original directory.
        """
        os.chdir(self.old_dir)


def start_service_in(sparkl_path, module_name, watchdog_path,
                     **kwargs):
    """
    Maps a SPARKL service to its implementation using `sparkl service`.
        - sparkl_path:
            The path to the SPARKL service in the user tree
        - module_name:
            The name of the implementation module (without the suffix)
        - watchdog_path:
            The directory in which the `sparkl service` command is executed
            (and the Python watchdog is started)
    """

    # Filter kwargs for `sparkl service`
    service_kwargs = dict()
    for key, value in kwargs.items():
        if key in ['path', 'alias']:
            service_kwargs[key] = value

    # Start the SPARKL service in the specified directory.
    with ChDir(watchdog_path):
        sparkl('service', sparkl_path, module_name,
               **service_kwargs)

        # Give the watchdog time to start.
        sleep(kwargs.get('wait', 3))


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


def match_error_event(event, *_args):
    """
    Matches error events.
    Returns True or False.
    """
    return event['tag'] == 'error'


def mine_event(event, miners):
    """
    Matches the event against the miner's filter
    function.
    """
    for miner in miners:
        fun = miner[MINER_FUN]
        args = miner.get(MINER_ARGS, ())
        kwargs = miner.get(MINER_KWARGS, {})

        if fun(event, *args, **kwargs):
            miner[MATCHED] = miner[MATCHED] + 1 if MATCHED in miner else 1

    return miners


def test_fail_msg(exp, test_name, miner_name, matched=0):
    """
    Formats message string for false test assertion.
        - exp:
            Expected number of events (to be matched).
        - test_name:
            Name of running test.
        - miner_name:
            Name of miner function.
        - matched:
            Number of events matched with miner function.
            By default it's 0.
    """
    return 'Expected to match {} events, not {} in {} with {}.'.format(
        exp, matched, test_name, miner_name)


def assert_miners(miners, test_name):
    """
    Checks whether each miner matched the
    expected number of events - if any.
    """
    for miner in miners:

        # If miner did not match any event, expected must have been zero.
        if MATCHED not in miner:
            assert miner[EXP] == 0, test_fail_msg(
                miner[EXP], test_name, miner[MINER_FUN].__name__)

        else:
            assert miner[MATCHED] == miner[EXP], test_fail_msg(
                miner[EXP], test_name, miner[MINER_FUN].__name__,
                matched=miner[MATCHED])


def assert_events(event_queue, log_writer, test_name, miners=None):
    """
    Processes SPARKL events received during the test run.
    The events are placed into a queue by a separate process.

        - event_queue:
            The tests try to retrieve the events from this queue.
        - log_writer:
            A co-routine. It writes events to a log file.
        - test_name:
            The name of the running test case.
        - miners:
            Optional filter functions. Some of the tests expect specific
            events to happen. The miners make sure they do.
    """
    received = 1

    # Error events should not happen.
    # Default miner is added to miners in all cases.
    def_miner = {
        MINER_FUN: match_error_event,
        EXP: 0}

    miners = miners + [def_miner] if miners else [def_miner]

    while True:
        try:
            event = event_queue.get(timeout=1)

            write_log(event, test_name, received, log_writer)
            received += 1

            mine_event(event, miners)

        except Empty:
            break

    assert_miners(miners, test_name)


def assert_result(result, **kwargs):
    """
    Checks the SPARKL response to the tested operation.
    """
    try:
        formatted_result = format_response_data(result)

        if EXP_RESPONSE in kwargs:
            compare_response(
                kwargs[EXP_RESPONSE], formatted_result['response'])

        if OUTPUT_FIELDS in kwargs:
            for key, exp_value in kwargs[OUTPUT_FIELDS].items():
                act_value = formatted_result['fields'][key]
                compare_values(exp_value, act_value)

        if CHECK_FUN in kwargs:
            kwargs[CHECK_FUN](formatted_result['fields'])

    except KeyError:
        assert False, 'Unexpected result: {}.'.format(json.dumps(result))


def run_tests(alias, event_queue, log_writer, test_data):
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
    # Stop all services in test directory if test requires so.
    if STOP_OR_NOT in test_data:
        sparkl('stop', IMPORT_DIR, alias=alias)

    # Set field values if the test specifies input data for the operation.
    if INPUT_FIELDS in test_data:
        sparkl('vars', literal=test_data[INPUT_FIELDS], alias=alias)

    # Call SPARKL operation and gather results.
    result = sparkl('call', test_data[OPERATION], alias=alias)

    # Check whether the expected events are received.
    assert_events(event_queue, log_writer, test_data[TEST_NAME],
                  miners=test_data.get(MINERS, None))

    # Check whether the tested operation returned the expected response.
    assert_result(result, **test_data)


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
    sleep(1)
    return event_queue, listen_process


@pytest.fixture(scope='module')
def file_sync_setup(request):
    """
    Setup and teardown for testing the file_sync demo.
    """

    # Create two temporary directories.
    master_dir = tempfile.mkdtemp()
    slave_dir = tempfile.mkdtemp()

    # Collect constants from the file_sync test module.
    master_service = getattr(request.module, 'MASTER_SERVICE')
    slave_service = getattr(request.module, 'SLAVE_SERVICE')
    path_to_modules = getattr(request.module, 'PATH_TO_MIX_DIR')

    # Start the master and slave watchdogs.
    start_service_in(master_service, 'master', master_dir,
                     alias=ALIAS, path=path_to_modules)
    start_service_in(slave_service, 'slave', slave_dir,
                     alias=ALIAS, path=path_to_modules)

    yield master_dir, slave_dir

    # Stop the services and remove the temp dirs.
    sparkl('stop', master_service, alias=ALIAS)
    sparkl('stop', slave_service, alias=ALIAS)
    subprocess.check_call(['rm', '-rf', master_dir])
    subprocess.check_call(['rm', '-rf', slave_dir])


@pytest.fixture(scope='module')
def module_setup(request):
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
def session_setup():
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

    # Start test log writer.
    log_writer, log_handle = start_test_log()

    # Each test can access it.
    yield log_writer

    # Clean up after all tests have run.
    sparkl('rm', IMPORT_DIR, alias=ALIAS)
    sparkl('logout', alias=ALIAS)
    sparkl('close', alias=ALIAS)

    # Close log file and writer co-routine.
    stop_test_log(log_writer, log_handle)


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
