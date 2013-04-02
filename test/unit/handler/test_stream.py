# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from mock import Mock

from bark.log import Log
from bark.handler.stream import Stream


def test_output():
    '''Test outputting to specified stream.'''
    target = StringIO()
    formatter = Mock()
    formatter.format = Mock(return_value='A message')

    stream = Stream(
        stream=target,
        formatter=formatter
    )

    log = Log(level='info', message='A message')
    stream.handle(log)

    assert target.getvalue() == 'A message'


def test_flush_when_supported_by_stream():
    '''Test flush when supported by stream.'''
    target = Mock()
    target.flush = Mock()

    stream = Stream(
        stream=target,
    )

    stream.flush()

    assert target.flush.called


def test_flush_when_unsupported_by_stream():
    '''Test flush executes without error when unsupported by stream.'''
    target = Mock()

    stream = Stream(
        stream=target,
    )

    stream.flush()


def test_auto_flush_on_exit():
    '''Test flush is called automatically on exit.'''
    target = Mock()
    stream = Stream(
        stream=target,
    )
    stream.flush = Mock()

    # Manually call the exitfunc that atexit registers against.
    sys.exitfunc()

    assert stream.flush.called

