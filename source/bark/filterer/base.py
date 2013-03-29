# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from abc import ABCMeta, abstractmethod


class Filterer(object):
    '''Determine if :py:class:`~bark.log.Log` should be filtered.'''

    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, log):
        '''Return True if *log* should be filtered.

        If a log is filtered then it will not be processed further by a
        handler.

        '''
