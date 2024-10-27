from unittest.mock import AsyncMock, patch

import pytest

from src.domain.schemas.user import UserUpdate
from src.services.user import UserService
from src.tests.mocks import MockUserRepository


@pytest.fixture
def mock_repo():
    mock_repo = MockUserRepository()
    return mock_repo


@pytest.fixture
def user_service(mock_repo):
    with patch("src.services.user.UserRepository", return_value=mock_repo):
        yield UserService(AsyncMock())


@pytest.mark.asyncio
async def test_get_user(user_service, mock_repo):
    user_id = "1"
    mock_user_data = {"username": "bob", "id": "1", 'info': None, 'image_url': None}
    result = await user_service.get_user(user_id=user_id)
    assert result == mock_user_data



@pytest.mark.asyncio
async def test_update_user(user_service, mock_repo):
    user_id = "1"
    data = UserUpdate(username="tot")
    mock_user_data = {'username': 'tot', 'id': '1', 'info': None, 'image_url': None}
    result = await user_service.update_user(user_id=user_id, data=data)
    assert result == mock_user_data
