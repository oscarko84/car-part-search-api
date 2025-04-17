import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        # 압축된 csv.gz 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv.gz")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {file_path}")

        return pd.read_csv(file_path, encoding="utf-8", compression='gzip')

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
                            "description": top['URL'],
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
