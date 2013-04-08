# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import mock

from bark.log import Log
from bark.formatter.email import Email as EmailFormatter
from bark.handler.email import Email


def test_output():
    '''Test outputting to email.'''
    with mock.patch('bark.handler.email.smtplib.SMTP', spec=True) as SMTP:
        host = 'emailhost'
        port = 90210
        handler = Email(
            host=host,
            port=port,
            formatter=EmailFormatter(
                'Test',
                'sender@test.com',
                'recipient@test.com'
            )
        )
        log = Log(level='info', message='A message')
        handler.handle(log)

        SMTP.assert_called_with(host, port)
        smtp = SMTP.return_value
        assert smtp.sendmail.called is True
        assert smtp.quit.called is True


def test_login_when_credentials_present():
    '''Test login is called when credentials available.'''
    with mock.patch('bark.handler.email.smtplib.SMTP', spec=True) as SMTP:
        handler = Email(
            credentials=('me@test.com', 'mypassword'),
            formatter=EmailFormatter(
                'Test',
                'sender@test.com',
                'recipient@test.com'
            )
        )
        log = Log(level='info', message='A message')
        handler.handle(log)

        smtp = SMTP.return_value
        smtp.login.assert_called_with('me@test.com', 'mypassword')


def test_no_login_when_credentials_not_present():
    '''Test login is not called when credentials not available.'''
    with mock.patch('bark.handler.email.smtplib.SMTP', spec=True) as SMTP:
        handler = Email(
            formatter=EmailFormatter(
                'Test',
                'sender@test.com',
                'recipient@test.com'
            )
        )
        log = Log(level='info', message='A message')
        handler.handle(log)

        smtp = SMTP.return_value
        assert smtp.login.called is False

