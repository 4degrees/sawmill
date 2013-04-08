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
    data = template.format([log])
    assert len(data) == 1

    datum = data[0]
    assert isinstance(datum, Message)
    assert datum['Subject'] == 'Test'
    assert datum['From'] == 'sender@test.com'
    assert datum['To'] == 'recipient@test.com'
    assert datum.is_multipart() is True

    html = datum.get_payload(1)
    assert html.get_payload() == '''
<html>
    <body>
        <h1>Logs</h1>
        <span class='info'>
            2013-03-06 10:22:52.847663:test.log:A message
        </span>
    </body>
</html>
'''

    text = datum.get_payload(0)
    assert text.get_payload() == '''# Logs

2013-03-06 10:22:52.847663:test.log:A message

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
    kwargs[key] = lambda logs: value

    template = Email(**kwargs)
    log = Log()
    data = template.format([log])
    assert len(data) == 1

    datum = data[0]
    mapping = {
        'subject': 'Subject',
        'sender': 'From',
        'recipients': 'To'
    }
    assert datum[mapping[key]] == value

