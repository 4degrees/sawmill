# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest
import mock

from bark.logger.base import Logger
from bark.log import Log


def test_log():
    '''Test log method emits correct message.'''
    handler = mock.Mock()
    logger = Logger(name='bark.test.logger', _handler=handler)
    logger.log(message='A message')
    assert handler.handle.called
    assert handler.handle.call_args[0][0] == Log(
        name='bark.test.logger',
        message='A message',
    )


def test_prepare_returns_distinct_copy():
    '''Test prepare returns a distinct copy of the logger.'''
    logger = Logger(name='bark.test.logger')
    log = logger.prepare()
    assert log is not logger


def test_repeat_call_side_effects():
    '''Test repeat calls with different arguments have no side-effects.'''
    handler = mock.Mock()
    logger = Logger(name='bark.test.logger', _handler=handler)
    logger.log(message_a='Message A')
    assert handler.handle.call_args[0][0] == Log(
        name='bark.test.logger',
        message_a='Message A',
    )

    # Confirm new message with different parameters does not have previous
    # data.
    logger.log(message_b='Message B')
    assert handler.handle.call_args[0][0] == Log(
        name='bark.test.logger',
        message_b='Message B',
    )

