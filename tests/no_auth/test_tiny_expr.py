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

Test cases for TinyTable expr SPARKL mix in examples repo.
"""

import pytest
from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, \
    OUTPUT_FIELDS, EXP_RESPONSE, CHECK_FUN, TEST_NAME, \
    MINERS, MINER_FUN, MINER_ARGS, MINER_KWARGS, EXP, run_tests

from tests.filters import match_state_change

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/TinyTableExpr/TinyTable_Expr.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/TinyTable_expr'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Path to tested operations in the user tree.
DELETE_OP = '{}/TinyTable_expr/Mix/Client/DeleteName'.format(IMPORT_DIR)
GET_OP = '{}/TinyTable_expr/Mix/Client/GetName'.format(IMPORT_DIR)
INSERT_OP = '{}/TinyTable_expr/Mix/Client/InsertName'.format(IMPORT_DIR)
LIST_OP = '{}/TinyTable_expr/Mix/Client/ListNames'.format(IMPORT_DIR)

# SPARKL responses/replies
OK_RESP = 'Ok'
ERROR_RESP = 'Error'

# Input/output fields
FIRST_NAME_FLD = 'first_name'
LAST_NAME_FLD = 'last_name'
KEY_FLD = 'key'
RECORDS_FLD = 'records'

EXP_NAMES = ['Bill', 'Door', 'King', 'Kong', 'Leonard', 'Cohen']


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_names(output_fields):
    """
    Checks all expected first and last names are in the database.
    """
    records = output_fields[RECORDS_FLD]
    assert all(name in records for name in EXP_NAMES)


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
#   - MINERS (optional):
#       A list of functions that filter and check SPARKL event logs.
##########################################################################
TEST_DATA = [

    # Get existing record corresponding to ID 0.
    # Expects record to have:
    #   - First name: Bill
    #   - Last name: Door
    {
        TEST_NAME: 'test_get_valid',
        OPERATION: GET_OP,
        INPUT_FIELDS: [('key', 0)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            FIRST_NAME_FLD: 'Bill',
            LAST_NAME_FLD: 'Door'}},

    # Get non-existent record with ID 30. Expects Error response to solicit.
    {
        TEST_NAME: 'test_get_invalid',
        OPERATION: GET_OP,
        INPUT_FIELDS: [('key', 30)],
        EXP_RESPONSE: ERROR_RESP},

    # Insert new record. Expects Ok response to solicit.
    # Also expects the new record to receive ID 2.
    {
        TEST_NAME: 'test_insert',
        OPERATION: INSERT_OP,
        INPUT_FIELDS: [('first_name', 'Leonard'),
                       ('last_name', 'Cohen')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            KEY_FLD: 2},

        # Also expects a state change event. NextKey
        # must change from 2 to 3.
        MINERS: [
            {MINER_FUN: match_state_change,
             MINER_ARGS: ('Database',),
             MINER_KWARGS: {
                 'exp_new': {
                     'NextKey': 3},

                 'exp_old': {
                     'NextKey': 2}},
             EXP: 1}

        ]},

    # List all records. Expects Ok response to solicit.
    {
        TEST_NAME: 'list_names',
        OPERATION: LIST_OP,
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_names},

    # Delete existing record. Expects Ok response to solicit.
    {
        TEST_NAME: 'delete_valid',
        OPERATION: DELETE_OP,
        INPUT_FIELDS: [('key', 1)],
        EXP_RESPONSE: OK_RESP,

        MINERS: [

            {MINER_FUN: match_state_change,
             MINER_ARGS: ('Database',),
             MINER_KWARGS: {
                 'exp_new': {
                     'NextKey': 3}},
             EXP: 1}]
    },

    # Delete non-existent record. Expects Error response to solicit.
    {
        TEST_NAME: 'delete_invalid',
        OPERATION: DELETE_OP,
        INPUT_FIELDS: [('key', 4)],
        EXP_RESPONSE: ERROR_RESP,

        MINERS: [

            {MINER_FUN: match_state_change,
             MINER_ARGS: ('Database',),
             EXP: 0}]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_tiny_expr(test_data, base_setup, setup_method, listener_setup):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    event_queue = listener_setup
    log_writer = base_setup
    alias = setup_method

    run_tests(alias, event_queue, log_writer, test_data)
