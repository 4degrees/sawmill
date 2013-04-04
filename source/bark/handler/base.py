# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import atexit
from abc import ABCMeta, abstractmethod


class Handler(object):
    '''Handle a :py:class:`~bark.log.Log`, outputting it in a relevant way.'''

    __metaclass__ = ABCMeta

    def __init__(self, filterer=None, formatter=None):
        '''Initialise handler with *filterer* and *formatter*.

        If specified, *filterer* should be an instance of
        :py:class:`~bark.filterer.base.Filterer` and will be used to determine
        whether to handle a log or not.

        *formatter* should be an instance of
        :py:class:`~bark.formatter.base.Formatter` and will be called to format
        the log record into a format suitable for output by this handler. As
        such a contractual relationship exists between a handler and its
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

    def handle(self, log):
        '''Output formatted *log* if passes defined filters.'''
        if self.filterer is not None and self.filterer.filter(log):
            return

        data = log
        if self.formatter is not None:
            data = self.formatter.format(log)

        self.output(data)

    @abstractmethod
    def output(self, data):
        '''Output formatted *data*.

        .. warning::

            *data* may be shared and should not be altered.

        '''

