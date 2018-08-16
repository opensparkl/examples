"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Sample SPARKL logging framework.

Use the log_frame function to specify:
    - One or more filters for logged SPARKL events
    - on-event callback that gets executed if an event gets
      through the filters
    - on-exit callback that gets executed when the event
      logging stops either due to a system exit or calling
      the close method on the events generator
"""

from log_exception import LogException


def add_event_to_args(fun_arg_tuple, event):
    """
    Adds the event to the positional arguments
    of the function.

    Event is always inserted as the first positional
    argument.
    """
    fun, arg, kwargs = fun_arg_tuple
    arg = (event, ) + arg
    return fun, arg, kwargs


def process_function(fun_args_tuple):
    """
    Accepts a tuple of:
        - fun - A function name
        - args - A tuple of positional args. By default: ()
        - kwargs - A dict of keyword args. By default: {}

    Calls the received function with the provided positional
    and keyword arguments.
    """
    fun, args, kwargs = fun_args_tuple
    return fun(*args, **kwargs)


def get_fun_name(fun_args_tuple):
    """
    Accepts a function, args, kwargs tuple and
    prints the name of a function instance.
    """
    fun_instance, _args, _kwargs = fun_args_tuple
    fun_name = fun_instance.__name__
    return fun_name


def print_filters_info(filter_tuples):
    """
    Prints the name of each filter function.
    """
    print('Filters set:')
    for filter_tuple in filter_tuples:
        print(get_fun_name(filter_tuple))


def apply_filters(event, constraints):
    """
    If any of the supplied filter functions
    returns False, return nothing.
    Otherwise, return the event.
    """

    for constraint in constraints:

        # Add the event to all filter functions as first
        # positional argument
        constraint = add_event_to_args(constraint, event)

        # Filters return True(success) or False(filtered out)
        result = process_function(constraint)

        # If any of the filters returns False, the event is filtered out
        if not result:
            return False

    # Only return event if all filter conditions succeed
    return event


def validate_fun(fun_arg_tuple):
    """
    Validates the function inputs such as filter functions
    on_event and on_exit functions.
    """
    help_message = ('Filter, on_event and on_exit functions must look like: '
                    ' ( function, (), {} )')

    if not isinstance(fun_arg_tuple, tuple):
        raise LogException('Input not a tuple!\n' + help_message)

    length = len(fun_arg_tuple)

    if length != 3:
        raise LogException('Tuple size not 3!\n' + help_message)

    fun, args, kwargs = fun_arg_tuple

    if not callable(fun):
        raise LogException('First argument not a callable function!\n' +
                           help_message)

    if not isinstance(args, tuple):
        raise LogException('Arguments must be a tuple!\n' + help_message)

    if not isinstance(kwargs, dict):
        raise LogException('Keyword args must be a dict!\n' + help_message)


def validate_input(filter_funs, on_event, on_exit):
    """
    Validates all functions.
    """
    if not isinstance(filter_funs, list):
        raise LogException('Add filter functions as a list!')

    all_functions = filter_funs + [on_event, on_exit]

    for function in all_functions:
        if function:
            validate_fun(function)


def log_frame(events, filter_funs, on_event=None, on_exit=None):
    """
    Events is the generator instance returned on calling sparkl('listen').

    The log_frame function passes each event through the specified filters.
    On each event that is not filtered out, it calls the provided on_event
    function if there is one.

    Finally, calls the on_exit function to clean up, if such a function
    is specified.

    All specified functions - filter, on_event, on_exit -  must be a tuple of:
        - The name of the function to call
        - The positional arguments (another tuple)
        - The keyword arguments (a dictionary)
    E.g. (my_fun, (1,2), {'foo':'bar'}) or (my_empty_fun, (), {})
    """

    # Collect functions and validate them. Validation failure raises
    # an exception crashing out
    validate_input(filter_funs, on_event, on_exit)

    # Print the name of all specified filters.
    if filter_funs:
        # Print the name of each specified filter function.
        print_filters_info(filter_funs)

    # Unless there isn't any
    else:
        print('No filters applied.')

    # Print the name of the specified on_event function, if any.
    if on_event:
        print('On matched event call:')
        print(get_fun_name(on_event))

    # Process all events.
    try:
        for event in events:

            if filter_funs:
                # Send the event through all specified filters.
                filtered_event = apply_filters(event, filter_funs)
            else:
                # Unless there are no filters.
                filtered_event = event

            # If the event succeeds and there is an on_event function, call it.
            if filtered_event and on_event:

                # Add event to on_event function
                on_event = add_event_to_args(on_event, event)
                # And call on event function
                process_function(on_event)

            # If there is no on_event function, just print all events
            # that get through the filters.
            elif filtered_event:
                print(filtered_event)

    # When the loop ends - either because of an interruption caused by the user
    # or the on-event function, execute the on-exit function, if there is one.
    finally:
        print('Exiting...')
        if on_exit:
            print('Calling exit function: {}'.format(get_fun_name(on_exit)))
            process_function(on_exit)
