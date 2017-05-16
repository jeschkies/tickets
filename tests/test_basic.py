import pytest
from tickets import tickets

@pytest.fixture
def client():
    return tickets.app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
