"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Traffic Lights Subroutines SPARKL mix in examples repo.
"""

import pytest
from tests.conftest import (IMPORT_DIR, OPERATION, EXP_RESPONSE,
                            CHECK_FUN, compare_values, run_tests)

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/TrafficSubr/Traf_Lig_Subr.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/Traf_Lig_Subr'.format(IMPORT_DIR)

# Path to tested operations in the user tree.
GET_MODE_OP = '{}/MasterFolder/MasterMix/Get/GetMode'.format(USER_TREE_PATH)
TEST_OP = '{}/MasterFolder/MasterMix/MasterTest/' \
          'StartTest'.format(USER_TREE_PATH)
WAIT_OP = '{}/SubrFolder/SubrMix/SubrGet/' \
          'IsPersonWaiting'.format(USER_TREE_PATH)

# Responses/replies sent by SPARKL.
OK_RESP = 'Ok'
TRAFFIC_RESP = 'Traffic'
NO_RESP = 'No'


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_traffic_states(output_fields):
    """
    Checks service (traffic) states are as expected.
    """
    states = output_fields['test_states']
    traffic_state = states['traffic']
    expected_traffic_state = 'red'
    compare_values(expected_traffic_state, traffic_state)

    pedestrian_state = states['pedestrian']
    expected_ped_state = 'green'
    compare_values(expected_ped_state, pedestrian_state)


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

    # Test operation presses pedestrian button, expected service states are:
    #   traffic: red
    #   pedestrian: green
    {
        OPERATION: TEST_OP,
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_traffic_states},

    # Test GetMode operation. Expects Traffic reply.
    {
        OPERATION: GET_MODE_OP,
        EXP_RESPONSE: TRAFFIC_RESP},

    # Test IsPersonWaiting operation. Expects No reply.
    {
        OPERATION: WAIT_OP,
        EXP_RESPONSE: NO_RESP}
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_traffic_subr(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
