from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import time

app = Flask(__name__)
CORS(app)

# CSV 파일 불러오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "parts.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")

df = pd.read_csv(CSV_PATH, encoding="utf-8")

@app.route("/")
def index():
    return "✅ Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        start_time = time.time()
        data = request.get_json()

        print(f"[DEBUG] 요청 데이터: {data}")

        # query 추출
        query = data.get("action", {}).get("params", {}).get("query", "").strip()
        if not query:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{
                        "simpleText": {
                            "text": "쿼리가 비어있습니다. 다시 입력해주세요."
                        }
                    }]
                }
            })

        print(f"[DEBUG] 검색어: {query}")
        keywords = query.split()
        search_columns = ["제조사", "시리즈", "모델", "바디연식", "부품명"]

        # 조건 생성: 모든 키워드가 포함된 행 필터링
        mask = pd.Series([True] * len(df))
        for keyword in keywords:
            keyword_match = pd.Series([False] * len(df))
            for col in search_columns:
                keyword_match |= df[col].astype(str).str.contains(keyword, case=False, na=False)
            mask &= keyword_match

        matched = df[mask]

        if matched.empty:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{
                        "simpleText": {
                            "text": f'"{query}"에 대한 검색 결과가 없습니다.'
                        }
                    }]
                }
            })

        top = matched.iloc[0]

        print(f"[DEBUG] 응답 시간: {time.time() - start_time:.2f}초")
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "basicCard": {
                        "title": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.",
                        "description": top['URL'],
                        "buttons": [{
                            "label": "링크 열기",
                            "action": "webLink",
                            "webLinkUrl": top["URL"]
                        }]
                    }
                }]
            }
        })

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
