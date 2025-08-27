# from flask import Flask, request, jsonify
# from search_engine import SearchEngine
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# search_engine = SearchEngine()

# @app.route("/")
# def index():
#     return "Car Part Search API is running."

# @app.route("/search", methods=["POST"])
# def search():
#     try:
#         data = request.get_json()

#         print(f"data: {data}")
#         # 스킬 서버 요청 형식 처리
#         # 요청에서 query 추출
#         if "action" in data and "params" in data["action"] and "query" in data["action"]["params"]:
#             query = data["action"]["params"]["query"].strip()
#         else:
#             return jsonify({
#                 "error": "Bad Request",
#                 "message": "Missing 'query' in 'userRequest.utterance' or 'action.params.query'."
#             }), 400
        
#         print(f"query: {query}")

#         result = search_engine.match(query)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({
#             "error": "Server error",
#             "message": str(e)
#         }), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import urllib.parse

app = Flask(__name__)
CORS(app)

VIN_REGEX = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$', re.IGNORECASE)

def extract_vin(data):
    """
    가능한 모든 경로에서 VIN 후보를 추출:
    - Kakao action.params.vincode
    - Kakao action.params.query (문장 속에서 정규식으로 추출)
    - Kakao userRequest.utterance (정규식)
    - 일반 JSON body의 'vin' 또는 'vincode'
    - 쿼리스트링 ?vin= / ?vincode=
    """
    # 1) Kakao: action.params.vincode
    try:
        params = data.get("action", {}).get("params", {})
        vin = params.get("vincode") or params.get("vin")
        if vin and VIN_REGEX.match(vin.strip()):
            return vin.strip()
        # 2) Kakao: action.params.query
        q = params.get("query")
        if q:
            m = re.search(r'[A-HJ-NPR-Z0-9]{17}', q, re.IGNORECASE)
            if m and VIN_REGEX.match(m.group(0)):
                return m.group(0)
    except Exception:
        pass

    # 3) Kakao: userRequest.utterance
    try:
        utt = (data.get("userRequest", {}).get("utterance") or "").strip()
        if utt:
            m = re.search(r'[A-HJ-NPR-Z0-9]{17}', utt, re.IGNORECASE)
            if m and VIN_REGEX.match(m.group(0)):
                return m.group(0)
    except Exception:
        pass

    # 4) 일반 JSON body
    for key in ("vin", "vincode", "code"):
        v = data.get(key)
        if isinstance(v, str) and VIN_REGEX.match(v.strip()):
            return v.strip()

    # 5) 쿼리스트링
    for key in ("vin", "vincode", "code"):
        v = request.args.get(key)
        if v and VIN_REGEX.match(v.strip()):
            return v.strip()

    return None

def build_parts119_url(vin):
    return f"https://m.parts119.com/goods/goods_search_vin.php?vin={urllib.parse.quote(vin.upper())}&keyword=all"

def is_kakao_request(data):
    # 매우 단순한 판별: Kakao 스킬 공통 필드가 있으면 True
    return "userRequest" in data or "intent" in data or "action" in data

def kakao_ok_response(url, vin):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "VIN 부품 검색 링크",
                        "description": f"VIN: {vin.upper()}",
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "링크 열기",
                                "webLinkUrl": url
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "다시 조회",
                    "action": "message",
                    "messageText": "vin KM8J33A4XRU123456"
                }
            ]
        }
    }

def kakao_error_response(msg):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": msg}}
            ],
            "quickReplies": [
                {
                    "label": "형식 예시",
                    "action": "message",
                    "messageText": "vin KM8J33A4XRU123456"
                }
            ]
        }
    }

@app.route("/")
def index():
    return "Car Part Search API is running."

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json(silent=True) or {}
        vin = extract_vin(data)

        if not vin:
            # VIN이 없거나 형식 오류
            if is_kakao_request(data):
                return jsonify(kakao_error_response("VIN(차대번호) 17자리를 입력해주세요. (I/O/Q 제외)"))
            return jsonify({
                "error": "Bad Request",
                "message": "Valid 17-character VIN not found in request."
            }), 400

        url = build_parts119_url(vin)

        # Kakao 스킬 응답
        if is_kakao_request(data):
            return jsonify(kakao_ok_response(url, vin))

        # 일반 JSON 응답
        return jsonify({
            "vin": vin.upper(),
            "url": url
        })
    except Exception as e:
        if is_kakao_request(request.get_json(silent=True) or {}):
            return jsonify(kakao_error_response("처리 중 오류가 발생했어요. 잠시 후 다시 시도해주세요.")), 500
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

