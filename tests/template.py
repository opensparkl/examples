"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Template for writing tests.
"""

import pytest


from tests.conftest import (OPERATION, EXP_RESPONSE,
                            INPUT_FIELDS, CHECK_FUN,
                            OUTPUT_FIELDS, run_tests)

# Path to one or more SPARKL mixes your test needs.
# The setup method uses the path(s) to import your configuration(s).
# The setup method assumes you run the tests from the root folder.
# E.g. FILE_PATHS = ['Examples/PrimesExpr/Primes_expr.xml']
FILE_PATHS = ['PATH_TO_MIX_ON_FILE_SYSTEM']


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
##########################################################################
TEST_DATA = [

    # Add your specific test data thus:
    {
        OPERATION: 'Scratch/test/mix/foo',
        INPUT_FIELDS: [('field_name', 'field_value')],
        EXP_RESPONSE: 'Ok',
        OUTPUT_FIELDS: {
            'output_field_name': 'output_field_value'},
        CHECK_FUN: check_output}]


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_my_test(test_data, setup_method):
    """
    Calls each set of data in TEST_DATA. The function also uses:
        - setup_method:
            A basic setup method that imports the needed configuration(s)
            and yields the SPARKL alias used in the session.
    """
    alias = setup_method
    run_tests(alias, **test_data)
