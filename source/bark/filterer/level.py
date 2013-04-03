# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import bark
from .base import Filterer


class Level(Filterer):
    '''Filter logs according to defined log level limits.'''

    def __init__(self, min='info', max=None, levels=bark.levels):
        '''Initialise filterer with *min* and *max* levels.

        The values must be taken from passed *levels* array. If the value given
        is None then it will be as if there is not limit.

        A :py:class:`~bark.log.Log` level value must fall between (inclusive)
        the *min* and *max* values.


        '''
        super(Level, self).__init__()
        self.min = min
        self.max = max
        self.levels = levels

    def filter(self, log):
        '''Filter *log* if its level is not between defined range.

        .. note::

            If the log has no level information (or a level not present in the
            current levels array) it will pass the filter successfully.

        '''
        level = log.get('level')

        # If level information not present then pass filter.
        if level is None:
            return False

        # If level value not recognised, play safe and pass filter.
        try:
            level_index = self.levels.index(level)
        except ValueError:
            return False

        # Check against defined range.
        if self.min is not None:
            min_index = self.levels.index(self.min)
            if level_index < min_index:
                return True

        if self.max is not None:
            max_index = self.levels.index(self.max)
            if level_index > max_index:
                return True

        return False
