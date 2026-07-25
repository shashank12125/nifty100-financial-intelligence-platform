from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_sectors():

    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_sector_companies():

    # Get available sectors
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200

    sectors = response.json()
    assert len(sectors) > 0

    sector_name = sectors[0]["sector"]

    # Test companies endpoint using an existing sector
    response = client.get(f"/api/v1/sectors/{sector_name}/companies")

    assert response.status_code == 200

    rows = response.json()

    assert isinstance(rows, list)