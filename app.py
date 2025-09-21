from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from flask_pymongo import PyMongo

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/testdb")
mongo = PyMongo(app)

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"msg": "Hello, World!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)