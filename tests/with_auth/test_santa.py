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

Test cases for Secret Santa SPARKL mix in examples repo.
Test also needs and import the Slack library.
"""

import json
import pytest

from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, \
    TEST_NAME, EXP_RESPONSE, OUTPUT_FIELDS, CHECK_FUN, \
    MINERS, MINER_FUN, MINER_ARGS, EXP, \
    run_tests, read_from_config

from tests.filters import match_state_change, match_event_with_field

# Collect link to test slack channel from environment variable.
SLACK_CHANNEL = read_from_config('slack_channel')

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Library/lib_slack/lib_slack.xml',
              'Examples/SecretSanta/SecretSanta.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/Santa'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Path to tested operations in the user tree.
START_OP = '{}/Mix/StartWithUrl'.format(USER_TREE_PATH)
BUILD_OP = '{}/Mix/SendSanta/BuildMessage'.format(USER_TREE_PATH)
PAIRS_OP = '{}/Mix/GetSanta/FormPairs'.format(USER_TREE_PATH)

# Test data.
ALL_PAIRS = ('[[{\"Jacoby\", \"foo.com\"}, {\"Miklos\", \"foo.com\"}],'
             '[{\"Yev\", \"foo.com\"}, {\"Mark\", \"foo.com\"}],'
             '[{\"Miklos\", \"foo.com\"}, {\"Jacoby\", \"foo.com\"}],'
             '[{\"Emily\", \"foo.com\"}, {\"Andrew\", \"foo.com\"}],'
             '[{\"Mark\", \"foo.com\"}, {\"Yev\", \"foo.com\"}],'
             '[{\"Andrew\", \"foo.com\"}, {\"Emily\", \"foo.com\"}]]')

EXP_NAMES = ['Yev', 'Miklos', 'Emily', 'Jacoby', 'Mark', 'Andrew']

# Input and output fields.
ALL_PAIRS_FLD = 'all_pairs'
HDG_FLD = 'heading'
MSG_FLD = 'map'
TEST_URL_FLD = 'start_url'
URL_FLD = 'url'
COLOUR_FLD = 'colour'

# Message keys
FROM_KEY = 'From'
TO_KEY = 'To'

# SPARKL responses/replies
OK_RESP = 'Ok'


#####################################################
# Additional check functions used by the test data. #
#####################################################


def erl_tuple_to_list(raw_data):
    """
    Formats Erlang data to be testable in Python.
    raw_data is a list of Erlang tuples serialised as string
    E.g.: '[{"giver1","recipient1"},{"giver2","recipient2"}]'
    formatted_list is a list of lists:
    E.g.:[ ['giver1','recipient1'], ['giver2','recipient2'] ]
    """
    # Replace Erlang tuple chars (and binary strings) with json list chars.
    replacements = {
        '{': '[',
        '}': ']',
        '<<': '',
        '>>': ''
    }

    for old_val, new_val in replacements.items():
        raw_data = raw_data.replace(old_val, new_val)

    # Deserialise into list of lists
    formatted_list = json.loads(raw_data)

    return formatted_list


def check_pairs(output_fields):
    """
    No one can send a message to him/herself. Check
    all pairs are made up of different people.
    """
    pairs = output_fields[ALL_PAIRS_FLD]
    formatted_pairs = erl_tuple_to_list(pairs)
    pairs_error = 'Giver and recipient cannot be the same person.'

    assert all(x[0] != x[1]
               for x in formatted_pairs), pairs_error


def check_build(output_fields):
    """
    Checks whether the SLACK message is as expected.
    """
    heading = output_fields[HDG_FLD]
    message = output_fields[MSG_FLD]
    giver = message[FROM_KEY]
    recipient = message[TO_KEY]

    giver_error = '{} not in list of expected givers : {}'.format(
        giver, EXP_NAMES)
    recipient_error = '{} not in list of expected recipients : {}'.format(
        recipient, EXP_NAMES)

    assert giver in EXP_NAMES, giver_error
    assert giver in heading, 'Heading must contain name of {}: {}'.format(
        giver, heading)
    assert recipient in EXP_NAMES, recipient_error
    assert recipient in heading, 'Heading must contain name of {}: {}'.format(
        recipient, heading)
    assert giver != recipient, 'Giver and recipient must not be the same.'


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

    # Test full Santa mix.
    {
        TEST_NAME: 'test_full',
        OPERATION: START_OP,
        INPUT_FIELDS: [(TEST_URL_FLD, SLACK_CHANNEL)],
        MINERS: [

            # Build message must happen 7 times, on the 7th time it
            # responds with Done.
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'BuildMessage'),
                EXP: 7
            },

            # Done reply must be sent once.
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('reply', 'Done'),
                EXP: 1
            },

            # Message must be sent 6 times.
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'SendMessageUrl'),
                EXP: 6
            },

            # There should be one state change when service
            # state is updated with proper URLs.
            {
                MINER_FUN: match_state_change,
                MINER_ARGS: ('Santas', ),
                EXP: 1
            }
        ]
    },

    # Check pairs are output correctly.
    {
        TEST_NAME: 'test_pairs',
        OPERATION: PAIRS_OP,
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_pairs
    },

    # Test BuildMessage operation.
    # Expects correctly built output fields.
    {
        TEST_NAME: 'test_build_msg',
        OPERATION: BUILD_OP,
        INPUT_FIELDS: [(ALL_PAIRS_FLD, ALL_PAIRS)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            COLOUR_FLD: 'green',
            URL_FLD: 'foo.com'},
        CHECK_FUN: check_build}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_santa(test_data, base_setup, setup_method, listener_setup):
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
