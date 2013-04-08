# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.filterer.level import Level


def pytest_funcarg__levels(request):
    '''Return levels.'''
    return [
        'debug',
        'info',
        'warning',
        'error'
    ]


def test_no_level_present(levels):
    '''Test log record with no level information passes.'''
    log = Log()
    filterer = Level(levels=levels)
    assert filterer.filter([log]) == [log]


def test_invalid_level(levels):
    '''Test invalid level on log passes filter.'''
    log = Log(level='invalid_level')
    filterer = Level(levels=levels)
    assert filterer.filter([log]) == [log]


def test_invalid_min_level(levels):
    '''Test invalid min level on filterer raises ValueError.'''
    log = Log(level='info')
    filterer = Level(min='invalid_level', levels=levels)
    with pytest.raises(ValueError):
        filterer.filter([log])


def test_invalid_max_level(levels):
    '''Test invalid max level on filterer raises ValueError.'''
    log = Log(level='info')
    filterer = Level(max='invalid_level', levels=levels)
    with pytest.raises(ValueError):
        filterer.filter([log])


def test_filter_below_min_level(levels):
    '''Test log with level below min does not pass.'''
    log = Log(level='info')
    filterer = Level(min='warning', levels=levels)
    assert filterer.filter([log]) == []


def test_filter_above_max_level(levels):
    '''Test log with level above max does not pass.'''
    log = Log(level='error')
    filterer = Level(max='warning', levels=levels)
    assert filterer.filter([log]) == []


def test_against_limitless_range(levels):
    '''Test log passes against a limitless range.'''
    log = Log(level='info')
    filterer = Level(min=None, max=None, levels=levels)
    assert filterer.filter([log]) == [log]

