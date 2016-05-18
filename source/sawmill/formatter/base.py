# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from abc import ABCMeta, abstractmethod


class Formatter(object):
    '''Format :py:class:`logs<sawmill.log.Log>` into data for output.

    The format of data returned should conform to a contract with supported
    handlers. In this way a formatter is tightly bound to a Handler and is
    really only separated out to increase possibility of reuse.

    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, logs):
        '''Return formatted data representing *logs*.

        The data should be returned as a list, typically one entry per log.
        Some formatters may choose to combine the passed logs into one
        formatted datum and should return a list of a single item.

        .. warning::

            *logs* may be shared and should not be altered.

        '''
