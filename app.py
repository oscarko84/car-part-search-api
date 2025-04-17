import os
from flask import Flask, request, jsonify
from search_engine import SearchEngine

app = Flask(__name__)
search_engine = SearchEngine()

@app.route("/")
def index():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    result = search_engine.match(user_query)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway가 제공하는 포트
    app.run(host="0.0.0.0", port=port)
