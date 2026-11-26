from unittest.mock import patch
import pytest
from ohtu_miniprojekti.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_etusivu_latautuu(client):
    response = client.get("/")
    assert response.status_code == 200

def test_viitteen_lisaaminen_onnistuu(client):
    with patch("ohtu_miniprojekti.app.tallenna_viite") as mock_tallenna:
        response = client.post(
            "/viitteet",
            data={
                "author": "Robert C. Martin",
                "title": "Clean Code",
                "year": "2008",
                "type": "Kirja",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "viite lisätty".encode("utf-8") in response.data
        mock_tallenna.assert_called_once_with(
            "Robert C. Martin", "Clean Code", "2008", "Kirja"
        )

def test_tyhja_kentta_ei_tallenna_viitetta(client):
    with patch("ohtu_miniprojekti.app.tallenna_viite") as mock_tallenna:
        response = client.post(
            "/viitteet",
            data={
                "author": "   ",
                "title": "Clean Code",
                "year": "2008",
                "type": "Kirja",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "Kaikki kentät on täytettävä!".encode("utf-8") in response.data
        mock_tallenna.assert_not_called()

def test_virheellinen_vuosi_ei_tallenna_viitetta(client):
    with patch("ohtu_miniprojekti.app.tallenna_viite") as mock_tallenna:
        response = client.post(
            "/viitteet",
            data={
                "author": "Robert C. Martin",
                "title": "Clean Code",
                "year": "kissa",
                "type": "Kirja",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "Vuosiluvun on oltava numero!".encode("utf-8") in response.data
        mock_tallenna.assert_not_called()