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

Template for writing tests.
"""

import pytest


from tests.conftest import IMPORT_DIR, OPERATION, EXP_RESPONSE, INPUT_FIELDS, \
    TEST_NAME, CHECK_FUN, OUTPUT_FIELDS, MINERS, MINER_FUN, MINER_ARGS, EXP, \
    run_tests

from tests.filters import match_event_with_field

# Path to one or more SPARKL mixes your test needs.
# The setup method uses the path(s) to import your configuration(s).
# The setup method assumes you run the tests from the root folder.
# E.g. FILE_PATHS = ['Examples/PrimesExpr/Primes_expr.xml']
FILE_PATHS = ['PATH_TO_MIX_ON_FILE_SYSTEM']

# The SPARKL path to the tested mix.
USER_TREE_PATH = "{}/TOPMOST_MIX_FOLDER".format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_output(output_fields):
    """
    Sample helper function used to check the output fields
    sent by SPARKL. It is referenced by the set of test data
    below.

    Each helper function takes as parameter a dictionary
    that contains all output fields. E.g.:
        {
            'sample_out_field1' : 3,
            'sample_out_field2': 'some_string'}
    """
    output_field = output_fields['output_field_name']
    assert isinstance(output_field, str), '{} must be a ' \
                                          'string!'.format(output_field)


##########################################################################
# Test data.
#
# Each set of data is used to call the parameterised test once.
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

    # Add your specific test data thus:
    {
        TEST_NAME: 'name_of_test_case',
        OPERATION: 'Scratch/test/mix/foo',
        INPUT_FIELDS: [('field_name', 'field_value')],
        EXP_RESPONSE: 'Ok',
        OUTPUT_FIELDS: {
            'output_field_name': 'output_field_value'},
        CHECK_FUN: check_output,
        MINERS: [
            {
                # Expects one notify event after firing Scratch/test/mix/foo.
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'foo'),
                EXP: 1
            }
        ]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_my_test(test_data, base_setup, setup_method, listener_setup):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session.
    """
    alias = setup_method

    event_queue = listener_setup
    log_writer = base_setup

    run_tests(alias, event_queue, log_writer, test_data)
