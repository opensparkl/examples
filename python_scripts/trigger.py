"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Contains functions to call operations.
Module itself calls the Primes expr SPARKL configuration
with a user specified number.
"""

from __future__ import print_function
import uuid

from six.moves import input
from sparkl_cli.main import sparkl
from sparkl_cli.CliException import CliException
from login_and_logout import connect_login, logout_close


def get_input_number():
    """
    Prompts user for a valid input number.
    Keeps prompting until it gets one.
    """

    # Get input as string
    value = input('Enter a number for testing: ')

    # Convert it into integer
    try:
        value = int(value)

    # If string is not a number, retry
    except ValueError as error:
        print(error)
        return get_input_number()

    # Return valid number as integer
    return value


def trigger_operation(fields, operation):
    """
    Function runs a SPARKL operation.
    It also sets the fields needed to do so.
    """

    # Generate random alias
    alias = uuid.uuid4().hex

    # Try to connect and log into SPARKL
    (login_tag, login_data) = connect_login(alias)

    # If either fails, return and print error
    if login_tag == 'error':
        print(login_data)
        return 'error', login_data

    # Set vars and call operation
    try:
        sparkl('vars', alias=alias, literal=fields)
        result_data = sparkl('call', operation, alias=alias)

    # Return from fun if operation not found or other SPARKL error
    except CliException as error:
        print(error)
        return 'error', error

    # Log out and close connection
    logout_close(alias)

    # Get response and fields
    try:
        response = result_data['attr']['name']
        fields = result_data['content']

    # If SPARKL operation fails, return data is not as expected
    except KeyError as error:
        print(result_data)
        return 'error', error

    # Return object with response and fields
    return_object = {'response': response, 'fields': fields}
    return 'ok', return_object


def is_prime():
    """
    Fires solicit of the Primes expr configuration.
    Decides if a number is prime or not.
    """

    # Use fun to prompt user for input number
    number = get_input_number()

    # Specify fields and operation for transaction
    fields = [('n', number)]
    operation = 'Scratch/Primes_expr/Mix/Frontend/CheckPrime'

    # Use fun to retrieve response to solicit
    (tag, response_data) = trigger_operation(fields, operation)

    if tag == 'error':
        print(response_data)
        return 'error'

    response = response_data['response']

    # Depending on response, print answer and return boolean
    if response == 'Yes':
        print('%s is a prime number.' % (number))
        return True

    print('%s is not a prime number.' % (number))
    return False


# Call fun when module is run with python -m trigger.py
is_prime()
