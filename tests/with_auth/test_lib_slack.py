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

Test cases for Crypto Portfolio SPARKL mix in examples repo.
"""
import pytest
from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, MINERS, \
    MINER_ARGS, MINER_FUN, TEST_NAME, EXP, run_tests, read_from_config

from tests.filters import match_event_with_field


# Collect link to test slack channel from environment variable.
SLACK_CHANNEL = read_from_config('slack_channel')

# Files to import for tests.
FILE_PATHS = ['Library/lib_slack/lib_slack.xml']

# SPARKL path to tested configuration.
USER_TREE_PATH = '{}/lib.slack'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Test input.
TEST_MAP = '{\"field1\": \"foo\", \"field2\": \"bar\"}'
TEST_MESSAGE_TEXT = '{\"text\": \"Test with simple text is successful.\"}'

# Path to tested operations.
SEND_URL_OP = '{}/Mix/SendMessageUrl'.format(USER_TREE_PATH)

# Input and output fields of the configuration.
COLOUR_FLD = 'colour'
HEADING_FLD = 'heading'
MAP_FLD = 'map'
URL_FLD = 'url'


##########################################################################
# Test data.
#
# Each set of data is used to call the parametrised test once.
# A set comprises:
#    - OPERATION:
#        The name of the operation to call
#    - EXP_RESPONSE:
#        The expected response/reply
#    - INPUT_FIELDS (optional):
#        The input fields and their values, if any
#    - OUTPUT_FIELDS (optional):
#        One or more output fields with their expected value
#    - CHECK_FUN (optional):
#        A function that makes extra assertions on the output values
#    - STOP_OR_NOT (optional):
#        A flag to indicate all running services must be stopped
#        before the test is run
##########################################################################
TEST_DATA = [
    # Test BuildMessage operation.
    # Expects built message to contain all the fields Slack requires.
    {
        TEST_NAME: 'test_send_url',
        OPERATION: SEND_URL_OP,
        INPUT_FIELDS: [
            (COLOUR_FLD, 'green'),
            (HEADING_FLD, 'BuildMessage test'),
            (MAP_FLD, TEST_MAP),
            (URL_FLD, SLACK_CHANNEL)],

        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'SendMessageUrl'),
                EXP: 1},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'SendMessageUrl'),
                EXP: 1}]
    },

    {
        TEST_NAME: 'test_send_url_simple',
        OPERATION: SEND_URL_OP,
        INPUT_FIELDS: [
            (COLOUR_FLD, 'amber'),
            (HEADING_FLD, 'Simple text test'),
            (MAP_FLD, TEST_MESSAGE_TEXT),
            (URL_FLD, SLACK_CHANNEL)],

        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'SendMessageUrl'),
                EXP: 1},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'SendMessageUrl'),
                EXP: 1}]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_lib_slack(test_data, base_setup, setup_method, listener_setup):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    event_queue = listener_setup
    log_writer = base_setup
    run_tests(alias, event_queue, log_writer, test_data)
