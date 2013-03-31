# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from mock import Mock

from bark.log import Log
from bark.handler.distribute import Distribute


def test_handlers_called():
    '''Test that registered handlers are called.'''
    mock_handler_a = Mock()
    mock_handler_b = Mock()

    distribute = Distribute(handlers={
        'a': mock_handler_a,
        'b': mock_handler_b
    })

    log = Log()
    distribute.handle(log)

    mock_handler_a.handle.assert_called_once_with(log)
    mock_handler_b.handle.assert_called_once_with(log)


def test_no_handlers():
    '''Test calling when no handlers registered.'''
    distribute = Distribute()
    log = Log()
    distribute.handle(log)


def test_handlers_not_called_due_to_filter():
    '''Test that distribute filter prevents handlers being called.'''
    mock_handler_a = Mock()
    deny_all = Mock()
    deny_all.filter = Mock(return_value=True)

    distribute = Distribute(
        filterer=deny_all,
        handlers={
            'a': mock_handler_a,
        }
    )

    log = Log()
    distribute.handle(log)

    assert mock_handler_a.handle.called is False


