# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# CSV 데이터 로딩
class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {file_path}")
        return pd.read_csv(file_path, encoding="utf-8")

    def match(self, user_query):
        search_columns = ["제조사", "시리즈", "모델", "바디연식", "부품명"]
        keywords = user_query.strip().split()

        mask = pd.Series([True] * len(self.df))
        for keyword in keywords:
            keyword_match = pd.Series([False] * len(self.df))
            for col in search_columns:
                keyword_match |= self.df[col].astype(str).str.contains(keyword, case=False, na=False)
            mask &= keyword_match

        matched = self.df[mask]

        if matched.empty:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [{
                        "simpleText": {
                            "text": f'"{user_query}"에 대한 검색 결과가 없습니다.'
                        }
                    }]
                }
            }

        top = matched.iloc[0]
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "basicCard": {
                        "title": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.",
                        "description": top['URL'],
                        "buttons": [{
                            "label": "링크 열기",
                            "action": "webLink",
                            "webLinkUrl": top['URL']
                        }]
                    }
                }]
            }
        }

search_engine = SearchEngine()

@app.route("/")
def home():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        if "action" in data and "params" in data["action"] and "query" in data["action"]["params"]:
            query = data["action"]["params"]["query"].strip()
        else:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'query' in action.params."
            }), 400
        result = search_engine.match(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
