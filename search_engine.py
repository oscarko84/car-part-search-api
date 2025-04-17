import pandas as pd
import os

class SearchEngine:
    def __init__(self):
        try:
            data_path = os.path.join(os.path.dirname(__file__), "data", "parts.csv")
            self.df = pd.read_csv(data_path)
            print(f"[INFO] CSV 로딩 완료 - {len(self.df)} rows")
        except Exception as e:
            print(f"[ERROR] CSV 로딩 실패: {e}")
            raise

    def match(self, user_query):
        try:
            search_columns = ["제조사", "시리즈", "모델", "부품명", "상품명"]
            condition = False
            for col in search_columns:
                if col in self.df.columns:
                    condition |= self.df[col].astype(str).str.contains(user_query, case=False, na=False)

            matched = self.df[condition]

            if matched.empty:
                return {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": f"'{user_query}'에 대한 검색 결과가 없습니다."
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
                                "title": top["부품명"],
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
        except Exception as e:
            print(f"[ERROR] match() 함수 처리 중 오류: {e}")
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": f"[서버 오류] 검색 처리 중 문제가 발생했습니다: {str(e)}"
                            }
                        }
                    ]
                }
            }
