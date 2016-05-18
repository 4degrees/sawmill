# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pystache

from .base import Formatter


class Mustache(Formatter):
    '''Format :py:class:`logs<sawmill.log.Log>` using Mustache template.'''

    def __init__(self, template, batch=False):
        '''Initialise formatter with *template*.

        If *batch* is False then the template will be applied for each log
        received. Otherwise all received logs will be passed to template at
        once under the key 'logs'.

        '''
        super(Mustache, self).__init__()
        self.template = template
        self.batch = batch

    def format(self, logs):
        '''Return formatted data representing *logs*.

        If self.batch is False then each log will be passed to the template
        separately as the context. Otherwise, all the logs will be passed as
        the context.

        '''
        data = []
        if self.batch:
            data.append(pystache.render(self.template, logs=logs))
        else:
            for log in logs:
                data.append(pystache.render(self.template, log))

        return data

