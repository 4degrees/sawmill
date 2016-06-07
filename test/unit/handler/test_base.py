# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import mock
from mock import Mock

from sawmill.log import Log
from sawmill.handler.base import Handler
from sawmill.formatter.base import Formatter


class Concrete(Handler):
    '''Concrete subclass of abstract base for testing.'''

    def __init__(self, *args, **kw):
        '''Initialise handler.'''
        super(Concrete, self).__init__(*args, **kw)
        self.data = []
        self.teardown_called = 0

    def teardown(self):
        '''Teardown handler.'''
        self.teardown_called += 1

    def output(self, data):
        '''Output formatted *data*.'''
        self.data.extend(data)


class Field(Formatter):
    '''Format logs into list of field strings.'''

    def format(self, logs):
        '''Return each log as a string of log fields.'''
        data = []
        for log in logs:
            entry = []
            for key, value in sorted(log.items()):
                entry.append('{0}={1}'.format(key, value))
            data.append(':'.join(entry))

        return data


def test_handle():
    '''Test handle method.'''
    handler = Concrete()
    log = Log(message='A message')
    handler.handle(log)

    assert handler.data == [log]


def test_filterer():
    '''Test filterer prevents output of log.'''
    deny_all = Mock()
    deny_all.filter = Mock(return_value=[])

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


def test_auto_teardown_on_exit():
    '''Call teardown automatically on exit.'''
    registry = []
    with mock.patch('atexit.register', new=registry.append):
        handler = Concrete(formatter=Field())

    # Manually call registered exit functions.
    for entry in registry:
        entry()

    assert handler.teardown_called
