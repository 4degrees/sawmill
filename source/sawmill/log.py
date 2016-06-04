# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import copy
from collections import MutableMapping


class Log(
    MutableMapping,
    dict  # dict is required as some third-party packages, such as pystache,
          # test using isinstance against dict.
          # Issue registered at https://github.com/defunkt/pystache/issues/185
):
    '''Hold individual log data.'''

    def __init__(self, *args, **kw):
        '''Initialise log.'''
        super(Log, self).__init__()
        self._mapping = dict(*args, **kw)

    def clone(self):
        '''Return a clone of this log.

        This is a mixture of shallow and deep copies where the log instance
        and its attributes are shallow copied, but the actual mapping (items)
        are deepcopied.

        '''
        log = copy.copy(self)
        log._mapping = copy.deepcopy(self._mapping)
        return log

    def __repr__(self):
        '''Return unambiguous representation.'''
        return '{0}({1!r})'.format(self.__class__.__name__, self._mapping)

    def __str__(self):
        '''Return string representation.'''
        return str(self._mapping)

    def __len__(self):
        '''Return number of keys.'''
        return len(self._mapping)

    def __iter__(self):
        '''Return iterator over object.'''
        return iter(self._mapping)

    def __getitem__(self, key):
        '''Return value referenced by *key*.'''
        return self._mapping[key]

    def __setitem__(self, key, value):
        '''Set *key* to reference *value*.'''
        self._mapping[key] = value

    def __delitem__(self, key):
        '''Remove *key* reference.'''
        del self._mapping[key]

    def __hash__(self):
        '''Return hash of mapping.'''
        return hash(frozenset(self._mapping.iteritems()))

