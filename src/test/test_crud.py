from fastapi.testclient import TestClient
from pytest import fixture
from main import app
from app.routers import *
from app.database import SessionLocal
from app.models import Document


@fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_status(client):
    response = client.get("http://0.0.0.0:8000/healthcheck/")

    assert response.status_code == 200
    assert response.json() == {"status": True}


def test_upload(client):
    url = "http://0.0.0.0:8000/upload/"
    with open("/app/test/image.png", "rb") as file:
        response = client.post(
            url,
            files={"data": file, "type": "image/png"},
        )

    assert response.status_code == 200
    assert response.json() == "/app/Documents/image.png"


def test_analys(client):
    url = "http://0.0.0.0:8000/analys/?id="
    db = SessionLocal()
    record = db.query(Document).order_by(Document.id.desc()).first()
    url += str(record.id)

    response = client.put(url)
    response_json = response.json()
    response_text = response_json["text"]

    assert response.status_code == 200
    assert response_text == "PURE\nTEXT\n"


def test_extract(client):
    url = "http://0.0.0.0:8000/extract/?id="
    db = SessionLocal()
    record = db.query(Document).order_by(Document.id.desc()).first()
    url += str(record.id)

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == "PURE\nTEXT\n"


def test_delete(client):
    url = "http://0.0.0.0:8000/delete/?id="
    db = SessionLocal()
    record = db.query(Document).order_by(Document.id.desc()).first()
    url += str(record.id)

    response = client.delete(url)

    assert response.status_code == 200
    assert response.json() == 0
