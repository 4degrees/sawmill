# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from ._version import __version__
from .handler.distribute import Distribute

#: Top level handler responsible for relaying all logs to other handlers.
root = Distribute()

#: Log levels ordered by severity. Do not rely on the index of the level name
# as it may change depending on the configuration.
levels = [
    'debug',
    'info',
    'warning',
    'error'
]

# Import configurators here to avoid configurators getting null references
# to above variables.
from .configurator import classic

#: Configurators registered for use with the :py:func:`sawmill.configure`
#: function.
configurators = {
    'classic': classic.configure
}


def configure(configurator='classic', *args, **kw):
    '''Configure Mill using *configurator*.

    Will call registered configuration function matching the *configurator*
    name with *args*, and *kw*.

    '''
    configurator = configurators.get(configurator)
    if configurator is None:
        raise ValueError('No configurator found with name {0}. Check that '
                         'the configurator is registered correctly in the '
                         'sawmill.configurators dictionary.')

    configurator(*args, **kw)

