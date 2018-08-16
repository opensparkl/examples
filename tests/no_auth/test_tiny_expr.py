"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for TinyTable expr SPARKL mix in examples repo.
"""

import pytest
from tests.conftest import (IMPORT_DIR, OPERATION, INPUT_FIELDS,
                            OUTPUT_FIELDS, EXP_RESPONSE, CHECK_FUN, run_tests)

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/TinyTableExpr/TinyTable_Expr.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/TinyTable_expr'.format(IMPORT_DIR)

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


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_names(output_fields):
    """
    Checks all expected first and last names are in the database.
    """
    records = output_fields[RECORDS_FLD]
    expected_names = ['Bill', 'Door', 'King', 'Kong', 'Leonard', 'Cohen']
    assert all(name in records for name in expected_names)


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

    # Get existing record corresponding to ID 0.
    # Expects record to have:
    #   - First name: Bill
    #   - Last name: Door
    {
        OPERATION: GET_OP,
        INPUT_FIELDS: [('key', 0)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            FIRST_NAME_FLD: 'Bill',
            LAST_NAME_FLD: 'Door'}},

    # Get not existing record with ID 30. Expects Error response to solicit.
    {
        OPERATION: GET_OP,
        INPUT_FIELDS: [('key', 30)],
        EXP_RESPONSE: ERROR_RESP},

    # Insert new record. Expects Ok response to solicit.
    # Also expects the new record to receive ID 2.
    {
        OPERATION: INSERT_OP,
        INPUT_FIELDS: [('first_name', 'Leonard'),
                       ('last_name', 'Cohen')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            KEY_FLD: 2}},

    # List all records. Expects Ok response to solicit.
    {
        OPERATION: LIST_OP,
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_names},

    # Delete existing record. Expects Ok response to solicit.
    {
        OPERATION: DELETE_OP,
        INPUT_FIELDS: [('key', 1)],
        EXP_RESPONSE: OK_RESP},

    # Delete not existing record. Expects Error response to solicit.
    {
        OPERATION: DELETE_OP,
        INPUT_FIELDS: [('key', 4)],
        EXP_RESPONSE: ERROR_RESP}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_tiny_expr(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
