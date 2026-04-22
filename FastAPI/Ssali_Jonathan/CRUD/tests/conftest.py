from FastAPI.Ssali_Jonathan.CRUD.books.book_schema import Book
from FastAPI.Ssali_Jonathan.CRUD.core.database import get_session
from FastAPI.Ssali_Jonathan.CRUD.api.main import app
from FastAPI.Ssali_Jonathan.CRUD.utils.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker

from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import uuid


mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()

def get_mock_session():
    yield mock_session


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])


app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer] = Mock()



@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_book_service():
    return mock_book_service


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def test_book():
    now = datetime.now()

    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="sample title",
        author="Test Author",
        publisher="Test Publisher",
        page_count=200,
        language="English",
        published_date=now.isoformat(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )