from flask import Flask, request, jsonify
from search_engine import SearchEngine

app = Flask(__name__)
search_engine = SearchEngine()

@app.route("/")
def index():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'query' field in request body."
            }), 400

        query = data["query"].strip()
        result = search_engine.match(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
