"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma.

Set of functions importing all SPARKL sample config files
into specified user tree.
"""
from __future__ import print_function
import glob
import uuid

from six.moves import input
from sparkl_cli.main import sparkl
from login_and_logout import connect_login, logout_close


def user_confirm(prompt):
    """
    Recursively prompts until user says sg starting with "Y/y" or "N/n"
    """
    valid = ['Y', 'N']
    answer = input(prompt)

    # Ask again if user hits enter without answer
    chars = len(answer)
    if chars == 0:
        return user_confirm(prompt)

    # Take first letter of answer and make it uppercase
    answer = answer[0].upper()

    if answer not in valid:
        print('Answer yes or no.')
        return user_confirm(prompt)

    return answer


def lib_create(name, names, alias):
    """
    Creates a folder in the user tree if it does not exist already.
    """
    if not any(x['attr']['name'] == name for x in names):
        sparkl('mkdir', name, alias=alias)
        print('Creating %s folder...' % (name))
        return

    print('Folder %s already exists.' % (name))
    return


def is_import_successful(change_message, config, folder):
    """
    Returns a boolean depending on whether
    the config is already in user tree.

    Also prints a message on success/failure.
    """
    if change_message['tag'] == 'change':
        print('Importing %s into %s...' % (config, folder))
        return True

    reason = change_message['attr']['reason']
    print('Failed to import %s . Reason: %s' % (config, reason))
    return False


def unit_import(config_files, folder, alias):
    """
    Iterates through a list of files and offers them for importing.
    """
    for config in config_files:

        # Prompt for user input
        answer = user_confirm('Import %s? y/n: ' % config)

        # If answer is yes, tries to import file
        if answer == 'Y':
            change_message = sparkl('put', config, folder, alias=alias)

            # Fun prints message based on success/failure
            is_import_successful(change_message, config, folder)

    return


def multi_import():
    """
    Imports all or only the selected SPARKL configs into the user's
    configuration tree.
    """

    # Logs you in using random alias
    alias = uuid.uuid4().hex
    (tag, info) = connect_login(alias)

    # If fails to log in or connect, return from function
    if tag == 'error':
        print(info)
        return

    # Gets the folders available in the user tree
    folders = sparkl('ls', alias=alias)
    folder_names = folders['content']

    # Creates Scratch and/or Lib folder if it does not exist in the user tree
    xmp_dir = 'Scratch'
    lib_dir = 'Lib'
    lib_create(xmp_dir, folder_names, alias)
    lib_create(lib_dir, folder_names, alias)

    # Gets the SPARKL config files from the Examples and Library folders
    # in the examples repo
    examples = glob.glob('../Examples/*/*.xml')
    libs = glob.glob('../Library/*/*.xml')

    # Prompts user to import all config files
    answer_all = user_confirm('Import all examples? y/n ')

    # If user chooses yes, tries to import
    if answer_all == 'Y':

        # All files from the Examples folder
        for config in examples:
            change_message = sparkl('put', config, xmp_dir, alias=alias)

            # Fun prints message based on success/failure
            is_import_successful(change_message, config, xmp_dir)

        # All files from the Library folder
        for config in libs:
            change_message = sparkl('put', config, lib_dir, alias=alias)

            # Fun prints message based on success/failure
            is_import_successful(change_message, config, lib_dir)

        # Logs you out and closes connection
        logout_close(alias)
        return

    # If not all files are chosen for importing, offers them one by one
    unit_import(examples, xmp_dir, alias)
    unit_import(libs, lib_dir, alias)

    # Logs you out and closes connection
    logout_close(alias)
    return


# Call fun when module is run with python -m bulk_import.py
multi_import()
