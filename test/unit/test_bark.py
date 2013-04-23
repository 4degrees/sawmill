# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest
import mock

import mill


def test_default_configure():
    '''Test configure helper with no arguments.'''
    configurators = {'classic': mock.Mock()}
    with mock.patch.dict(
        mill.configurators, configurators, clear=True
    ):
        mill.configure()
        assert configurators['classic'].called


def test_custom_configure():
    '''Test configure helper with specific configurator.'''
    configurators = {'other': mock.Mock()}
    with mock.patch.dict(
        mill.configurators, configurators, clear=True
    ):
        mill.configure(configurator='other')
        assert configurators['other'].called


def test_configure_with_missing_configurator():
    '''Test configure raised ValueError for missing configurator.'''
    with mock.patch.dict(mill.configurators, clear=True):
        with pytest.raises(ValueError):
            mill.configure(configurator='other')

