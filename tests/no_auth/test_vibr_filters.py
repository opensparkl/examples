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

Test cases for Vibration filters SPARKL mix in examples repo.
"""
import pytest
from random import randint

from tests.conftest import IMPORT_DIR, TEST_NAME, OPERATION, \
    INPUT_FIELDS, MINERS, MINER_FUN, MINER_ARGS, EXP, \
    run_tests

from tests.filters import match_event_with_field

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/FilteredVibrations/FilteredVibrations.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/FilteredVibrations'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Notify to kick off the subroutines.
NOTIFY = '{}/Vibration/MasterMix/GenVibr'.format(USER_TREE_PATH)


# Parametrised test data. test_vibr is invoked once per item in list.
# Each test generates a random integer value between two given thresholds.
# The value between the thresholds should only trigger one alert.
TEST_DATA = [
    {
        TEST_NAME: 'TestGreenAlert',
        OPERATION: NOTIFY,
        INPUT_FIELDS: [('vibration', randint(0, 30))],
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'GreenAlert'),
             EXP: 1},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'AmberAlert'),
             EXP: 0},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'RedAlert'),
             EXP: 0}]},

    {
        TEST_NAME: 'TestAmberAlert',
        OPERATION: NOTIFY,
        INPUT_FIELDS: [('vibration', randint(31, 69))],
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'AmberAlert'),
             EXP: 1},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'GreenAlert'),
             EXP: 0},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'RedAlert'),
             EXP: 0}]},

    {
        TEST_NAME: 'TestRedAlert',
        OPERATION: NOTIFY,
        INPUT_FIELDS: [('vibration', randint(70, 100))],
        MINERS: [
            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'RedAlert'),
             EXP: 1},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'GreenAlert'),
             EXP: 0},

            {MINER_FUN: match_event_with_field,
             MINER_ARGS: ('notify', 'GreenAlert'),
             EXP: 0}]}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_vibr(test_data, session_setup, module_setup, listener_setup):
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
