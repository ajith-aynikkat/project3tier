from flask import Flask, jsonify, request
from pymongo import MongoClient
import os


app = Flask(__name__)


MONGO_HOST = os.environ.get("MONGO_HOST", "mongo")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "appdb")


client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
items = db["items"]


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/items")
def get_items():
    data = list(items.find({}, {"_id": 0}))
    return jsonify(data)


@app.post("/items")
def add_item():
    req = request.get_json()
    name = req.get("name")
    if not name:
        return {"error": "name required"}, 400
    item = {"name": name}
    items.insert_one(item)
    return item, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
