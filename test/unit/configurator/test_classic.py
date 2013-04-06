# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from contextlib import nested
from StringIO import StringIO

import mock

import bark
import bark.log
from bark.configurator import classic


def test_classic_configurator_with_no_options():
    '''Test classic configurator when passed no options.'''
    with nested(
        mock.patch('sys.stderr', new_callable=StringIO),
        mock.patch.dict(bark.handler.handlers, clear=True)
    ) as (stderr, handlers):
        assert len(bark.handler.handlers) == 0

        # Check handlers added under expected keys
        classic.configure()
        assert sorted(bark.handler.handlers.keys()) == ['file', 'stderr']

        # Check stderr handler
        assert stderr.getvalue() == ''
        log = bark.log.Log(message='Test configurator')
        bark.handle(log)
        assert stderr.getvalue() == 'Test configurator\n'
        stderr.truncate(0)

        log = bark.log.Log(message='Test configurator', level='debug')
        bark.handle(log)
        assert stderr.getvalue() == ''

        # Check file handler
        bark.handler.handlers['file'].flush()
        filepath = bark.handler.handlers['file'].stream.name
        with open(filepath, 'r') as file:
            contents = file.read()
            expected = (
                'level=:name=:message=Test configurator\n'
                'level=debug:name=:message=Test configurator\n'
            )
            assert contents == expected

