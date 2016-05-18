# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from sawmill.log import Log
from sawmill.formatter.template import Template


def test_format():
    '''Test formatted log result is as expected.'''
    log = Log(message='A message', level='info')
    template = Template('{level}:{message}')
    assert template.format([log]) == ['info:A message']


def test_missing_key_set_to_substitute():
    '''Test missing values replaced when missing_key set to a substitute.'''
    log = Log(message='A message')
    template = Template('{level}:{message}', missing_key='None')
    assert template.format([log]) == ['None:A message']


def test_missing_key_set_to_error():
    '''Test missing values raise KeyError when missing_key set to ERROR.'''
    log = Log(message='A message', data=[1, 2])

    # Missing key
    template = Template('{level}:{message}', missing_key=Template.ERROR)
    with pytest.raises(KeyError):
        template.format([log])

    # Invalid attribute
    template = Template('{message.type}', missing_key=Template.ERROR)
    with pytest.raises(AttributeError):
        template.format([log])

    # Invalid index
    template = Template('{data[3]}', missing_key=Template.ERROR)
    with pytest.raises(IndexError):
        template.format([log])

