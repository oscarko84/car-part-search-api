import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        # 현재 파일 위치 기준으로 data/parts.csv 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV not found at: {file_path}")

        df = pd.read_csv(file_path, encoding="utf-8")
        return df

    def match(self, user_query):
        matched = self.df[self.df["부품명"].str.contains(user_query, case=False, na=False)]
        if matched.empty:
            return {"type": "miss", "message": "검색 결과가 없습니다."}

        top = matched.iloc[0]
        return {
            "type": "키워드",
            "message": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.",
            "url": top["URL"]
        }
