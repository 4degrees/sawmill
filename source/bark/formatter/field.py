# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Formatter


class Field(Formatter):
    '''Format :py:class:`logs<bark.log.Log>` according to item list.'''

    IGNORE, ERROR = ('ignore', 'error')
    REMAINING = '*'

    def __init__(self, keys, mode=IGNORE, template='{key}={value}',
                 item_separator=':'):
        '''Initialise formatter with *keys* to look for in specific order.

        *keys* may contain :py:attr:`REMAINING` at any point to include all
        remaining unspecified keys in alphabetical order.

        *mode* determines how to handle a missing key when formatting a log.
        The default :py:attr:`IGNORE` will substitute an empty string for the
        missing value. An alternative is :py:attr:`ERROR`, which would cause an
        error to be raised.

        *template* is used to format the key and value of each field and
        *item_separator* will separate each item.

        '''
        super(Field, self).__init__()
        self.keys = keys
        self.mode = mode
        self.template = template
        self.item_separator = item_separator

    def format(self, logs):
        '''Return formatted data representing *logs*.'''
        data = []
        for log in logs:
            field_data = []

            # Expand keys.
            keys = self.keys[:]
            remaining = sorted(set(log.keys()) - set(keys))
            expanded = []
            for key in keys:
                if key == self.REMAINING:
                    expanded.extend(remaining)
                else:
                    expanded.append(key)

            # Format string.
            for key in expanded:
                if not key in log:
                    if self.mode is self.ERROR:
                        raise KeyError()
                    else:
                        value = ''
                else:
                    value = log[key]

                entry = self.template.format(key=key, value=value)
                if entry:
                    field_data.append(entry)

            data.append('{0}\n'.format(self.item_separator.join(field_data)))

        return data

