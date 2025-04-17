import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        # 현재 파일 위치 기준으로 CSV 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {file_path}")

        # CSV 읽기
        df = pd.read_csv(file_path, encoding="utf-8")
        return df

    def match(self, user_query):
        search_columns = ["제조사", "시리즈", "모델", "바디연식", "부품명"]

        condition = False
        for col in search_columns:
            condition |= self.df[col].astype(str).str.contains(user_query, case=False, na=False)

        matched = self.df[condition]

        if matched.empty:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": f'"{user_query}"에 대한 검색 결과가 없습니다.'
                            }
                        }
                    ]
                }
            }

        top = matched.iloc[0]
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다."
                        }
                    },
                    {
                        "basicCard": {
                            "title": f"{top['부품명']}",
                            "description": f"{top['제조사']} {top['모델']}",
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "상세보기",
                                    "webLinkUrl": top["URL"]
                                }
                            ]
                        }
                    }
                ]
            }
        }
