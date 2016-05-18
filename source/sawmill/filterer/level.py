# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sawmill
from .base import Filterer


class Level(Filterer):
    '''Filter logs according to defined log level limits.'''

    def __init__(self, min='info', max=None, levels=sawmill.levels):
        '''Initialise filterer with *min* and *max* levels.

        The values must be taken from passed *levels* array. If the value given
        is None then it will be as if there is not limit.

        A :py:class:`~sawmill.log.Log` level value must fall between (inclusive)
        the *min* and *max* values.


        '''
        super(Level, self).__init__()
        self.min = min
        self.max = max
        self.levels = levels

    def filter(self, logs):
        '''Return *logs* whose level is between the defined range.

        .. note::

            If a log has no level information (or a level not present in the
            current levels array) it will pass the filter successfully.

        '''
        passed = []
        for log in logs:
            level = log.get('level')

            # If level information not present then pass filter.
            if level is None:
                passed.append(log)
                continue

            # If level value not recognised, play safe and pass filter.
            try:
                level_index = self.levels.index(level)
            except ValueError:
                passed.append(log)
                continue

            # Check against defined range.
            if self.min is not None:
                min_index = self.levels.index(self.min)
                if level_index < min_index:
                    continue

            if self.max is not None:
                max_index = self.levels.index(self.max)
                if level_index > max_index:
                    continue

            passed.append(log)

        return passed
