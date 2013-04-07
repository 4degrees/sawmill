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
        <h1>Log Message</h1>
        {{#name}}Logger: {{.}}<br/>{{/name}}
        {{#created}}Datetime: {{.}}<br/>{{/created}}
        <p class='{{level}}'>
            {{message}}
            {{traceback}}
        </p>
    </body>
</html>
'''


class Email(Mustache):
    '''Format :py:class:`~bark.log.Log` to email message instance.'''

    def __init__(self, subject, sender, recipients, template=DEFAULT_TEMPLATE,
                 **kw):
        '''Initialise handler with *subject*, *sender* and *recipients*.

        Each of *subject*, *sender* and *recipients* can be either a static
        string or a callable which will be passed the log record being handled
        and should return an appropriate value.

        *recipients* should be (or return) a string of comma separated email
        addresses.

        '''
        super(Email, self).__init__(template, **kw)
        self.subject = subject
        self.sender = sender
        self.recipients = recipients

    def format(self, log):
        '''Return :py:class:`~email.message.Message` representing *log*.

        The message will be a multipart message containing both html and plain
        text versions of the log formatted according to the set template.

        '''
        html = super(Email, self).format(log)
        text = html2text(html)

        subject = self.subject
        if isinstance(subject, collections.Callable):
            subject = subject(log)

        sender = self.sender
        if isinstance(sender, collections.Callable):
            sender = sender(log)

        recipients = self.recipients
        if isinstance(recipients, collections.Callable):
            recipients = recipients(log)

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = recipients

        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))

        return message

