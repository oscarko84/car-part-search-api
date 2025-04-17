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

        print(f"data: {data}")
        # 스킬 서버 요청 형식 처리
        # 요청에서 query 추출
        if "action" in data and "params" in data["action"] and "query" in data["action"]["params"]:
            query = data["action"]["params"]["query"].strip()
        else:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'query' in 'userRequest.utterance' or 'action.params.query'."
            }), 400

        print(f"query: {query}")

        result = search_engine.match(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
