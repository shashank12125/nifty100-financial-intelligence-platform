import threading
import time

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def call_api():
    """Send a request to the screener API."""
    response = client.get("/api/v1/screener")
    assert response.status_code == 200


def test_screener_load():
    """Test concurrent load on the screener API."""
    threads = []

    start = time.perf_counter()

    for _ in range(10):
        t = threading.Thread(target=call_api)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start

    print(f"\nTotal Time: {elapsed:.2f} seconds")

    assert elapsed < 10