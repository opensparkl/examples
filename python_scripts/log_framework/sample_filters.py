"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Sample filters for filtering SPARKL events. Each filter function
returns either True (the event succeeds) or False (the event is filtered out).

Each filter function has 'event' as their first parameter. This argument is
inserted by the log framework.

Events share a common struct, such as:

{
    u'content': [
        {u'tag': u'field', u'attr': {u'name': u'RECORDS'}},
        {u'tag': u'field', u'attr': {u'name': u'GET'}},
        {u'tag': u'field', u'attr': {u'name': u'CURRENCY'}}
    ],
    u'tag': u'notify',
    u'attr': {
        u'name': u'Update',
        u'svc': u'Sequencer'}
}

All filter functions use a decorator, which wraps each
filter function into a try/except statement.

On any exception, the decorator prints a warning message
and returns a default True/False value.
"""

DEFAULT = True


def print_warning(error, fun_name):
    """
    Prints warnings if a filter function fails
    due to exception.
    """
    print('Warning, {} function error: {}'.format(fun_name, error))


def generic_filter_fun(filter_fun):
    """
    Decorator for filter functions. All
    filter functions return either True or False.

    If any filter function fails due to
    an exception, the wrapper function prints
    a warning with the exception and returns the
    default value specified by the filter function.

    If the filter function does not specify a default
    value, the wrapper returns default_fallback.
    """
    def filter_wrapper(*args, **kwargs):
        """
        Filter function wrapper handling all exceptions.
        """
        default_fallback = DEFAULT

        try:
            return filter_fun(*args, **kwargs)

        except Exception as error:
            fun_name = filter_fun.__name__
            print_warning(error, fun_name)
            default = kwargs.get('default', default_fallback)
            return default

    return filter_wrapper


@generic_filter_fun
def filter_name(event, name, default=DEFAULT):
    """
    Filters out events, whose name does not
    match the specified name.

    If the matching fails, it returns the default
    boolean value.

    NOTE, the default values are used by the decorator
    function.
    """
    event_name = event['attr']['name']
    return event_name == name


@generic_filter_fun
def filter_field(event, field_name, default=DEFAULT):
    """
    Returns True if any field carried in the event
    has the same name specified in field_name.

    Returns the default boolean value on errors.
    """
    content = event['content']
    return any(x['attr']['name'] == field_name for x in content)


@generic_filter_fun
def filter_field_values(event, field_name,
                        min_val=0, max_val=100, default=DEFAULT):
    """
    Returns True if the specified field's value falls between
    the specified thresholds.

    Returns the default value on errors.
    """
    value = [x['attr']['value'] for x in event['content']
             if x['attr']['name'] == field_name][0]
    return min_val < value < max_val


@generic_filter_fun
def filter_tag(event, tag, default=DEFAULT):
    """
    Return True if event tag matches
    the specified tag. Otherwise return False.
    """
    event_tag = event['tag']
    return event_tag == tag
