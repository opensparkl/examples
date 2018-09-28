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

Test cases for Traffic Lights Subroutines SPARKL mix in examples repo.
"""

import pytest
from tests.conftest import IMPORT_DIR, OPERATION, EXP_RESPONSE, TEST_NAME, \
    MINERS, MINER_FUN, MINER_ARGS, MINER_KWARGS, EXP, run_tests

from tests.filters import match_event_with_field, match_state_change

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/TrafficSubr/Traf_Lig_Subr.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/Traf_Lig_Subr'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Path to tested operations in the user tree.
GET_MODE_OP = '{}/MasterFolder/MasterMix/Get/GetMode'.format(USER_TREE_PATH)

WAIT_OP = '{}/SubrFolder/SubrMix/SubrGet/' \
          'IsPersonWaiting'.format(USER_TREE_PATH)

SET_PEOPLE = '{}/MasterFolder/MasterMix/Set/SetPeople'.format(USER_TREE_PATH)

# Responses/replies sent by SPARKL.
OK_RESP = 'Ok'
TRAFFIC_RESP = 'Traffic'
NO_RESP = 'No'

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

    # Test GetMode operation. Expects Traffic reply.
    {
        TEST_NAME: 'Test_GetMode',
        OPERATION: GET_MODE_OP,
        EXP_RESPONSE: TRAFFIC_RESP,

        # Expects one request event and the reply to it.
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('request', 'GetMode'),
             EXP: 1},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('reply', 'Traffic'),
             EXP: 1}
        ]},


    # Test IsPersonWaiting operation. Expects No reply.
    {
        TEST_NAME: 'Test_IsPersonWaiting',
        OPERATION: WAIT_OP,
        EXP_RESPONSE: NO_RESP,

        # Expects one request event and the reply to it.
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('request', 'IsPersonWaiting'),
             EXP: 1},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('reply', 'No'),
             EXP: 1}
        ]},

    {
        TEST_NAME: 'TestSetPeopleMode',
        OPERATION: SET_PEOPLE,
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('consume', 'SetPeople'),
             EXP: 1},

            # Expects the Junction service's state to change.
            {MINER_FUN: match_state_change,
             MINER_ARGS: ('Junction',),
             MINER_KWARGS: {
                 'exp_new': {
                     'PedLight': 'green',
                     'TrafLight': 'red'}},
             EXP: 1}
        ]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_traffic_subr(test_data, session_setup, module_setup, listener_setup):
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
