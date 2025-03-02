import pytest
from bookstore.middleware import JWTBearer
from unittest.mock import patch
from fastapi import HTTPException
from fastapi import Request
import jwt
from bookstore.constants import SECRET_KEY, ALGORITHM

@pytest.mark.asyncio
async def test_jwt_bearer_valid_token():
    with patch("jwt.decode", return_value={"sub": "test@example.com"}):
        bearer = JWTBearer()
        request = Request({"type": "http", "headers": [(b"authorization", b"Bearer valid_token")]})
        token = await bearer(request)
        assert token == "valid_token"

@pytest.mark.asyncio
async def test_jwt_bearer_invalid_token():
    with patch("jwt.decode", side_effect=jwt.PyJWTError):
        bearer = JWTBearer()
        request = Request({"type": "http", "headers": [(b"authorization", b"Bearer invalid_token")]})
        with pytest.raises(HTTPException) as exc_info:
            await bearer(request)
        assert exc_info.value.status_code == 403

@pytest.mark.asyncio
async def test_jwt_bearer_missing_token():
    bearer = JWTBearer()
    request = Request({"type": "http", "headers": []})
    with pytest.raises(HTTPException) as exc_info:
        await bearer(request)
    assert exc_info.value.status_code == 403