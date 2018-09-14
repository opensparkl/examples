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

Test cases for Primes expr SPARKL mix in examples repo.
"""

import pytest
from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, EXP_RESPONSE, \
    TEST_NAME, OUTPUT_FIELDS, run_tests

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/PrimesExpr/Primes_expr.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/Primes_expr'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = '{}/Sequencer'.format(USER_TREE_PATH)

# Path to tested operations in the user tree.
SOLICIT_OP = '{}/Primes_expr/Mix/Frontend/CheckPrime'.format(IMPORT_DIR)
FIRST_DIV_OP = '{}/Primes_expr/Mix/Backend/FirstDivisor'.format(IMPORT_DIR)
TEST_OP = '{}/Primes_expr/Mix/Backend/Test'.format(IMPORT_DIR)
ITERATE_OP = '{}/Primes_expr/Mix/Backend/Iterate'.format(IMPORT_DIR)

# Input and output fields.
N_FLD = 'n'
DIV_FLD = 'div'

# Responses/replies sent by SPARKL.
OK_RESP = 'Ok'
YES_RESP = 'Yes'
NO_RESP = 'No'
MAYBE_RESP = 'Maybe'

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
    # Test full transaction with prime number. Expects Yes response.
    {
        TEST_NAME: 'test_solicit_13',
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(N_FLD, 13)],
        EXP_RESPONSE: YES_RESP},

    # Test full transaction with not prime number. Expects No response.
    {
        TEST_NAME: 'test_solicit_66',
        OPERATION: SOLICIT_OP,
        INPUT_FIELDS: [(N_FLD, 66)],
        EXP_RESPONSE: NO_RESP},

    # Test FirstDivisor operation. Expects div field to be 2.
    {
        TEST_NAME: 'test_first_div',
        OPERATION: FIRST_DIV_OP,
        INPUT_FIELDS: [(N_FLD, 66)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            DIV_FLD: 2}},

    # Test the Test request. Expects Maybe reply to request.
    {
        TEST_NAME: 'test_test_op',
        OPERATION: TEST_OP,
        INPUT_FIELDS: [(N_FLD, 13),
                       (DIV_FLD, 2)],
        EXP_RESPONSE: MAYBE_RESP},

    # Test Iterate consume/reply with first divisor(2).
    # Expects new divisor to be 3.
    {
        TEST_NAME: 'test_iterate_op_13_2',
        OPERATION: ITERATE_OP,
        INPUT_FIELDS: [(N_FLD, 13),
                       (DIV_FLD, 2)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            DIV_FLD: 3}},

    # Test Iterate consume/reply with a divisor of 3.
    # Expects new divisor to be 5.
    {
        TEST_NAME: 'test_iterate_op_39_3',
        OPERATION: ITERATE_OP,
        INPUT_FIELDS: [(N_FLD, 39),
                       (DIV_FLD, 3)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            DIV_FLD: 5}}
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_primes_expr(test_data, base_setup, setup_method, listener_setup):
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
