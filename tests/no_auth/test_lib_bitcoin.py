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

Test cases for testing SPARKL bitcoin library.
"""

import pytest
from tests.conftest import IMPORT_DIR, OPERATION, INPUT_FIELDS, \
    EXP_RESPONSE, OUTPUT_FIELDS, CHECK_FUN, TEST_NAME, \
    check_float_value, run_tests

# Constants are imported into test setup and teardown methods in conftest
FILE_PATHS = ['Library/lib_bitcoin/lib_bitcoin.xml']
USER_TREE_PATH = '{}/lib_bitcoin'.format(IMPORT_DIR)

# SPARKL resource targeted by the `sparkl listen` command.
LISTEN_TARGET = '{}/Sequencer'.format(USER_TREE_PATH)

# Path to tested operations in the user tree.
GET_BTC_OP = '{}/lib_bitcoin/Mix/GetBTC'.format(IMPORT_DIR)
GET_CRYPTO_REQUEST = '{}/lib_bitcoin/Mix/Bitcoin/GetCrypto'.format(IMPORT_DIR)
GET_CRYPTO_SOLICIT = '{}/lib_bitcoin/Mix/GetCrypto'.format(IMPORT_DIR)
CONVERT_OP = '{}/lib_bitcoin/Mix/Bitcoin/Convert'.format(IMPORT_DIR)

# Input and output fields used by the configuration.
CURRENCY_FLD = 'currency'
CRYPTO_CURRENCY_FLD = 'crypto_currency'
CRYPTO_PRICE_FLD = 'crypto_price'
BTC_PRICE_FLD = 'btc_price'
PRICE_IN_BTC_FLD = 'price_in_btc'
ERROR_FLD = 'error'

# Expected reponses/replies by SPARKL
ERROR_RESP = 'Error'
OK_RESP = 'Ok'


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_get_btc(output_fields):
    """
    Checks whether the price of btc is a float and
    larger than zero.
    """
    btc_price = output_fields[BTC_PRICE_FLD]
    check_float_value(btc_price, BTC_PRICE_FLD)


def check_get_etc(output_fields):
    """
    Checks whether the price of etc is a float
    and larger than zero.
    """
    etc_price = output_fields[CRYPTO_PRICE_FLD]
    check_float_value(etc_price, CRYPTO_PRICE_FLD)


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

    # Test full transaction with GetBTC solicit.
    # Expects value of btc_price field to be:
    #   - A float
    #   - More than zero
    {
        TEST_NAME: 'test_get_btc_usd',
        OPERATION: GET_BTC_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'usd')],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_get_btc},

    # Test full transaction with GetBTC solicit and invalid currency (bar).
    # Expects error message to complain about invalid currency.
    {
        TEST_NAME: 'test_get_btc_bar_error',
        OPERATION: GET_BTC_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'bar')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '{\"Currency not supported\",\"BAR\"}'}},

    # Test full transaction with GetCrypto solicit.
    # Expects value of crypto_price field to be:
    # - A float
    # - More than zero
    {
        TEST_NAME: 'test_get_etc_gbp',
        OPERATION: GET_CRYPTO_SOLICIT,
        INPUT_FIELDS: [(CURRENCY_FLD, 'GBP'),
                       (CRYPTO_CURRENCY_FLD, 'ETC')],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_get_etc},

    # Test full transaction with solicit and invalid crypto currency (foo).
    # Expects error message about invalid crypto currency (prefixed with btc_).
    {
        TEST_NAME: 'test_get_foo_error',
        OPERATION: GET_CRYPTO_REQUEST,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'foo')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '{\"Currency not supported\",\"BTC_FOO\"}'}},

    # Test Convert request. Expects value of crypto_price field to be:
    #   A float
    #   The multiplication of the two input fields: 12, 2
    {
        TEST_NAME: 'test_convert',
        OPERATION: CONVERT_OP,
        INPUT_FIELDS: [(PRICE_IN_BTC_FLD, 12),
                       (BTC_PRICE_FLD, 2)],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            CRYPTO_PRICE_FLD: 24}}
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_lib_bitcoin(test_data, session_setup, module_setup, listener_setup):
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
