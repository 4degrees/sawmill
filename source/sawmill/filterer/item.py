# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Filterer


class Item(Filterer):
    '''Filter logs based on key, value item matching.'''

    INCLUDE, EXCLUDE = ('include', 'exclude')

    def __init__(self, key, value, mode=INCLUDE):
        '''Initialise filterer with *key* and *value* to test against.

        *mode* can be either :py:attr:`~sawmill.filterer.item.Item.EXCLUDE` or
        :py:attr:`~sawmill.filterer.item.Item.INCLUDE`. If set to
        :py:attr:`~sawmill.filterer.item.Item.EXCLUDE` then any log that has the
        specific *key*, *value* pair will be filtered. Conversely, if set to
        :py:attr:`~sawmill.filterer.item.Item.INCLUDE` then any log not matching
        the *key*, *value* pair exactly will be filtered.

        '''
        super(Item, self).__init__()
        self.key = key
        self.value = value
        self.mode = mode

    def filter(self, logs):
        '''Filter *logs* based on key, value item matching.

        If a log does not have the key to test against and mode is set to
        :py:attr:`~sawmill.filterer.item.Item.INCLUDE` it will be filtered.
        Conversely, if mode is set to
        :py:attr:`~sawmill.filterer.item.Item.EXCLUDE` it will not be filtered.

        '''
        passed = []
        for log in logs:
            # Handle case where key not present to test against.
            if self.key not in log:
                if self.mode == self.EXCLUDE:
                    passed.append(log)
                continue

            value = log[self.key]

            if value == self.value and self.mode == self.EXCLUDE:
                continue

            if value != self.value and self.mode == self.INCLUDE:
                continue

            passed.append(log)

        return passed
