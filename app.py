from flask import Flask, request, jsonify
from flask_cors import CORS
from search_engine import SearchEngine

app = Flask(__name__)
CORS(app)

search_engine = SearchEngine()

@app.route("/", methods=["GET"])
def home():
    return "✅ Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json(force=True)

        query = data.get("action", {}).get("params", {}).get("query", "").strip()
        if not query:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        result = search_engine.match(query)
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
