# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest
import mock

import bark


def test_default_configure():
    '''Test configure helper with no arguments.'''
    configurators = {'classic': mock.Mock()}
    with mock.patch.dict(
        bark.configurators, configurators, clear=True
    ):
        bark.configure()
        assert configurators['classic'].called


def test_custom_configure():
    '''Test configure helper with specific configurator.'''
    configurators = {'other': mock.Mock()}
    with mock.patch.dict(
        bark.configurators, configurators, clear=True
    ):
        bark.configure(configurator='other')
        assert configurators['other'].called


def test_configure_with_missing_configurator():
    '''Test configure raised ValueError for missing configurator.'''
    with mock.patch.dict(bark.configurators, clear=True):
        with pytest.raises(ValueError):
            bark.configure(configurator='other')

