import pytest
import mongomock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, mongo


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Mocka o MongoDB em memória com mongomock
    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["livros_testdb"]

    client = app.test_client()
    yield client
    mongo.db.livros.delete_many({})  # limpa após cada teste


# ----------------- TESTES FELIZES ----------------- #
def test_cadastrar_livro(client):
    res = client.post(
        "/livros",
        json={
            "titulo": "Livro Teste",
            "autor": "Autor X",
            "genero": "Ficção",
            "anoPublicacao": 2020
        }
    )
    assert res.status_code == 201
    assert "id" in res.json


def test_listar_livros(client):
    client.post(
        "/livros",
        json={
            "titulo": "Livro 1",
            "autor": "Autor Y",
            "genero": "História",
            "anoPublicacao": 1999
        }
    )
    res = client.get("/livros")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) > 0


def test_excluir_livro(client):
    res = client.post(
        "/livros",
        json={
            "titulo": "Livro Deletar",
            "autor": "Autor Z",
            "genero": "Técnico",
            "anoPublicacao": 2010
        }
    )
    livro_id = res.json["id"]

    delete_res = client.delete(f"/livros/{livro_id}")
    assert delete_res.status_code == 200
    assert delete_res.json["msg"] == "Livro excluído com sucesso"


# ----------------- TESTES DE ERRO ----------------- #
def test_cadastrar_livro_campos_faltando(client):
    res = client.post("/livros", json={"titulo": "Só título"})
    assert res.status_code == 400
    assert "erro" in res.json


def test_excluir_livro_inexistente(client):
    res = client.delete("/livros/000000000000000000000000")
    assert res.status_code in (400, 404)
