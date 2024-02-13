import pytest 
from pytest import fixture
from fastapi.testclient import TestClient
from antisocial_backend.app.main import app
from antisocial_backend.dependencies.dependencies import get_session
from sqlmodel import Session,SQLModel,create_engine, StaticPool
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},poolclass= StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        
@pytest.fixture(name="client")
def client_fixture(session:Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()