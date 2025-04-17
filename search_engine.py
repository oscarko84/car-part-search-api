import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        # 현재 파일 경로 기준으로 CSV 파일 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "data", "parts.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"[ERROR] CSV 파일이 존재하지 않습니다: {csv_path}")

        try:
            df = pd.read_csv(csv_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")

        # 필수 컬럼 존재 여부 검사
        required_columns = {"부품명", "제조사", "모델", "URL"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"[ERROR] CSV에 필수 컬럼이 없습니다: {required_columns}")

        return df

    def match(self, user_query):
        if not user_query or not isinstance(user_query, str):
            return {"type": "error", "message": "유효하지 않은 검색어입니다."}

        # 대소문자 무시, 결측치 제거
        results = self.df[self.df["부품명"].str.contains(user_query, case=False, na=False)]

        if results.empty:
            return {"type": "miss", "message": f"'{user_query}'에 대한 검색 결과가 없습니다."}

        top = results.iloc[0]
        return {
            "type": "match",
            "message": f"{top['제조사']} {top['모델']}의 '{top['부품명']}' 검색 결과입니다.",
            "url": top["URL"]
        }
