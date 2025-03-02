import pytest
from bookstore.main import pwd_context, create_user_signup, login_for_access_token
from unittest.mock import patch
from bookstore.database import UserCredentials
from sqlalchemy.orm import Session
from fastapi import HTTPException

def test_password_hashing():
    password = "testpassword"
    hashed_password = pwd_context.hash(password)
    assert pwd_context.verify(password, hashed_password)

@pytest.mark.asyncio
async def test_create_user_signup_success(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    user_credentials = UserCredentials(email="test@example.com", password="password123")
    result = await create_user_signup(user_credentials, mock_db)
    assert result == {"message": "User created successfully"}
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_signup_duplicate(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = UserCredentials(email="test@example.com", password="password123")
    user_credentials = UserCredentials(email="test@example.com", password="password123")
    with pytest.raises(HTTPException) as exc_info:
        await create_user_signup(user_credentials, mock_db)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_login_for_access_token_success(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_user = UserCredentials(email="test@example.com", password=pwd_context.hash("password123"))
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    user_credentials = UserCredentials(email="test@example.com", password="password123")
    result = await login_for_access_token(user_credentials, mock_db)
    assert "access_token" in result
    assert "token_type" in result

@pytest.mark.asyncio
async def test_login_for_access_token_failure(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    user_credentials = UserCredentials(email="test@example.com", password="password123")
    with pytest.raises(HTTPException) as exc_info:
        await login_for_access_token(user_credentials, mock_db)
    assert exc_info.value.status_code == 400