# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .handler.distribute import Distribute
from .configurator import classic

#: Top level handler responsible for relaying all logs to other handlers.
handler = Distribute()
handlers = handler.handlers

#: Main handle method that should be called with :py:class:`~bark.log.Log`
#: instances.
handle = handler.handle

#: Log levels ordered by severity. Do not rely on the index of the level name
# as it may change depending on the configuration.
levels = [
    'debug',
    'info',
    'warning',
    'error'
]

#: Configurators registered for use with the :py:func:`bark.configure`
#: function.
configurators = {
    'classic': classic.configure
}


def configure(configurator='classic', *args, **kw):
    '''Configure Bark using *configurator*.

    Will call registered configuration function matching the *configurator*
    name with *args*, and *kw*.

    '''
    configurator = configurators.get(configurator)
    if configurator is None:
        raise ValueError('No configurator found with name {0}. Check that '
                         'the configurator is registered correctly in the '
                         'bark.configurators dictionary.')

    configurator(*args, **kw)

