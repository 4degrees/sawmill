# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re

from .base import Filterer


class Pattern(Filterer):
    '''Filter logs using pattern matching.'''

    INCLUDE, EXCLUDE = ('include', 'exclude')

    def __init__(self, pattern, key='name', mode=INCLUDE):
        '''Initialise filterer with *pattern* and *key* to test.

        If *pattern* is a string it will be converted to a compiled regular
        expression instance.

        *mode* can be either 'exclude' or 'include'. If set to 'exclude'
        then any log matching the pattern will be filtered. Conversely, if set
        to 'include' then any log not matching the pattern will be filtered.

        '''
        super(Pattern, self).__init__()
        self.pattern = pattern
        if isinstance(self.pattern, basestring):
            self.pattern = re.compile(self.pattern)

        self.key = key
        self.mode = mode

    def filter(self, logs):
        '''Filter *logs* based on pattern matching.

        If a log does not have the key to test against it will pass the
        filter successfully. If the key is present, but not a string then the
        log will be filtered.

        '''
        passed = []
        for log in logs:
            # If key was not present then pass filter
            if self.key not in log:
                passed.append(log)
                continue

            value = log[self.key]

            # If not a string then can't test pattern against it so fail filter.
            if not isinstance(value, basestring):
                continue

            matched = self.pattern.search(value)
            if matched and self.mode == self.EXCLUDE:
                continue

            if not matched and self.mode == self.INCLUDE:
                continue

            passed.append(log)

        return passed

