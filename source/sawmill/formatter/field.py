# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Formatter


class Field(Formatter):
    '''Format :py:class:`logs<sawmill.log.Log>` according to item list.'''

    SKIP, ERROR = ('__SKIP__', '__ERROR__')
    REMAINING = '*'

    def __init__(self, keys, missing_key=SKIP, template='{key}={value}',
                 item_separator=':'):
        '''Initialise formatter with *keys* to look for in specific order.

        *keys* may contain :py:attr:`REMAINING` at any point to include all
        remaining unspecified keys in alphabetical order.

        *missing_key* determines how to handle a missing key when formatting a
        log. The default :py:attr:`SKIP` will skip the key and not include it
        in the resulting output. :py:attr:`ERROR` will cause a KeyError to be
        raised. Any other value will be used as the substitute string for the
        missing value.

        *template* is used to format the key and value of each field and
        *item_separator* will separate each item.

        '''
        super(Field, self).__init__()
        self.keys = keys
        self.missing_key = missing_key
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
                    if self.missing_key == self.ERROR:
                        raise KeyError(key)
                    elif self.missing_key == self.SKIP:
                        continue
                    else:
                        value = self.missing_key
                else:
                    value = log[key]

                entry = self.template.format(key=key, value=value)
                if entry:
                    field_data.append(entry)

            data.append('{0}\n'.format(self.item_separator.join(field_data)))

        return data

