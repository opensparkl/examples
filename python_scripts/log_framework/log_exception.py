"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Exception raised when e.g. the log framework
receives a malformed on_exit or on_event function.
"""


class LogException(Exception):
    """
    Class for log framework exceptions.
    """
    def __init__(self, message):
        """
        Reason of exception kept in
        message attribute.
        """
        Exception.__init__(self)
        self.message = str(message)
