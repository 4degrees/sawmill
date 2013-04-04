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

    def __and__(self, other):
        '''Combine this filterer with *other* using All.'''
        if not isinstance(other, Filterer):
            raise NotImplementedError(
                'Cannot combine filterer {0} with non-filterer {1}'
                .format(self, other)
            )
        return All([self, other])

    def __or__(self, other):
        '''Combine this filterer with *other* using Any.'''
        if not isinstance(other, Filterer):
            raise NotImplementedError(
                'Cannot combine filterer {0} with non-filterer {1}'
                .format(self, other)
            )

        return Any([self, other])


class All(Filterer):
    '''Combine filterers and filter logs that don't pass all filterers.

    .. note::

        If one of the filterers pass then the log will *not* be filtered.

    '''

    def __init__(self, filterers=None):
        '''Initialise filterer with initial *filterers* to combine.'''
        self.filterers = filterers or []
        super(All, self).__init__()

    def filter(self, log):
        '''Return True if all filterers return True for *log*.

        .. note::

            If no filterers have been set then will return False.

        '''
        if not len(self.filterers):
            return False

        for filterer in self.filterers:
            if not filterer.filter(log):
                return False

        return True


class Any(Filterer):
    '''Combine filterers and filter logs that don't pass any filterers.

    .. note::

        If any of the filterers do not pass then the log will be filtered.

    '''

    def __init__(self, filterers=None):
        '''Initialise filterer with initial *filterers* to combine.'''
        self.filterers = filterers or []
        super(Any, self).__init__()

    def filter(self, log):
        '''Return True if any filterer returns True for *log*.

        .. note::

            If no filterers have been set then will return False.

        '''
        if not len(self.filterers):
            return False

        for filterer in self.filterers:
            if filterer.filter(log):
                return True

        return False

