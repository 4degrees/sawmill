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
    assert template.format([log]) == ['level=info:message=A message\n']


def test_alternative_template():
    '''Test configuring the template.'''
    log = Log(message='A message')

    template = Field(keys=['level', 'message'], template='{value}')
    assert template.format([log]) == ['A message\n']


def test_alternative_separator():
    '''Test configuring the separator'''
    log = Log(message='A message', level='info')
    template = Field(keys=['level', 'message'], item_separator=', ')
    assert template.format([log]) == ['level=info, message=A message\n']


def test_missing_key_set_to_skip():
    '''Test missing values skipped when missing_key set to SKIP.'''
    log = Log(message='A message')
    template = Field(keys=['level', 'message'], missing_key=Field.SKIP)
    assert template.format([log]) == ['message=A message\n']


def test_missing_key_set_to_substitute():
    '''Test missing values replaced when missing_key set to a substitute.'''
    log = Log(message='A message')
    template = Field(keys=['level', 'message'], missing_key='NOT_SET')
    assert template.format([log]) == ['level=NOT_SET:message=A message\n']


def test_missing_key_set_to_error():
    '''Test missing values raise KeyError when missing_key set to ERROR.'''
    log = Log(message='A message')

    template = Field(keys=['level', 'message'], missing_key=Field.ERROR)
    with pytest.raises(KeyError):
        template.format([log])


@pytest.mark.parametrize(('keys', 'expected'), [
    (['*', 'level', 'message'], ['a=3:b=2:z=1:level=info:message=A message\n']),
    (['level', '*', 'message'], ['level=info:a=3:b=2:z=1:message=A message\n']),
    (['level', 'message', '*'], ['level=info:message=A message:a=3:b=2:z=1\n']),
    (['*'], ['a=3:b=2:level=info:message=A message:z=1\n']),
    (['*', '*'], (['a=3:b=2:level=info:message=A message:z=1:'
                   'a=3:b=2:level=info:message=A message:z=1\n']))
])
def test_include_remaining_keys(keys, expected):
    '''Test using '*' to include remaining keys in alphabetical order.'''
    log = Log(level='info', message='A message', a=3, b=2, z=1)

    template = Field(keys=keys)
    assert template.format([log]) == expected

