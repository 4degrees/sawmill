# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log


def test_create():
    '''Test creating a Log instance.'''
    log = Log(name='bark.test.log')
    assert log.items() == [('name', 'bark.test.log')]


def test_string_represenation():
    '''Test string representation of Log instance.'''
    log = Log(name='bark.test.log')
    assert str(log) == "{'name': 'bark.test.log'}"


def test_length():
    '''Test len method returns number of current keys.'''
    log = Log(name='bark.test.log')
    assert len(log) == 1
    log['message'] = 'A message'
    assert len(log) == 2


def test_setting_and_getting_item():
    '''Test setting and getting key value pair.'''
    log = Log()
    assert len(log) == 0
    log['message'] = 'A message'
    assert len(log) == 1
    assert log['message'] == 'A message'


def test_delete_item():
    '''Test removing an item.'''
    log = Log()
    assert len(log) == 0
    log['message'] = 'A message'
    assert len(log) == 1
    assert log['message'] == 'A message'

    del log['message']
    assert len(log) == 0
    with pytest.raises(KeyError):
        log['message']

