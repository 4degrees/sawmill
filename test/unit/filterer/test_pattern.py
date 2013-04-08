# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.filterer.pattern import Pattern


def test_missing_key_passes():
    '''Test log record with missing key passes.'''
    log = Log()
    filterer = Pattern('bark\.test\..*')
    assert filterer.filter([log]) == [log]


def test_non_string_key_fails():
    '''Test log record with non-string key fails.'''
    log = Log(name=None)
    filterer = Pattern('bark\.test\..*')
    assert filterer.filter([log]) == []


def test_include_mode():
    '''Test only logs with matching value pass when mode is INCLUDE.'''
    log = Log(name='bark.test.one')
    filterer = Pattern('bark\.test\..*', mode=Pattern.INCLUDE)
    assert filterer.filter([log]) == [log]

    log = Log(name='bark.other.one')
    assert filterer.filter([log]) == []


def test_exclude_mode():
    '''Test only logs with matching value fail when mode is EXCLUDE.'''
    log = Log(name='bark.test.one')
    filterer = Pattern('bark\.test\..*', mode=Pattern.EXCLUDE)
    assert filterer.filter([log]) == []

    log = Log(name='bark.other.one')
    assert filterer.filter([log]) == [log]


def test_different_key():
    '''Test using key other than name.'''
    log = Log()
    filterer = Pattern('A message', key='message')
    assert filterer.filter([log]) == [log]

    log = Log(message='A message')
    filterer = Pattern('A message', key='message')
    assert filterer.filter([log]) == [log]

    log = Log(message='Another message')
    filterer = Pattern('A message', key='message')
    assert filterer.filter([log]) == []

    log = Log(message='A message')
    filterer = Pattern('A message', key='message', mode=Pattern.EXCLUDE)
    assert filterer.filter([log]) == []

