# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from contextlib import nested
from StringIO import StringIO

import mock

import sawmill
import sawmill.log
from sawmill.configurator import classic


def test_classic_configurator_with_no_options():
    '''Test classic configurator when passed no options.'''
    with nested(
        mock.patch('sys.stderr', new_callable=StringIO),
        mock.patch.dict(sawmill.root.handlers, clear=True)
    ) as (stderr, handlers):
        assert len(sawmill.root.handlers) == 0

        # Check handlers added under expected keys
        classic.configure()
        assert sorted(sawmill.root.handlers.keys()) == ['file', 'stderr']

        # Check stderr handler
        assert stderr.getvalue() == ''
        log = sawmill.log.Log(message='Test configurator')
        sawmill.root.handle(log)
        assert stderr.getvalue() == 'Test configurator\n'
        stderr.truncate(0)

        log = sawmill.log.Log(message='Test configurator', level='debug')
        sawmill.root.handle(log)
        assert stderr.getvalue() == ''

        # Check file handler
        sawmill.root.handlers['file'].flush()
        filepath = sawmill.root.handlers['file'].stream.name
        with open(filepath, 'r') as file:
            contents = file.read()
            expected = (
                'message=Test configurator\n'
                'level=debug:message=Test configurator\n'
            )
            assert contents == expected

