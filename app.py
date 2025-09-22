from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/testdb")
mongo = PyMongo(app)

# Rota para cadastrar livro
@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.json
    if not dados or "titulo" not in dados or "autor" not in dados or "genero" not in dados or "anoPublicacao" not in dados:
        return jsonify({"erro": "Campos obrigatórios: titulo, autor, genero, anoPublicacao"}), 400

    livro_id = mongo.db.livros.insert_one({
        "titulo": dados["titulo"],
        "autor": dados["autor"],
        "genero": dados["genero"],
        "anoPublicacao": dados["anoPublicacao"],
        "dataCadastro": datetime.now()
    }).inserted_id

    return jsonify({"id": str(livro_id)}), 201

# Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    livros = []
    for l in mongo.db.livros.find():
        livros.append({
            "id": str(l["_id"]),
            "titulo": l["titulo"],
            "autor": l["autor"],
            "genero": l["genero"],
            "anoPublicacao": l["anoPublicacao"],
            "dataCadastro": l["dataCadastro"]
        })
    return jsonify(livros), 200

# Rota para excluir livro
@app.route("/livros/<id>", methods=["DELETE"])
def excluir_livro(id):
    result = mongo.db.livros.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"erro": "Livro não encontrado"}), 404
    return jsonify({"msg": "Livro excluído com sucesso"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

