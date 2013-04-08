# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.formatter.template import Template


def test_format():
    '''Test formatted log result is as expected.'''
    log = Log(message='A message', level='info')
    template = Template('{level}:{message}')
    assert template.format([log]) == ['info:A message']


def test_no_error_with_missing_values():
    '''Test missing values replaced correctly when mode is IGNORE.'''
    log = Log(message='A message')
    template = Template('{level}:{message}', mode=Template.IGNORE)
    assert template.format([log]) == [':A message']


def test_error_with_missing_values():
    '''Test missing values cause KeyError when mode is ERROR.'''
    log = Log(message='A message', data=[1, 2])

    # Missing key
    template = Template('{level}:{message}', mode=Template.ERROR)
    with pytest.raises(KeyError):
        template.format([log])

    # Invalid attribute
    template = Template('{message.type}', mode=Template.ERROR)
    with pytest.raises(AttributeError):
        template.format([log])

    # Invalid index
    template = Template('{data[3]}', mode=Template.ERROR)
    with pytest.raises(IndexError):
        template.format([log])

