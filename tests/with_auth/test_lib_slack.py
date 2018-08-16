"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Crypto Portfolio SPARKL mix in examples repo.
"""
import pytest
from tests.conftest import (IMPORT_DIR, OPERATION, INPUT_FIELDS, EXP_RESPONSE,
                            CHECK_FUN, run_tests, read_from_config)

# Collect link to test slack channel from environment variable.
SLACK_CHANNEL = read_from_config('slack_channel')

# Messages sent to this Slack channel must come back with error.
WRONG_SLACK_CHANNEL = 'https://hooks.slack.com/services/bla/bla/bla'

# Files to import for tests.
FILE_PATHS = ['Library/lib_slack/lib_slack.xml']

# SPARKL path to tested configuration.
USER_TREE_PATH = '{}/lib.slack'.format(IMPORT_DIR)

# Test input.
TEST_MAP = '{\"field1\": \"foo\", \"field2\": \"bar\"}'
TEST_MESSAGE_TEXT = '{\"text\": \"Test with simple text is successful.\"}'

# Keys expected by SLACK.
EXPECTED_MESSAGE_KEYS = ['color', 'fallback', 'fields', 'pretext']

# Path to tested operations.
SOLICIT_OP = '{}/Mix/Test/Start'.format(USER_TREE_PATH)
BUILD_OP = '{}/Mix/Test/BuildMessage'.format(USER_TREE_PATH)
SEND_OP = '{}/Mix/Test/SendToSlack'.format(USER_TREE_PATH)

# Input and output fields of the configuration.
TEST_COLOUR_FLD = 'test_colour'
TEST_HEADING_FLD = 'test_heading'
TEST_MAP_FLD = 'test_map'
TEST_URL_FLD = 'test_url'
TEST_MSG_FLD = 'test_message'

# SPARKL replies/responses.
OK_RESP = 'Ok'
ERROR_RESP = 'Error'


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_msg_keys(output_fields):
    """
    Checks whether the constructed message dict
    has all the keys expected by SLACK.
    """
    message = output_fields[TEST_MSG_FLD]
    message_keys = list(message.keys())
    message_keys.sort()
    message_keys_error = 'Expected keys are {}, ' \
                         'not {}.'.format(EXPECTED_MESSAGE_KEYS, message_keys)
    assert message_keys == EXPECTED_MESSAGE_KEYS, message_keys_error


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
        OPERATION: BUILD_OP,
        INPUT_FIELDS: [
            (TEST_COLOUR_FLD, 'green'),
            (TEST_HEADING_FLD, 'BuildMessage test'),
            (TEST_MAP_FLD, TEST_MAP)],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_msg_keys},

    # Test SendToSlack operation. Expects Ok reply.
    {
        OPERATION: SEND_OP,
        INPUT_FIELDS: [(TEST_MSG_FLD, TEST_MESSAGE_TEXT),
                       (TEST_URL_FLD, SLACK_CHANNEL)],
        EXP_RESPONSE: OK_RESP},

    # Test SendToSlack operation with wrong URL. Expects Error reply.
    {
        OPERATION: SEND_OP,
        INPUT_FIELDS: [(TEST_MSG_FLD, TEST_MESSAGE_TEXT),
                       (TEST_URL_FLD, WRONG_SLACK_CHANNEL)],
        EXP_RESPONSE: ERROR_RESP},

    # Test Start solicit operation - i.e. full transaction.
    # Expects a message with all the fields Slack requires.
    {
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(TEST_COLOUR_FLD, 'red'),
                       (TEST_HEADING_FLD, 'Full solicit test with fields'),
                       (TEST_MAP_FLD, TEST_MAP),
                       (TEST_URL_FLD, SLACK_CHANNEL)],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_msg_keys}
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_lib_slack(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
