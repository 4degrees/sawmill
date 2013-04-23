# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from mock import Mock

from mill.log import Log
from mill.handler.buffer import Buffer


def test_handler_called_on_trigger():
    '''Test that wrapped handler is called when trigger returns True.'''
    wrapped_handler = Mock()

    handler = Buffer(
        wrapped_handler,
        lambda logs, buffer: len(buffer) > 4
    )

    logs = []

    for index in range(4):
        log = Log(index=index)
        logs.append(log)
        handler.handle(log)
        assert wrapped_handler.handle.called is False

    handler.handle(log)
    logs.append(log)
    wrapped_handler.handle.assert_called_once_with(*logs)


def test_buffer_cleared_post_trigger():
    '''Test buffer is cleared after successful trigger.'''
    handler = Buffer(
        Mock(),
        lambda logs, buffer: len(buffer) > 4
    )

    for index in range(1, 5):
        log = Log(index=index)
        handler.handle(log)
        assert len(handler.buffer) == index

    handler.handle(log)
    assert len(handler.buffer) == 0


def test_buffer_does_not_exceed_limit():
    '''Test buffer size does not grow beyond set limit.'''
    handler = Buffer(
        Mock(),
        lambda logs, buffer: False,
        limit=10
    )

    assert len(handler.buffer) == 0

    for index in range(20):
        log = Log(index=index)
        handler.handle(log)

    assert len(handler.buffer) == 10

