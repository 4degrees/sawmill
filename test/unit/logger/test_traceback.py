# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import mock

from mill.logger.traceback import Traceback


def test_extracting_traceback():
    '''Test extracting traceback when key set to True.'''
    handler = mock.Mock()
    logger = Traceback(_handler=handler)
    try:
        raise ValueError('Forced error')
    except Exception:
        logger.log(traceback=True)

    log = handler.handle.call_args[0][0]
    assert isinstance(log['traceback'], basestring)

    lines = log['traceback'].splitlines()
    assert lines[0] == 'Traceback (most recent call last):'
    assert lines[-1] == 'ValueError: Forced error'


def test_custom_traceback():
    '''Test setting traceback manually.'''
    handler = mock.Mock()
    logger = Traceback(_handler=handler)
    logger.log(traceback='Some other value')

    log = handler.handle.call_args[0][0]
    assert log['traceback'] == 'Some other value'


def test_extracting_traceback_outside_exception():
    '''Test extracting traceback outside exception.'''
    handler = mock.Mock()
    logger = Traceback(_handler=handler)
    logger.log(traceback=True)

    log = handler.handle.call_args[0][0]
    assert log['traceback'] == 'None'
