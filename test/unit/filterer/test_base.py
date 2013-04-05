# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from bark.log import Log
from bark.filterer.base import Filterer, Any, All


class DenyAll(Filterer):
    '''Filter all logs.'''

    def filter(self, log):
        '''Return True if *log* should be filtered.'''
        return True


class AllowAll(Filterer):
    '''Don't filter any log.'''

    def filter(self, log):
        '''Return True if *log* should be filtered.'''
        return False


def test_filter():
    '''Test filter method.'''
    log = Log()

    allow = DenyAll()
    assert allow.filter(log) is True

    deny = AllowAll()
    assert deny.filter(log) is False


def test_and_combine():
    '''Test combining filterers with and operator.'''
    log = Log()
    filterer = DenyAll() & AllowAll()
    assert filterer.filter(log) is False

    filterer = DenyAll()
    filterer &= AllowAll()
    assert filterer.filter(log) is False


def test_and_with_non_filterer_errors():
    '''Test and operator with non-filterer raises NotImplementedError.'''
    with pytest.raises(NotImplementedError):
        DenyAll() & 1


def test_or_combine():
    '''Test combining filterers with or operator.'''
    log = Log()
    filterer = DenyAll() | AllowAll()
    assert filterer.filter(log) is True

    filterer = DenyAll()
    filterer |= AllowAll()
    assert filterer.filter(log) is True


def test_or_with_non_filterer_errors():
    '''Test or operator with non-filterer raises NotImplementedError.'''
    with pytest.raises(NotImplementedError):
        DenyAll() | 1


def test_all():
    '''Test All filterer.'''
    log = Log()

    allow = DenyAll()
    deny = AllowAll()
    filterer = All([allow, deny])
    assert filterer.filter(log) is False

    filterer = All([AllowAll(), AllowAll()])
    assert filterer.filter(log) is False

    filterer = All([DenyAll(), DenyAll()])
    assert filterer.filter(log) is True


def test_all_when_no_filterers_Set():
    '''Test All filterer does not filter when no filterers set.'''
    log = Log()
    filterer = All()
    assert filterer.filter(log) is False


def test_any():
    '''Test Any filterer.'''
    log = Log()

    allow = DenyAll()
    deny = AllowAll()
    filterer = Any([allow, deny])
    assert filterer.filter(log) is True

    filterer = Any([AllowAll(), AllowAll()])
    assert filterer.filter(log) is False

    filterer = Any([DenyAll(), DenyAll()])
    assert filterer.filter(log) is True


def test_any_when_no_filterers_Set():
    '''Test Any filterer does not filter when no filterers set.'''
    log = Log()
    filterer = Any()
    assert filterer.filter(log) is False

