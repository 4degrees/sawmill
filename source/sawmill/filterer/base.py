# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from abc import ABCMeta, abstractmethod


class Filterer(object):
    '''Determine if :py:class:`logs<sawmill.log.Log>` should be filtered.'''

    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, logs):
        '''Return *logs* that pass filter.'''

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
    '''Combine filterers and filter logs that don't pass all filterers.'''

    def __init__(self, filterers=None):
        '''Initialise filterer with initial *filterers* to combine.'''
        self.filterers = filterers or []
        super(All, self).__init__()

    def filter(self, logs):
        '''Return *logs* that pass all filterers.

        .. note::

            If no filterers have been set then all *logs* are returned.

        '''
        if not len(self.filterers):
            return logs

        passed = set(logs)
        for filterer in self.filterers:
            passed.intersection_update(filterer.filter(logs))

        return sorted(passed, key=logs.index)


class Any(Filterer):
    '''Combine filterers and filter logs that don't pass any filterers.'''

    def __init__(self, filterers=None):
        '''Initialise filterer with initial *filterers* to combine.'''
        self.filterers = filterers or []
        super(Any, self).__init__()

    def filter(self, logs):
        '''Return *logs* that pass any of the filterers.

        .. note::

            If no filterers have been set then all *logs* are returned.

        '''
        if not len(self.filterers):
            return logs

        passed = set()
        for filterer in self.filterers:
            passed.update(filterer.filter(logs))

        return sorted(passed, key=logs.index)
