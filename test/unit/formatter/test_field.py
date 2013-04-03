# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.formatter.field import Field


def test_format():
    '''Test formatted log result is as expected.'''
    log = Log(message='A message', level='info')
    template = Field(keys=['level', 'message'])
    assert template.format(log) == 'level=info:message=A message'


def test_alternative_template():
    '''Test configuring the template.'''
    log = Log(message='A message')

    template = Field(keys=['level', 'message'], template='{value}')
    assert template.format(log) == 'A message'


def test_alternative_separator():
    '''Test configuring the separator'''
    log = Log(message='A message', level='info')
    template = Field(keys=['level', 'message'], item_separator=', ')
    assert template.format(log) == 'level=info, message=A message'


def test_no_error_with_missing_values():
    '''Test missing values replaced correctly when mode is IGNORE.'''
    log = Log(message='A message')
    template = Field(keys=['level', 'message'], mode=Field.IGNORE)
    assert template.format(log) == 'level=:message=A message'


def test_error_with_missing_values():
    '''Test missing values cause KeyError when mode is ERROR.'''
    log = Log(message='A message')

    template = Field(keys=['level', 'message'], mode=Field.ERROR)
    with pytest.raises(KeyError):
        template.format(log)


