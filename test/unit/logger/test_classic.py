# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest
import mock

from bark.logger.classic import Classic
from bark.log import Log


def test_log():
    '''Test log method emits correct message.'''
    handler = mock.Mock()
    logger = Classic(
        'bark.test.classic',
        note='A note',
        _handler=handler
    )
    logger.log('A message', extra_info_a='Extra A')
    assert handler.handle.called
    assert handler.handle.call_args[0][0] == Log(
        name='bark.test.classic',
        note='A note',
        message='A message',
        extra_info_a='Extra A'
    )


@pytest.mark.parametrize('level', [
    'debug',
    'info',
    'error',
    'warning'
])
def test_level_helper(level):
    '''Test level helper correctly sets level key.'''
    logger = Classic('bark.test.classic')
    logger.log = mock.Mock()

    message = 'A {0} level message.'.format(level)
    getattr(logger, level)(message)
    assert logger.log.call_args[0] == (message, )
    assert logger.log.call_args[1] == {'level': level}

