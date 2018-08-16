"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Test cases for Crypto Portfolio SPARKL mix in examples repo.
"""

import json
import pytest

from tests.conftest import (IMPORT_DIR, OPERATION, INPUT_FIELDS, EXP_RESPONSE,
                            OUTPUT_FIELDS, CHECK_FUN, STOP_OR_NOT,
                            check_float_value, compare_values, run_tests)

# The test setup imports these files into the import directory.
FILE_PATHS = ["Examples/CryptoPortfolio/CryptoPortfolio.xml",
              "Library/lib_bitcoin/lib_bitcoin.xml"]

# The SPARKL path to the tested mix.
USER_TREE_PATH = "{}/CryptoPortfolio".format(IMPORT_DIR)

# Path to the tested operations.
ITERATE_OP = '{}/Mix/Impl/ChangeTracker/Iterate'.format(USER_TREE_PATH)
COMPARE_OP = '{}/Mix/Impl/ChangeTracker/Compare'.format(USER_TREE_PATH)
ADD_OP = '{}/Mix/Test/TestAdd'.format(USER_TREE_PATH)
ADD_DUPL_OP = '{}/Mix/Test/TestAddDuplicate'.format(USER_TREE_PATH)
ADD_RECORD_OP = '{}/Mix/API/AddRecord'.format(USER_TREE_PATH)
DELETE_OP = '{}/Mix/API/DeleteRecord'.format(USER_TREE_PATH)
TEST_DELETE_OP = '{}/Mix/Test/TestDelete'.format(USER_TREE_PATH)
BULK_ADD_OP = '{}/Mix/Impl/Manage/BulkAdd'.format(USER_TREE_PATH)
CHANGE_OP = '{}/Mix/API/ChangeCurrency'.format(USER_TREE_PATH)

# The input and output fields of the tested mix.
CURRENCY_FLD = 'currency'
CRYPTO_CURRENCY_FLD = 'crypto_currency'
CRYPTO_CURRENCIES_FLD = 'crypto_currencies'
CRYPTO_PRICE_FLD = 'crypto_price'
PORTFOLIO_FLD = 'portfolio'
START_STATE_FLD = 'start_state'
END_STATE_FLD = 'end_state'
ERROR_FLD = 'error'
LAST_PRICE_FLD = 'last_price'
CHANGE_FLD = 'change'
BTC_PRICE_FLD = 'btc_price'

# SPARKL replies/responses
OK_RESP = 'Ok'
ERROR_RESP = 'Error'
DONE_RESP = 'Done'


#####################################################
# Additional check functions used by the test data. #
#####################################################


def check_compare(change, reference_value):
    """
    Rounds a percentage value and checks it
    against a reference value.
    """
    rounded_change = round(change, 2)
    compare_values(reference_value, rounded_change)


def check_iterate(out_fields):
    """
    Collects the last price from the output fields and
    checks whether it is a float larger than zero.
    """
    last_price = out_fields[LAST_PRICE_FLD]
    check_float_value(last_price, LAST_PRICE_FLD)


def check_compare_grow(out_fields):
    """
    Collects the percentage change fom the output fields,
    checks whether it is a float, rounds it and checks it
    against a reference value.
    """
    change = out_fields[CHANGE_FLD]
    expected_change = 50.00
    check_compare(change, expected_change)
    check_float_value(change, CHANGE_FLD)


def check_compare_decrease(out_fields):
    """
    Collects the percentage change fom the output fields,
    checks whether it is a float, rounds it and checks it
    against a reference value.
    """
    change = out_fields[CHANGE_FLD]
    expected_change = -25.00
    check_compare(change, expected_change)
    check_float_value(change, CHANGE_FLD)


def check_add(out_fields):
    """
    Used in testing `Add` operation, adding xrp cryptocurrency to portfolio.
    Expects:
        End state of [ [ 'XRP', price_as_float ] ]
    """
    # Get value of end_state field and decode into json
    end_state = json.loads(out_fields[END_STATE_FLD])

    # Get first record of end_state list and split it into ticker and price
    [crypto_ticker, crypto_price] = end_state[0]
    expected_crypto_ticker = 'XRP'
    compare_values(expected_crypto_ticker, crypto_ticker)
    check_float_value(crypto_price, crypto_price)


def check_delete(out_fields):
    """
    Used in testing `Delete` operation by first adding
    crypto currency (dgb) to portfolio to have something to delete.

    Expects:
        Start state of ['DGB', DGP_PRICE_FLOAT]
    """
    # Get value of start state field and decode into json
    start_state = json.loads(out_fields[START_STATE_FLD])

    # Get first record of end_state list and split it into ticker and price
    [crypto_ticker, crypto_price] = start_state[0]
    expected_crypto_ticker = 'DGB'
    compare_values(expected_crypto_ticker, crypto_ticker)
    check_float_value(crypto_price, crypto_price)


def check_change(output_fields):
    """
    Test ChangeCurrency operation.
    Expects:
        Ok response
        Price of bitcoin in EUR as float
    """
    btc_price = output_fields[BTC_PRICE_FLD]
    check_float_value(btc_price, BTC_PRICE_FLD)


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

    # Test Iterate operation with empty portfolio.
    {
        OPERATION: ITERATE_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'gbp'),
                       (PORTFOLIO_FLD, '[]')],
        EXP_RESPONSE: DONE_RESP},

    # Test Iterate operation with [{\"etc\",321.44}] in portfolio.
    {
        OPERATION: ITERATE_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'usd'),
                       (PORTFOLIO_FLD, '[{\"etc\",321.44}]')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            CURRENCY_FLD: 'usd',
            CRYPTO_CURRENCY_FLD: 'etc',
            PORTFOLIO_FLD: '[]'},
        CHECK_FUN: check_iterate},

    # Test Compare operation with 10.6 as last price and 15.9 as current price.
    {
        OPERATION: COMPARE_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'eth'),
                       (CRYPTO_PRICE_FLD, 15.9),
                       (LAST_PRICE_FLD, 10.6)],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_compare_grow},

    # Test Compare operation with 12.8 as last price and 9.6 as current price.
    {
        OPERATION: COMPARE_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'eth'),
                       (CRYPTO_PRICE_FLD, 9.6),
                       (LAST_PRICE_FLD, 12.8)],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_compare_decrease},

    # Test Add operation, adding xrp cryptocurrency to portfolio.
    # Expects:
    #    Start state of [] (empty list)
    #    End state of [ [ 'XRP', price_as_float ] ] -> check_add
    {
        OPERATION: ADD_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'xrp')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            START_STATE_FLD: '[]'},
        CHECK_FUN: check_add},

    # Test Add operation, trying to add same cryptocurrency (ltc) twice.
    # Expects Error message as LTC is already in portfolio.
    {
        OPERATION: ADD_DUPL_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'ltc')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '\"Crypto currency LTC is already in portfolio.\"'}},

    # Test Add operation, trying to add invalid cryptocurrency (foo).
    # Expects Error message of not supported currency.
    {
        OPERATION: ADD_RECORD_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'foo')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '{\"Currency not supported\",\"BTC_FOO\"}'}},

    # Test Delete operation with crypto currency not in portfolio.
    # Expects Error response saying crypto currency is not in portfolio.
    {
        OPERATION: DELETE_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'dgb')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '\"Crypto currency DGB is not in portfolio.\"'}},

    # Test Delete operation by first adding crypto currency (dgb) to portfolio
    # to have something to delete.
    # Expects:
    #    End state of empty list
    #    Start state of ['DGB', DGP_PRICE_FLOAT] -> check_delete
    # Services are stopped before running this operation to clear service state
    {
        OPERATION: TEST_DELETE_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCY_FLD, 'dgb')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            END_STATE_FLD: '[]'},
        CHECK_FUN: check_delete,
        STOP_OR_NOT: True},

    # Test BulkAdd operation with empty list. Must send Done reply back.
    {
        OPERATION: BULK_ADD_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCIES_FLD, '[]')],
        EXP_RESPONSE: DONE_RESP},

    # Test BulkAdd operation with a list of one cryptocurrency - ["etc"].
    # Expects the following fields and values:
    #    crypto_currencies (remaining_list) -> [] (empty list)
    #    crypto_currency -> etc (value taken from input list)
    {
        OPERATION: BULK_ADD_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCIES_FLD, '[\"etc\"]')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            CRYPTO_CURRENCIES_FLD: '[]',
            CRYPTO_CURRENCY_FLD: 'etc'}},

    # Test BulkAdd operation with a list of cryptocurrencies - ["etc","eth"].
    # Expects the following fields and values:
    #    crypto_currencies (remaining_list) -> ["eth"] (one remaining)
    #    crypto_currency -> etc (first value taken from input list)
    {
        OPERATION: BULK_ADD_OP,
        INPUT_FIELDS: [(CRYPTO_CURRENCIES_FLD, '[\"etc\",\"eth\"]')],
        EXP_RESPONSE: OK_RESP,
        OUTPUT_FIELDS: {
            CRYPTO_CURRENCIES_FLD: '[\"eth\"]',
            CRYPTO_CURRENCY_FLD: 'etc'}},

    # Test ChangeCurrency operation.
    # Expects: Price of bitcoin in EUR as float
    {
        OPERATION: CHANGE_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'EUR')],
        EXP_RESPONSE: OK_RESP,
        CHECK_FUN: check_change},

    # Test ChangeCurrency operation with invalid currency (foo).
    # Expects: Error message saying currency is not supported.
    {
        OPERATION: CHANGE_OP,
        INPUT_FIELDS: [(CURRENCY_FLD, 'foo')],
        EXP_RESPONSE: ERROR_RESP,
        OUTPUT_FIELDS: {
            ERROR_FLD: '{\"Currency not supported\",\"FOO\"}'}}
]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_crypto_portfolio(test_data, base_setup, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session
    """
    alias = setup_method
    run_tests(alias, **test_data)
