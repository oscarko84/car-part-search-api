from flask import Flask, request, jsonify
from search_engine import SearchEngine
import os

app = Flask(__name__)
search_engine = SearchEngine()

@app.route("/", methods=["GET"])
def index():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        # 요청에서 JSON 추출
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' in request"}), 400

        query = data["query"]
        result = search_engine.match(query)

        return jsonify(result), 200

    except Exception as e:
        # 예외 발생 시 에러 메시지 출력
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
