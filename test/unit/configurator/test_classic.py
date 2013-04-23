# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from contextlib import nested
from StringIO import StringIO

import mock

import mill
import mill.log
from mill.configurator import classic


def test_classic_configurator_with_no_options():
    '''Test classic configurator when passed no options.'''
    with nested(
        mock.patch('sys.stderr', new_callable=StringIO),
        mock.patch.dict(mill.root.handlers, clear=True)
    ) as (stderr, handlers):
        assert len(mill.root.handlers) == 0

        # Check handlers added under expected keys
        classic.configure()
        assert sorted(mill.root.handlers.keys()) == ['file', 'stderr']

        # Check stderr handler
        assert stderr.getvalue() == ''
        log = mill.log.Log(message='Test configurator')
        mill.root.handle(log)
        assert stderr.getvalue() == 'Test configurator\n'
        stderr.truncate(0)

        log = mill.log.Log(message='Test configurator', level='debug')
        mill.root.handle(log)
        assert stderr.getvalue() == ''

        # Check file handler
        mill.root.handlers['file'].flush()
        filepath = mill.root.handlers['file'].stream.name
        with open(filepath, 'r') as file:
            contents = file.read()
            expected = (
                'message=Test configurator\n'
                'level=debug:message=Test configurator\n'
            )
            assert contents == expected

