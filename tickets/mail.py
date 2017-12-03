import requests


class Postmark(object):
    def __init__(self, token):
        self._token = token

    def send(self, to, subject, body):
        requests.post(
            'https://api.postmarkapp.com/email',
            headers={
                'X-Postmark-Server-Token': self._token,
            },
            json={
                'From': 'd@zerovolt.org',
                'To': to,
                'Subject': subject,
                'TextBody': body
            }).raise_for_status()


class TestMailer(object):
    def send(self, to, subject, body):
        pass
