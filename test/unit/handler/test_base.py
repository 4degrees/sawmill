# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from mock import Mock

from bark.log import Log
from bark.handler.base import Handler
from bark.formatter.base import Formatter


class Concrete(Handler):
    '''Concrete subclass of abstract base for testing.'''

    def __init__(self, *args, **kw):
        '''Initialise handler.'''
        super(Concrete, self).__init__(*args, **kw)
        self.data = []

    def output(self, data):
        '''Output formatted *data*.'''
        self.data.append(data)


class Field(Formatter):
    '''Format log into string of fields.'''

    def format(self, log):
        '''Return string of log fields.'''
        data = []
        for key, value in sorted(log.items()):
            data.append('{0}={1}'.format(key, value))
        return ':'.join(data)


def test_handle():
    '''Test handle method.'''
    handler = Concrete()
    log = Log(message='A message')
    handler.handle(log)

    assert handler.data == [log]


def test_filterer():
    '''Test filterer prevents output of log.'''
    deny_all = Mock()
    deny_all.filter = Mock(return_value=True)

    handler = Concrete(filterer=deny_all)
    log = Log(message='A message')
    handler.handle(log)

    assert handler.data == []


def test_formatter():
    '''Test formatting of data before output.'''
    handler = Concrete(formatter=Field())
    log = Log(message='A message')
    handler.handle(log)

    assert handler.data == ['message=A message']
