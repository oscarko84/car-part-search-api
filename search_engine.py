import pandas as pd
import os
from flask import Flask, request, jsonify


class SearchEngine:
    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "parts.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV not found at: {file_path}")

        df = pd.read_csv(file_path, encoding="utf-8")
        return df

    def match(self, user_query):
        # 여러 컬럼에서 검색
        conditions = (
            self.df["제조사"].str.contains(user_query, case=False, na=False) |
            self.df["시리즈"].str.contains(user_query, case=False, na=False) |
            self.df["모델"].str.contains(user_query, case=False, na=False) |
            self.df["바디연식"].str.contains(user_query, case=False, na=False) |
            self.df["부품명"].str.contains(user_query, case=False, na=False)
        )

        matched = self.df[conditions]

        if matched.empty:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "검색 결과가 없습니다."
                            }
                        }
                    ]
                }
            }

        top = matched.iloc[0]
        response_text = f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.{top['URL']}"

        # return {
        #     "version": "2.0",
        #     "template": {
        #         "outputs": [
        #             {
        #                 "simpleText": {
        #                     "text": response_text
        #                 }
        #             }
        #         ]
        #     }
        # }

        data = {"version":"2.0","template":{"outputs":[{"simpleText":{"text":response_text}}]}}

        return jsonify(data)