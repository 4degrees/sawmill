# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import string

from .base import Formatter


class Template(Formatter, string.Formatter):
    '''Format :py:class:`logs<sawmill.log.Log>` according to a template.'''

    ERROR = ('__ERROR__')

    def __init__(self, template, missing_key=''):
        '''Initialise formatter with *template*.

        *missing_key* determines how to handle a missing key when formatting a
        log. If set to :py:attr:`ERROR` then an error will be raised for any
        key referenced in the template that is missing from the log. Any other
        value will be used as the substitute for the missing value. The default
        is an empty string.

        .. note::

            The template is applied once per processed log.

        '''
        super(Template, self).__init__()
        self.template = template
        self.missing_key = missing_key

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
            if self.missing_key == self.ERROR:
                raise
            else:
                return self.missing_key, first

        return obj, first

