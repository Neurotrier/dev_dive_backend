from unittest.mock import AsyncMock, patch

import pytest

from src.core.role import Role
from src.domain.schemas.user import UserPoliciesUpdate, UserUpdate
from src.services.user import UserService
from src.tests.mocks import MockUserRepository
from src.tests.mocks.MockUsers import mock_users


@pytest.fixture
def mock_repo():
    mock_repo = MockUserRepository(mock_users)
    return mock_repo


@pytest.fixture
def user_service(mock_repo):
    with patch("src.services.user.UserRepository", return_value=mock_repo):
        yield UserService(AsyncMock())


@pytest.mark.asyncio
async def test_get_user(user_service, mock_repo):
    user_id = "1"
    result = await user_service.get_user(user_id=user_id)

    mock_user_data = {
        "username": "bob",
        "id": "1",
        "info": None,
        "image_url": None,
        "is_banned": False,
        "role": Role.MODERATOR,
        "reputation": 100,
    }
    assert result == mock_user_data


@pytest.mark.asyncio
async def test_update_user(user_service, mock_repo):
    user_id = "1"
    data = UserUpdate(username="bobr", info="Hello")
    result = await user_service.update_user(user_id=user_id, data=data)

    mock_user_data = {
        "username": "bobr",
        "id": "1",
        "info": "Hello",
        "image_url": None,
        "is_banned": False,
        "role": Role.MODERATOR,
        "reputation": 100,
    }
    assert result == mock_user_data


@pytest.mark.asyncio
async def test_update_user_policies(user_service, mock_repo):
    user_id = "1"
    data = UserPoliciesUpdate(is_banned=True, role=Role.USER)
    result = await user_service.update_user_policies(user_id=user_id, data=data)

    mock_user_data = {
        "username": "bobr",
        "id": "1",
        "info": "Hello",
        "image_url": None,
        "is_banned": True,
        "role": Role.USER,
        "reputation": 100,
    }
    assert result == mock_user_data


@pytest.mark.asyncio
async def test_delete_user(user_service, mock_repo):
    user_id = "2"
    result = await user_service.delete_user(user_id=user_id)

    mock_user_data = "2"
    assert result == mock_user_data
