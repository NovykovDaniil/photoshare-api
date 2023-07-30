import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_estimate_photo(test_client):
    photo_id = "your_photo_id_here"
    estimate_data = {"photo_id": photo_id, "estimate": 4}

    response = await test_client.post(f"/estimates/{photo_id}", json=estimate_data)

    assert response.status_code == 200
    assert "estimate" in response.json()
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_get_estimates(test_client):
    photo_id = "existing_photo_id_here"
    response = await test_client.get(f"/estimates/{photo_id}")

    assert response.status_code == 200
    assert "estimates" in response.json()
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_delete_estimate(test_client):
    estimate_id = "existing_estimate_id_here"
    delete_data = {"estimate_id": estimate_id}

    response = await test_client.delete(f"/estimates/{estimate_id}", json=delete_data)

    assert response.status_code == 200
    assert "estimate" in response.json()
    assert "detail" in response.json()