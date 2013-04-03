# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import collections

from .base import Logger


class Dynamic(Logger):
    '''Dynamic logger allowing delayed computation of values.'''

    def __getitem__(self, key):
        '''Return value referenced by *key*.

        If the value is a callable, then call it and return the result. In
        addition store the computed result for future use.

        '''
        value = self._mapping[key]
        if isinstance(value, collections.Callable):
            self[key] = value = value()

        return value
