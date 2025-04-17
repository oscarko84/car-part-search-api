import pandas as pd

class SearchEngine:
    def __init__(self):
        try:
            self.df = pd.read_csv("data/parts.csv")
            print(f"[INFO] CSV Loaded - {len(self.df)} rows")
        except Exception as e:
            print("[ERROR] Failed to load CSV:", e)
            self.df = pd.DataFrame()

    def match(self, user_query):
        if self.df.empty:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "데이터를 불러오지 못했습니다."
                            }
                        }
                    ]
                }
            }

        search_columns = ["제조사", "시리즈", "모델", "연식", "부품명"]

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
                            "text": f"{top['제조사']} {top['모델']}의 [{top['부품명']}] 링크입니다."
                        }
                    },
                    {
                        "basicCard": {
                            "title": top["부품명"],
                            "description": f"{top['제조사']} / {top['모델']}",
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "링크 열기",
                                    "webLinkUrl": top["URL"]
                                }
                            ]
                        }
                    }
                ]
            }
        }
