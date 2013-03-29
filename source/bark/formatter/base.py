# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from abc import ABCMeta, abstractmethod


class Formatter(object):
    '''Format :py:class:`~bark.log.Log` data for output.

    The format of data returned should conform to a contract with supported
    handlers. In this way a formatter is tightly bound to a Handler and is
    really only separated out to increase possibility of reuse.

    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, log):
        '''Return formatted data representing *log*.'''
