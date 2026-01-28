import pytest
from app import create_app
from app.db import db

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client:
        yield client

