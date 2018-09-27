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
# The setup method uses the path(s) to import your configuration(s).
# The setup method assumes you run the tests from the root folder.
# E.g. FILE_PATHS = ['Examples/PrimesExpr/Primes_expr.xml']

PATH_TO_MIX_DIR = os.path.abspath('Examples/FileSync')
FILE_PATHS = ['Examples/FileSync/FileSync.xml']

# The SPARKL path to the tested mix.
USER_TREE_PATH = '{}/FileSync'.format(IMPORT_DIR)
MASTER_SERVICE = '{}/Master'.format(USER_TREE_PATH)
SLAVE_SERVICE = '{}/Slave'.format(USER_TREE_PATH)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = USER_TREE_PATH

TEST_FILE = 'bar.txt'
TEST_DIR = 'my_dir'

TRIGGER = 'trigger'


def file_operation(path, command):
    with ChDir(path):
        subprocess.check_call(command)


def create_file(path):
    command = ['touch', TEST_FILE]
    file_operation(path, command)


def create_folder(path):
    command = ['mkdir', TEST_DIR]
    file_operation(path, command)


def move_file(path):
    new_path = os.path.join(TEST_DIR, TEST_FILE)
    command = ['mv', TEST_FILE, new_path]
    file_operation(path, command)


def delete_folder(path):
    command = ['rm', '-rf', TEST_DIR]
    file_operation(path, command)


TEST_DATA = [
    {
        TEST_NAME: 'test_create',
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

    {
        TEST_NAME: 'test_create_folder',
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

    {
        TEST_NAME: 'test_move_file',
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

    {
        TEST_NAME: 'test_delete',
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
def test_file_sync(test_data, base_setup, setup_method, listener_setup, file_sync_setup):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session.
    """
    event_queue = listener_setup
    log_writer = base_setup
    master_dir, _slave_dir = file_sync_setup

    test_data[TRIGGER](master_dir)

    assert_events(event_queue, log_writer, test_data[TEST_NAME],
                  miners=test_data[MINERS])
