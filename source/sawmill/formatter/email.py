# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from __future__ import absolute_import

import collections
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from html2text import html2text

from .mustache import Mustache

#: Default html email template.
DEFAULT_TEMPLATE = '''
<html>
    <body>
        <h1>Logs</h1>
        {{#logs}}
        <span class='{{level}}'>
            {{timestamp}}:{{name}}:{{message}}{{#traceback}}<br/>{{.}}{{/traceback}}
        </span><br/>
        {{/logs}}
    </body>
</html>
'''


class Email(Mustache):
    '''Format :py:class:`logs<sawmill.log.Log>` to email messages.'''

    def __init__(self, subject, sender, recipients, template=DEFAULT_TEMPLATE,
                 batch=True, **kw):
        '''Initialise handler with *subject*, *sender* and *recipients*.

        Each of *subject*, *sender* and *recipients* can be either a static
        string or a callable which will be passed the log records being handled
        and should return an appropriate value.

        *recipients* should be (or return) a string of comma separated email
        addresses.

        '''
        super(Email, self).__init__(template, batch=batch, **kw)
        self.subject = subject
        self.sender = sender
        self.recipients = recipients

    def format(self, logs):
        '''Return email messages representing *logs*.

        Each message will be an instance of :py:class:`~email.message.Message`.
        It will be setup as a multipart message containing both html and plain
        text versions of the logs formatted according to the set template.

        '''
        subject = self.subject
        if isinstance(subject, collections.Callable):
            subject = subject(logs)

        sender = self.sender
        if isinstance(sender, collections.Callable):
            sender = sender(logs)

        recipients = self.recipients
        if isinstance(recipients, collections.Callable):
            recipients = recipients(logs)

        data = []
        entries = super(Email, self).format(logs)
        for html in entries:
            text = html2text(html)

            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = sender
            message['To'] = recipients

            message.attach(MIMEText(text, 'plain'))
            message.attach(MIMEText(html, 'html'))

            data.append(message)

        return data


