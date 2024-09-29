from collections.abc import Generator

import fastapi
from fastapi.testclient import TestClient

from sqlmodel import Session, delete
from app.main import app
from app.db import engine, init_db
from models import Watch

import pytest


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Watch)
        session.exec(statement)
        session.commit()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health(client):
    # When I make a GET to the healthz endpoint
    result = client.get("/healthz")

    # Then I expect an HTTP OK
    assert result.status_code == fastapi.status.HTTP_200_OK


def test_metrics(client):
    # When I make a GET to the healthz endpoint
    client.get("/healthz")

    # Then make a request to the metrics endpoint
    result = client.get("/metrics")

    # Then I expect an HTTP OK
    assert result.status_code == fastapi.status.HTTP_200_OK

    # And a metric response
    body = result.text
    assert 'request_latency_seconds_count{method="GET",path="/healthz",status="200"}' in body


def test_get_watches(client, db):
    # Given a bunch of watches in the DB
    w1 = Watch(enabled=True, team="alpacas", backend_type="prometheus", query="up", forecast_frequency_minutes=5)
    w2 = Watch(enabled=True, team="alpacas", backend_type="prometheus", query="up1", forecast_frequency_minutes=5)
    w3 = Watch(enabled=True, team="alpacas", backend_type="prometheus", query="up2", forecast_frequency_minutes=5)
    db.add_all([w1, w2, w3])
    db.commit()

    # When I make a GET request to the watch endpoint
    response = client.get("/forecaster/v1/watch")

    # Then I expect an HTTP OK
    assert response.status_code == fastapi.status.HTTP_200_OK

    # And the watches in the response
    data = response.json()
    assert len(data) == 3


def test_get_watch(client, db):
    # Given a watch in the DB
    watch = Watch(enabled=True, team="alpacas", backend_type="prometheus", query="up", forecast_frequency_minutes=5)
    db.add(watch)
    db.commit()

    # When I make a GET request to the watch endpoint
    response = client.get(f"/forecaster/v1/watch/{watch.id}")

    # Then I expect an HTTP OK
    assert response.status_code == fastapi.status.HTTP_200_OK

    # And the watch in the response
    data = response.json()
    assert data["id"] == watch.id
    assert data["query"] == watch.query


def test_post_watch(client, db):
    # When I make a POST request to the watch endpoint
    post_data = {"enabled": True, "team": "alpacas", "backend_type": "prometheus", "query": "test_foo", "forecast_frequency_minutes": 5}
    response = client.post("/forecaster/v1/watch", json=post_data)

    # Then I expect an HTTP OK
    assert response.status_code == fastapi.status.HTTP_201_CREATED

    # And a metric response
    data = response.json()
    assert data["query"] == "test_foo"


def test_put_watch(client, db):
    # Given a watch in the DB
    watch = Watch(enabled=True, team="alpacas", backend_type="prometheus", query="up", forecast_frequency_minutes=5)
    db.add(watch)
    db.commit()

    # When I make a POST request to the watch endpoint
    put_data = {"enabled": False}
    response = client.put(f"/forecaster/v1/watch/{watch.id}", json=put_data)

    # Then I expect an HTTP OK
    assert response.status_code == fastapi.status.HTTP_200_OK
    # And a metric response
    data = response.json()
    assert data["enabled"] == False
