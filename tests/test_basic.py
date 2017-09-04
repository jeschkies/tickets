import pytest
from tickets.app import app
from tickets.views import *  # NOQA


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
