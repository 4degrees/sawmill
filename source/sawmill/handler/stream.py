# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from .base import Handler


class Stream(Handler):
    '''Output log records to stream.'''

    def __init__(self, stream, *args, **kw):
        '''Initialise handler with target *stream*.

        .. note::

            The given stream is not managed by this handler. It is not opened
            or closed as it may also be being used elsewhere (such as
            sys.stderr).

        '''
        super(Stream, self).__init__(*args, **kw)
        self.stream = stream

    def teardown(self):
        '''Teardown handler.'''
        try:
            self.flush()
        except (ValueError, IOError):
            # Ignore errors caused by streams that have been closed without
            # corresponding references cleaned up prior to teardown.
            pass

    def flush(self):
        '''Explicitly flush the stream if supported.'''
        if self.stream and hasattr(self.stream, 'flush'):
            self.stream.flush()

    def output(self, data):
        '''Output formatted *data*.

        *data* should be a list of objects able to be written to a stream.

        '''
        for datum in data:
            self.stream.write(datum)
