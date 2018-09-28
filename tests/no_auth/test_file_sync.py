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

Tests for FileSync demo.
"""

import os
import subprocess
import pytest

from tests.conftest import IMPORT_DIR, TEST_NAME, MINERS, MINER_FUN, \
    MINER_ARGS, EXP, ChDir, assert_events

from tests.filters import match_event_with_field


# Path to one or more SPARKL mixes your test needs.
FILE_PATHS = ['Examples/FileSync/FileSync.xml']

# Full path to FileSync'se folder. file_sync_setup uses it in conftest.py.
PATH_TO_MIX_DIR = os.path.abspath('Examples/FileSync')

# The SPARKL path to the tested mix and the master/slave services.
USER_TREE_PATH = '{}/FileSync'.format(IMPORT_DIR)
MASTER_SERVICE = '{}/Master'.format(USER_TREE_PATH)
SLAVE_SERVICE = '{}/Slave'.format(USER_TREE_PATH)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

# Test files/folders created/moved and removed by the tests.
# They are handled inside a temp directory.
TEST_FILE = 'bar.txt'
TEST_DIR = 'my_dir'

# Key constant used by test data.
TRIGGER = 'trigger'


def file_operation(path, command):
    """
    Invokes a file system operation changing
    into the specified directory first.
    """
    with ChDir(path):
        subprocess.check_call(command)


def create_file(path):
    """
    Creates a test file.
    """
    command = ['touch', TEST_FILE]
    file_operation(path, command)


def create_folder(path):
    """
    Creates a test folder.
    """
    command = ['mkdir', TEST_DIR]
    file_operation(path, command)


def move_file(path):
    """
    Moves a test file from
    one directory to another.
    """
    new_path = os.path.join(TEST_DIR, TEST_FILE)
    command = ['mv', TEST_FILE, new_path]
    file_operation(path, command)


def delete_folder(path):
    """
    Deletes a whole test folder.
    """
    command = ['rm', '-rf', TEST_DIR]
    file_operation(path, command)


"""
Each set of test data comprises:
    - TEST_NAME:
        The name of the test case
    - TRIGGER:
        A function that invokes a file system
        operation causing events to happen
    - MINERS:
        Filters that try to match specific events
"""
TEST_DATA = [

    # Create a test file. 1 Put notify and 1 Put consume are expected.
    {
        TEST_NAME: 'test_file_sync_create',
        TRIGGER: create_file,
        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'Put'),
                EXP: 1},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'Put'),
                EXP: 1}]
    },

    # Create a test folder. 1 Put notify and 1 Put consume are expected.
    {
        TEST_NAME: 'test_file_sync_create_folder',
        TRIGGER: create_folder,
        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'Put'),
                EXP: 1},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'Put'),
                EXP: 1}]
    },

    # Move the test file into the test dir.
    # 1 Move notify and 1 Move consume are expected.
    {
        TEST_NAME: 'test_file_sync_move_file',
        TRIGGER: move_file,
        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'Move'),
                EXP: 1},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'Move'),
                EXP: 1}]
    },

    # Delete the test dir. 2 Delete notifes and 2 Delete consumes are expected
    # (1 for the test folder, 1 for the test file inside).
    {
        TEST_NAME: 'test_file_sync_delete',
        TRIGGER: delete_folder,
        MINERS: [
            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('notify', 'Delete'),
                EXP: 2},

            {
                MINER_FUN: match_event_with_field,
                MINER_ARGS: ('consume', 'Delete'),
                EXP: 2}]
    }
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_file_sync(test_data, session_setup, module_setup, listener_setup, file_sync_setup):
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
        - file_sync_setup:
            Module-based setup that starts the slave and master service implemenations, creates
            the slave and master temp dirs and hands them to each test case.
    """
    log_writer = session_setup
    event_queue = listener_setup

    master_dir, _slave_dir = file_sync_setup

    # File operation that causes events to happen.
    test_data[TRIGGER](master_dir)

    assert_events(event_queue, log_writer, test_data[TEST_NAME],
                  miners=test_data[MINERS])
