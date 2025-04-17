from flask import Flask, request, jsonify
from search_engine import SearchEngine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

search_engine = SearchEngine()

@app.route("/")
def index():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        print(f"📥 Received data: {data}")  # 디버깅 로그

        if not data or "action" not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'action' in request payload."
            }), 400

        action = data["action"]
        params = action.get("params", {})

        query = params.get("query", "").strip()

        if not query:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing or empty 'query' parameter."
            }), 400

        result = search_engine.match(query)
        return jsonify(result)

    except Exception as e:
        print(f"❌ Exception: {str(e)}")  # 서버 로그 출력
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
