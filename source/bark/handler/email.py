# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from __future__ import absolute_import

import smtplib

from .base import Handler


class Email(Handler):
    '''Output log records to email.'''

    def __init__(self, host='localhost', port=smtplib.SMTP_PORT,
                 credentials=None,
                 *args, **kw):
        '''Initialise handler with *host* and *port* to connect to SMTP server.

        *credentials* may be supplied as a tuple of (username, password) if
        the server requires a login.

        .. note::

            Messages are expected to be constructed by the formatter and is
            where attributes such as sender, recipients, subject and content
            should be set.

        '''
        super(Email, self).__init__(*args, **kw)
        self.host = host
        self.port = port
        self.credentials = credentials

    def output(self, data):
        '''Output formatted *data*.

        *data* should be a list of prepared :py:class:`~email.message.Message`
        instances that will be sent using the configured SMTP server. In
        addition each message must specify the keys 'To' and 'From' which will
        be used when sending the email.

        '''
        smtp = smtplib.SMTP(self.host, self.port)
        if self.credentials:
            smtp.login(*self.credentials)

        for datum in data:
            smtp.sendmail(
                datum['From'],
                datum['To'].split(','),
                datum.as_string()
            )
        smtp.quit()

