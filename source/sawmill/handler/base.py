# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import atexit
from abc import ABCMeta, abstractmethod


class Handler(object):
    '''Handle a :class:`~sawmill.log.Log`, outputting it in a relevant way.'''

    __metaclass__ = ABCMeta

    def __init__(self, filterer=None, formatter=None):
        '''Initialise handler with *filterer* and *formatter*.

        If specified, *filterer* should be an instance of
        :py:class:`~sawmill.filterer.base.Filterer` and will be used to
        determine whether to handle a log or not.

        *formatter* should be an instance of
        :py:class:`~sawmill.formatter.base.Formatter` and will be called to
        format the log record into a format suitable for output by this handler.
        As such a contractual relationship exists between a handler and its
        formatter.

        '''
        self.filterer = filterer
        self.formatter = formatter
        self.setup()

    def setup(self):
        '''Setup handler.'''
        atexit.register(self.teardown)

    def teardown(self):
        '''Teardown handler.'''

    def handle(self, *logs):
        '''Output formatted *logs* that pass defined filters.'''
        if self.filterer is not None:
            logs = self.filterer.filter(logs)

        data = logs
        if self.formatter is not None:
            data = self.formatter.format(logs)

        self.output(data)

    @abstractmethod
    def output(self, data):
        '''Output formatted *data*.

        *data* should be a list of entries (typically one per log) to output.

        .. warning::

            *data* may be shared and should not be altered.

        '''

