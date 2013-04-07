# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

from email.message import Message

import pytest

from bark.log import Log
from bark.formatter.email import Email


def test_format():
    '''Test formatted log result is as expected.'''
    log = Log(
        created='2013-03-06 10:22:52.847663',
        name='test.log',
        message='A message',
        level='info'
    )
    template = Email('Test', 'sender@test.com', 'recipient@test.com')
    data = template.format(log)
    assert isinstance(data, Message)
    assert data['Subject'] == 'Test'
    assert data['From'] == 'sender@test.com'
    assert data['To'] == 'recipient@test.com'
    assert data.is_multipart() is True

    html = data.get_payload(1)
    assert html.get_payload() == '''
<html>
    <body>
        <h1>Log Message</h1>
        Logger: test.log<br/>
        Datetime: 2013-03-06 10:22:52.847663<br/>
        <p class='info'>
            A message
            
        </p>
    </body>
</html>
'''

    text = data.get_payload(0)
    assert text.get_payload() == '''# Log Message

Logger: test.log

Datetime: 2013-03-06 10:22:52.847663

A message

'''


@pytest.mark.parametrize(('key', 'value'), [
    ('subject', 'A Test'),
    ('sender', 'me@test.com'),
    ('recipients', 'you@test.com')
])
def test_callable(key, value):
    '''Test callable'''
    kwargs = {
        'subject': 'Test',
        'sender': 'sender@test.com',
        'recipients': 'recipient@test.com'
    }
    kwargs[key] = lambda log: value

    template = Email(**kwargs)
    log = Log()
    data = template.format(log)
    mapping = {
        'subject': 'Subject',
        'sender': 'From',
        'recipients': 'To'
    }
    assert data[mapping[key]] == value

