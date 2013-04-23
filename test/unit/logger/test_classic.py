# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from contextlib import nested

import pytest
import mock

from mill.logger.classic import Classic
from mill.log import Log


def test_log():
    '''Test log method emits correct message.'''
    now = 1234456789
    with nested(
        mock.patch(
            'mill.logger.audit.getpass',
            **{'getuser.return_value': 'thesociable'}
        ),
        mock.patch(
            'mill.logger.audit.time',
            **{'time.return_value': now}
        )
    ):
        handler = mock.Mock()
        logger = Classic(
            'mill.test.classic',
            note='A note',
            _handler=handler
        )

        logger.log('A message', extra_info_a='Extra A')
        assert handler.handle.called

        log = handler.handle.call_args[0][0]
        assert log == Log(
            name='mill.test.classic',
            note='A note',
            message='A message',
            extra_info_a='Extra A',
            timestamp=now,
            username='thesociable'
        )


@pytest.mark.parametrize('level', [
    'debug',
    'info',
    'error',
    'warning'
])
def test_level_helper(level):
    '''Test level helper correctly sets level key.'''
    logger = Classic('mill.test.classic')
    logger.log = mock.Mock()

    message = 'A {0} level message.'.format(level)
    getattr(logger, level)(message)
    assert logger.log.call_args[0] == (message, )
    assert logger.log.call_args[1] == {'level': level}

