"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Lib SMS SPARKL mix in examples repo.
"""
import pytest

# IMPORT_DIR is the default folder in the SPARKL user tree
# your test files are imported to for testing
# setup method in conftest creates it for the tests and then deletes it
from tests.conftest import (IMPORT_DIR, OPERATION, INPUT_FIELDS,
                            EXP_RESPONSE, run_tests, read_from_config)

# Environment variables used by test.
TWILIO_SID = read_from_config('twilio_sid')
TWILIO_PWD = read_from_config('twilio_pass')
TWILIO_NUMBER = read_from_config('twilio_number')
TEST_NUMBER = read_from_config('test_number')

# List of file paths to one or more SPARKL mixes your test needs.
# The setup method uses the path(s) to import your configuration(s)
FILE_PATHS = ['Library/lib_sms/sms_lib.xml']

# The path to the root folder of your mix in the SPARKL user tree.
USER_TREE_PATH = '{}/lib.sms'.format(IMPORT_DIR)

# Message sent in SMS by one of the tests.
TEST_MESSAGE = 'Lib sms test succesful!'

# The path to all tested operations in the user tree.
SOLICIT_OP = '{}/Mix/SendMessageSecure'.format(USER_TREE_PATH)
SET_STATE_OP = '{}/Mix/Impl/SetAPIKeys'.format(USER_TREE_PATH)

# Responses/replies sent by SPARKL.
OK_RESP = 'Ok'

# Input fields used by the operations.
ACC_SID_FLD = 'acc_sid'
AUTH_FLD = 'auth_token'
FROM_FLD = 'from'
MSG_FLD = 'message'
TO_FLD = 'to'

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

    # Tests SetAPIKeys operation. Expects Ok reply.
    {
        OPERATION: SET_STATE_OP,
        INPUT_FIELDS: [(ACC_SID_FLD, TWILIO_SID),
                       (AUTH_FLD, TWILIO_PWD),
                       (FROM_FLD, TWILIO_NUMBER)],
        EXP_RESPONSE: OK_RESP},

    # Tests SendMessageSecure solicit. Expects Ok response.
    {
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(ACC_SID_FLD, TWILIO_SID),
                       (AUTH_FLD, TWILIO_PWD),
                       (FROM_FLD, TWILIO_NUMBER),
                       (MSG_FLD, TEST_MESSAGE),
                       (TO_FLD, TEST_NUMBER)],
        EXP_RESPONSE: OK_RESP}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_lib_sms(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
