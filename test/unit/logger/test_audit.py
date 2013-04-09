# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from contextlib import nested

import mock

from bark.logger.audit import Audit


def test_adding_audit_information():
    '''Test adding audit information automatically.'''
    now = 987654321
    with nested(
        mock.patch(
            'bark.logger.audit.getpass',
            **{'getuser.return_value': 'thesociable'}
        ),
        mock.patch(
            'bark.logger.audit.time',
            **{'time.return_value': now}
        )
    ):
        handler = mock.Mock()
        logger = Audit(_handler=handler)
        logger.log('Test audit.')

        log = handler.handle.call_args[0][0]
        assert log.get('username') == 'thesociable'
        assert log.get('timestamp') == now


def test_adding_audit_information_doesnt_overwrite():
    '''Test audit information not added when already present.'''
    handler = mock.Mock()
    logger = Audit(_handler=handler)
    logger.log('Test audit.', timestamp=123456789, username='me')

    log = handler.handle.call_args[0][0]
    assert log.get('username') == 'me'
    assert log.get('timestamp') == 123456789
