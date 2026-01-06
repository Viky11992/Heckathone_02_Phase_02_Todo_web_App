import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app  # Adjust import based on your app structure
from app.database import get_session
from app.models import Task


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    response = client.post(
        "/api/user-123/tasks",
        json={"title": "Test task", "description": "Test description"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["title"] == "Test task"
    assert data["data"]["description"] == "Test description"
    assert data["data"]["completed"] is False


def test_read_tasks(client: TestClient, session: Session):
    # Create a task first
    task = Task(
        user_id="user-123",
        title="Test task",
        description="Test description",
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.get("/api/user-123/tasks")
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) > 0