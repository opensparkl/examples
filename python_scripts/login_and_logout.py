"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Shortcuts for connection and login management
"""
from __future__ import print_function
from six.moves import input
from sparkl_cli.main import sparkl
from sparkl_cli.CliException import CliException


def connect_login(alias='default'):
    """
    Connects to a SPARKL instance and logs into a user account
    The function returns the specified alias (default is "default")
    for other funs to use
    """

    # Prompt for SPARKL instance URL
    instance = input('Enter your SPARKL instance URL: ')

    # Get live connections
    connection_data = sparkl('connect')
    connections = connection_data['content']

    # If alias in use, prompt for new alias
    while any(x['attr']['alias'] == alias for x in connections):
        alias = input(
            'Alias %s in use. Type in another (e.g. foo or bar):' % (alias))

    try:
        # Connect to SPARKL instance
        sparkl('connect', url=instance, alias=alias)
        print('Connected to %s using alias %s' % (instance, alias))

        # Prompt for username
        user = input('Enter your username: ')

        # Log into specified user account
        sparkl('login', user=user, alias=alias)
        print('Logging in as %s...' % (user))

    except CliException as error:
        print(error)
        return 'error', error

    # Return used alias
    return 'ok', alias


def logout_close(alias='default'):
    """
    Logs out user and closes connection linked to specified alias
    (default is "default")
    """
    sparkl('logout', alias=alias)
    print('Logging out of SPARKL...')

    sparkl('close', alias=alias)
    print('Connection associated with alias %s is closed' % (alias))
