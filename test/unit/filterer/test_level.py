# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.filterer.level import Level


def test_no_level_present():
    '''Test log record with no level information passes.'''
    log = Log()
    filterer = Level()
    assert filterer.filter(log) is False


def test_invalid_level():
    '''Test invalid level on log passes filter.'''
    log = Log(level='invalid_level')
    filterer = Level()
    assert filterer.filter(log) is False


def test_invalid_min_level():
    '''Test invalid min level on filterer raises ValueError.'''
    log = Log(level='info')
    filterer = Level(min='invalid_level')
    with pytest.raises(ValueError):
        filterer.filter(log)


def test_invalid_max_level():
    '''Test invalid max level on filterer raises ValueError.'''
    log = Log(level='info')
    filterer = Level(max='invalid_level')
    with pytest.raises(ValueError):
        filterer.filter(log)


def test_filter_below_min_level():
    '''Test log with level below min does not pass.'''
    log = Log(level='info')
    filterer = Level(min='warning')
    assert filterer.filter(log) is True


def test_filter_above_max_level():
    '''Test log with level above max does not pass.'''
    log = Log(level='error')
    filterer = Level(max='warning')
    assert filterer.filter(log) is True


def test_against_limitless_range():
    '''Test log passes against a limitless range.'''
    log = Log(level='info')
    filterer = Level(min=None, max=None)
    assert filterer.filter(log) is False

