import bcrypt
import pytest
from httpx import Client
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import User

PASSWORD="Test123!"
pw_bytes = PASSWORD.encode()
salt = bcrypt.gensalt()
hashed_pw = bcrypt.hashpw(
    password=pw_bytes,
    salt=salt,
)
USER = User(name="Test User", email="testuser@email.com", username="testuser", password=hashed_pw.decode())

def setup_data(session: Session) -> None:  
    session.add_all([USER])
    session.flush()
    session.commit()

@pytest.mark.anyio
def test_auth_views(client: Client, session: Session) -> None:
    # setup
    setup_data(session)

    """Register"""
    users = session.execute(select(User))
    users_count = len(users.scalars().all())
    print(users.scalars().all())

    payload = {
        "name": "Test Register", 
        "username": "testregister", 
        "email": "testregister@email.com", 
        "password": "TestRegister123!"
    }

    # execute
    response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert 200 == response.status_code
    assert response.json()["data"]["username"] == payload["username"]

    users = session.execute(select(User))

    assert users_count + 1 == len(users.scalars().all())

    print(users.scalars().all())
    """Login"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username":"testuser",
            "password":PASSWORD
        }
    )

    print(response.json())
    assert 200 == response.status_code

    """Refresh Token"""
    REFRESH_TOKEN = response.json()["data"]["refresh_token"]
    response = client.get(
        "/api/v1/auth/refresh-token",
        headers={
            "Authorization": "Bearer " + REFRESH_TOKEN 
        }
    )

    assert 200 == response.status_code
    assert response.json()["data"]["access_token"] is not None

    """Change Password"""
    ACCESS_TOKEN = response.json()["data"]["access_token"]
    response = client.put(
        "/api/v1/auth/change-password",
        headers={
            "Authorization": "Bearer " + ACCESS_TOKEN 
        },
        json={
            "old_password":PASSWORD,
            "new_password":PASSWORD+"!"
        }
    )

    assert 200 == response.status_code