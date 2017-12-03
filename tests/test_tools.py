import pytest
from tickets.tools import external_url_for
from tickets.app import app


@pytest.fixture
def client():
    with app.app_context():
        yield app.test_client()


def test_external_url_for(client):
    assert external_url_for(
        'purchase', purchase_id="123",
        secret="456") == "http://127.0.0.1:5000/purchase/123?secret=456"
