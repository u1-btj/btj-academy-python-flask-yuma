import pytest
from httpx import Client


@pytest.mark.anyio
def test_health(client: Client) -> None:
    response = client.get(
        "/api/v1/health/",
    )
    assert 200 == response.status_code