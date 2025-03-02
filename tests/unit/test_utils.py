import pytest
from datetime import timedelta
from bookstore.utils import create_access_token
import jwt
from bookstore.constants import SECRET_KEY, ALGORITHM

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=1))
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "test@example.com"
    assert "exp" in decoded_token

def test_create_access_token_default_expiry():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in decoded_token