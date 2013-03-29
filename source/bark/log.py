# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from collections import MutableMapping


class Log(MutableMapping):
    '''Hold individual log data.'''

    def __init__(self, *args, **kw):
        '''Initialise log.'''
        super(Log, self).__init__()
        self._mapping = dict(*args, **kw)

    def __str__(self):
        '''Return string representation.'''
        return str(self._mapping)

    def __len__(self):
        '''Return number of keys.'''

    def __iter__(self):
        '''Return iterator over object.'''
        return iter(self._mapping)

    def __getitem__(self, key):
        '''Return value referenced by *key*.'''
        return self._mapping[key]

    def __setitem__(self, key, value):
        '''Set *key* to reference *value*.'''
        self._mapping[key] = value

    def __delitem(self, key):
        '''Remove *key* reference.'''
        del self._mapping[key]

