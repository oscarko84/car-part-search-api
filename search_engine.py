import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        # 현재 파일 위치 기준으로 압축된 CSV 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv.gz")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {file_path}")

        # gzip 압축된 CSV 읽기
        df = pd.read_csv(file_path, compression='gzip', encoding="utf-8")
        return df

    def match(self, user_query):
        search_columns = ["제조사", "시리즈", "모델", "바디연식", "부품명"]

        # 공백 기준 키워드 분리
        keywords = user_query.strip().split()

        # 각 키워드가 최소한 하나의 컬럼에 존재해야 함
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
                        "basicCard": {
                            "title": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.",
                            "description": top["URL"],
                            "buttons": [
                                {
                                    "label": "링크 열기",
                                    "action": "webLink",
                                    "webLinkUrl": top["URL"]
                                }
                            ]
                        }
                    }
                ]
            }
        }
