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
        mock.patch.dict(bark.root.handlers, clear=True)
    ) as (stderr, handlers):
        assert len(bark.root.handlers) == 0

        # Check handlers added under expected keys
        classic.configure()
        assert sorted(bark.root.handlers.keys()) == ['file', 'stderr']

        # Check stderr handler
        assert stderr.getvalue() == ''
        log = bark.log.Log(message='Test configurator')
        bark.root.handle(log)
        assert stderr.getvalue() == 'Test configurator\n'
        stderr.truncate(0)

        log = bark.log.Log(message='Test configurator', level='debug')
        bark.root.handle(log)
        assert stderr.getvalue() == ''

        # Check file handler
        bark.root.handlers['file'].flush()
        filepath = bark.root.handlers['file'].stream.name
        with open(filepath, 'r') as file:
            contents = file.read()
            expected = (
                'level=:name=:message=Test configurator\n'
                'level=debug:name=:message=Test configurator\n'
            )
            assert contents == expected

