# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.


from sawmill.log import Log
from sawmill.filterer.item import Item


def test_missing_key_passes_when_mode_is_exclude():
    '''Test log record with missing key passes when mode is exclude.'''
    log = Log()
    filterer = Item('name', 'sawmill.test', mode=Item.EXCLUDE)
    assert filterer.filter([log]) == [log]


def test_missing_key_fails_when_mode_is_include():
    '''Test log record with missing key fails when mode is include.'''
    log = Log()
    filterer = Item('name', 'sawmill.test', mode=Item.INCLUDE)
    assert filterer.filter([log]) == []


def test_include_mode():
    '''Test only logs with matching key, value pass when mode is INCLUDE.'''
    filterer = Item('name', 'sawmill.test.one', mode=Item.INCLUDE)

    log = Log(name='sawmill.test.one')
    assert filterer.filter([log]) == [log]

    log = Log(name='sawmill.test.two')
    assert filterer.filter([log]) == []


def test_exclude_mode():
    '''Test only logs without matching key, value pass when mode is EXCLUDE.'''
    filterer = Item('name', 'sawmill.test.one', mode=Item.EXCLUDE)

    log = Log(name='sawmill.test.one')
    assert filterer.filter([log]) == []

    log = Log(name='sawmill.test.two')
    assert filterer.filter([log]) == [log]

