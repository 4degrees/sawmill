# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pystache

from .base import Formatter


class Mustache(Formatter):
    '''Format :py:class:`~bark.log.Log` according to a mustache template.'''

    def __init__(self, template):
        '''Initialise formatter with *template*.'''
        super(Mustache, self).__init__()
        self.template = template

    def format(self, log):
        '''Return formatted data representing *log*.'''
        return pystache.render(self.template, **log)

