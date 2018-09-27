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

Test cases for Lib SMS SPARKL mix in examples repo.
"""
import pytest

# IMPORT_DIR is the default folder in the SPARKL user tree
# your test files are imported to for testing
# setup method in conftest creates it for the tests and then deletes it
from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, \
    EXP_RESPONSE, TEST_NAME, MINERS, MINER_FUN, MINER_ARGS, EXP, \
    run_tests, read_from_config

from tests.filters import match_state_change

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

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

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
        TEST_NAME: 'test_set_api',
        OPERATION: SET_STATE_OP,
        INPUT_FIELDS: [(ACC_SID_FLD, TWILIO_SID),
                       (AUTH_FLD, TWILIO_PWD),
                       (FROM_FLD, TWILIO_NUMBER)],
        EXP_RESPONSE: OK_RESP,

        # State of SMS service must change.
        MINERS: [
            {
                MINER_FUN: match_state_change,
                MINER_ARGS: ('SMS',),
                EXP: 1
            }
        ]},

    # Tests SendMessageSecure solicit. Expects Ok response.
    {
        TEST_NAME: 'test_solicit',
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(ACC_SID_FLD, TWILIO_SID),
                       (AUTH_FLD, TWILIO_PWD),
                       (FROM_FLD, TWILIO_NUMBER),
                       (MSG_FLD, TEST_MESSAGE),
                       (TO_FLD, TEST_NUMBER)],
        EXP_RESPONSE: OK_RESP,

        # State has already changed, there should be no second change.
        MINERS: [
            {
                MINER_FUN: match_state_change,
                MINER_ARGS: ('SMS',),
                EXP: 0
            }
        ]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_lib_sms(test_data, session_setup, module_setup, listener_setup):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - session_setup:
            A setup method per test session. It handles connectins to SPARKL
            and starts the log writer co-routine.
        - module_setup:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session.
        - listener_setup:
            A setup method that starts the SPARKL listener and places
            events in a queue.
    """
    log_writer = session_setup
    alias = module_setup
    event_queue = listener_setup

    run_tests(alias, event_queue, log_writer, test_data)
