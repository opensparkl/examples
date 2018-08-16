"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Secret Santa SPARKL mix in examples repo.
Test also needs and import the Slack library.
"""

import json
import pytest

from tests.conftest import (IMPORT_DIR, OPERATION, INPUT_FIELDS, EXP_RESPONSE,
                            OUTPUT_FIELDS, CHECK_FUN, run_tests,
                            read_from_config)

# Collect link to test slack channel from environment variable.
SLACK_CHANNEL = read_from_config('slack_channel')

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Library/lib_slack/lib_slack.xml',
              'Examples/SecretSanta/SecretSanta.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/Santa'.format(IMPORT_DIR)

# Path to tested operations in the user tree.
SOLICIT_OP = '{}/Mix/Test/StartTest'.format(USER_TREE_PATH)
BUILD_OP = '{}/Mix/SendSanta/BuildMessage'.format(USER_TREE_PATH)

# Test data.
ALL_PAIRS = ('[[{\"Jacoby\", \"foo.com\"}, {\"Miklos\", \"foo.com\"}],'
             '[{\"Yev\", \"foo.com\"}, {\"Mark\", \"foo.com\"}],'
             '[{\"Miklos\", \"foo.com\"}, {\"Jacoby\", \"foo.com\"}],'
             '[{\"Emily\", \"foo.com\"}, {\"Andrew\", \"foo.com\"}],'
             '[{\"Mark\", \"foo.com\"}, {\"Yev\", \"foo.com\"}],'
             '[{\"Andrew\", \"foo.com\"}, {\"Emily\", \"foo.com\"}]]')

# Input and output fields.
PAIRS_FLD = 'pairs_state'
ALL_PAIRS_FLD = 'all_pairs'
HDG_FLD = 'heading'
MSG_FLD = 'message'
TEST_URL_FLD = 'test_url'
URL_FLD = 'url'
COLOUR_FLD = 'colour'
MSG_SENT_FLD = 'messages_sent'

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
    # Replace Erlang tuple chars with json list chars
    formatted_data = raw_data.replace('{', '[').replace('}', ']')

    # Deserialise into list of lists
    formatted_list = json.loads(formatted_data)

    return formatted_list


def check_solicit(output_fields):
    """
    Checks whether giver and recipient are the same in any of the pairs.
    """
    pairs = output_fields[PAIRS_FLD]

    formatted_pairs = erl_tuple_to_list(pairs)

    pairs_error = 'Giver and recipient cannot be the same person.'

    assert all(x[0] != x[1]
               for x in formatted_pairs), pairs_error


def check_build(output_fields):
    """
    Checks whether the SLACK message is as expected.
    """
    expected_names = ['Yev', 'Miklos', 'Emily', 'Jacoby', 'Mark', 'Andrew']

    heading = output_fields[HDG_FLD]
    message = output_fields[MSG_FLD]
    giver = message[FROM_KEY]
    recipient = message[TO_KEY]

    giver_error = '{} not in list of expected givers : {}'.format(
        giver, expected_names)
    recipient_error = '{} not in list of expected recipients : {}'.format(
        recipient, expected_names)

    assert giver in expected_names, giver_error
    assert giver in heading, 'Heading must contain name of {}: {}'.format(
        giver, heading)
    assert recipient in expected_names, recipient_error
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
    # Expects:
    #   Starting and ending state
    #   Correct giver/recipient pairs
    #   i.e. giver and recipient must not be the same
    {
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(TEST_URL_FLD, SLACK_CHANNEL)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            MSG_SENT_FLD: 6},
        CHECK_FUN: check_solicit},

    # Test BuildMessage operation.
    # Expects correctly built output fields.
    {
        OPERATION: BUILD_OP,
        INPUT_FIELDS: [(ALL_PAIRS_FLD, ALL_PAIRS)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            COLOUR_FLD: 'green',
            URL_FLD: 'foo.com'},
        CHECK_FUN: check_build}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_santa(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
