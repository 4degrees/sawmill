# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import string

from .base import Formatter


class Template(Formatter, string.Formatter):
    '''Format :py:class:`logs<bark.log.Log>` according to a template.'''

    IGNORE, ERROR = ('ignore', 'error')

    def __init__(self, template, mode=IGNORE):
        '''Initialise formatter with *template*.

        *mode* determines how to handle a missing key when formatting a log.
        The default IGNORE will substitute an empty string for the missing
        value. An alternative is ERROR, which would cause an error to be
        raised.

        .. note::

            The template is applied once per processed log.

        '''
        super(Template, self).__init__()
        self.template = template
        self.mode = mode

    def format(self, logs):
        '''Return formatted data representing *log*.'''
        data = []
        for log in logs:
            data.append(self.vformat(self.template, (), log))

        return data

    def get_field(self, field_name, args, kwargs):
        '''Convert and return *field_name* to an object to be formatted.

        .. note::

            Based on Python's string.Formatter.get_field source.

        '''
        first, rest = field_name._formatter_field_name_split()

        try:
            obj = self.get_value(first, args, kwargs)

            for is_attr, index in rest:
                if is_attr:
                    obj = getattr(obj, index)
                else:
                    obj = obj[index]

        except Exception:
            if self.mode == self.IGNORE:
                return '', first
            else:
                raise

        return obj, first

