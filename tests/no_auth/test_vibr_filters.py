"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Vibration filters SPARKL mix in examples repo.
"""

import pytest
from queue import Empty
from random import randint
from sparkl_cli.main import sparkl
from tests.conftest import IMPORT_DIR

# Configuration(s) imported by the test setup.
FILE_PATHS = ['Examples/FilteredVibrations/FilteredVibrations.xml']

# Path to the tested operation in SPARKL.
USER_TREE_PATH = '{}/FilteredVibrations'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = '{}/Sequencer'.format(USER_TREE_PATH)

# Notify to kick off the subroutines.
NOTIFY = '{}/Vibration/MasterMix/GenVibr'.format(USER_TREE_PATH)

# Subroutine notify operations.
ALERT_NOTIFIES = ['GreenAlert', 'AmberAlert', 'RedAlert']


def get_event_name(event, event_type, short=True):
    """
    Retrieves the name of an event.
        - event:
            The event as returned by `sparkl listen`.
        - event_type:
            The type of the event, e.g. notify.
        - short:
            An optional value. The event name is a full path.
            The short version returns only the actual event name.
    """
    name = event['attr'][event_type]
    if short:
        name = name.split('/')[-1]

    return name


def match_name(event, event_type, exp_name):
    """
    Tries to match the name of the event to the expected value.
    Returns True or False depending on the match.
        - event:
            An event log as returned by the `sparkl('listen')` command.
        - type:
            The type of the event. E.g. notify or request.
        - exp_name:
            The expected name the function matches against.
    """
    # Get the name of the event and compare it to the expected value.
    try:

        # Name comprises full path. Last part is the actual name.
        name = get_event_name(event, event_type)

        return name == exp_name

    # If the event has no attr attribute (or type), it cannot be matched.
    except KeyError:
        return False


def match_event(event, exp_type):
    """
    Tries to match an event type.
    Returns True or False depending on the match.
        - event:
            An event log as returned by the `sparkl('listen')` command.
        - exp_type:
            The expected event type the function matches against.
    """
    try:
        return exp_type in event['attr']

    except KeyError:
        return False


def match_unexpected(notify, expected, collected):
    """
    Returns True (the notify is unexpected) or False.
        - notify: The name of the notify
        - expected: The name of the expected notify.
        - collected: All notifies that did happen.

    A notify is unexpected if:
        1. It is in the collected list and
        2. It is not the same as the expected notify.
    """
    return notify in collected and notify != expected


# Parametrised test data. test_vibr is invoked once per item in list.
# Each test generates a random integer value between two given thresholds.
# The value between the thresholds should only trigger one alert.
TEST_DATA = [
                {
                    'test_vibration': randint(0, 30),
                    'exp_notify': 'GreenAlert'},

                {
                    'test_vibration': randint(31, 69),
                    'exp_notify': 'AmberAlert'
                },

                {
                    'test_vibration': randint(70, 100),
                    'exp_notify': 'RedAlert'}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_vibr(test_data, base_setup, setup_method, listener_setup):
    """
    Test filtered subroutines. For any given vibration value, only
    one of the subroutine notifies should be triggered.

    The test fails, if:
        - No notify events happen due to the test.
        - The expected subroutine notify is not triggered.
        - Any of the unexpected subroutine notifies gets triggered.
    """

    # All notify events will be put into this list.
    notifies_collected = []

    # Collect alias and event queue from test setup.
    alias = setup_method
    event_queue = listener_setup

    # Trigger master notify with test vibration value.
    vibration = test_data['test_vibration']
    sparkl('vars',
           literal=[('vibration', vibration)],
           alias=alias)
    sparkl('call', NOTIFY, alias=alias)

    # Read event log and collect all notify events.
    while True:
        try:
            event = event_queue.get(timeout=3)

            if match_event(event, 'notify'):
                notifies_collected.append(
                    get_event_name(event, 'notify'))

        except Empty:
            break

    # Test fails if no notify event is found.
    assert notifies_collected, 'No notify events found.'

    # Check event log for expected notify.
    expected_notify = test_data['exp_notify']

    # Check event log for unexpected notifies.
    unexpected_notifies = [notify for notify in ALERT_NOTIFIES
                           if match_unexpected(notify, expected_notify,
                                               notifies_collected)]

    assert not unexpected_notifies, \
        'With vibration of {} did not expect any of these events: {}'.format(
                vibration, ','.join(unexpected_notifies))

    assert expected_notify in notifies_collected, \
        'With vibration of {} expected to get {} event'.format(
            vibration, expected_notify)
