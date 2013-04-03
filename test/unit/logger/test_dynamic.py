# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest
import mock

from bark.logger.dynamic import Dynamic


def test_non_dyanmic_item_access():
    '''Test normal item access is successful.'''
    logger = Dynamic()
    logger['a'] = 'A string'

    assert logger['a'] == 'A string'
    with pytest.raises(KeyError):
        logger['b']


def test_dynamic_item_access():
    '''Test dynamic item access is successful.'''
    logger = Dynamic()
    compute = mock.Mock(return_value='A string')

    logger['a'] = compute
    assert logger['a'] == 'A string'
    assert compute.called == 1


def test_dynamic_item_access_is_cached():
    '''Test dynamic item access is computed only once.'''
    logger = Dynamic()
    compute = mock.Mock(return_value='A string')

    logger['a'] = compute
    assert logger['a'] == 'A string'
    assert compute.call_count == 1

    assert logger['a'] == 'A string'
    assert compute.call_count == 1
