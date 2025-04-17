import pandas as pd

class SearchEngine:
    def __init__(self):
        try:
            self.df = pd.read_csv("data/parts.csv")
            self.df.fillna("", inplace=True)
            print(f"[INFO] CSV 로딩 완료 - {len(self.df)} rows")
        except Exception as e:
            print(f"[ERROR] CSV 로딩 실패: {e}")
            self.df = pd.DataFrame()

    def match(self, query: str):
        if self.df.empty:
            return self._response_text("데이터가 로딩되지 않았습니다.")

        matched = self.df[self.df.apply(lambda row: query.lower() in " ".join(map(str, row)).lower(), axis=1)]

        if matched.empty:
            return self._response_text(f'"{query}"에 대한 검색 결과가 없습니다.')

        title = matched.iloc[0].get("title", "부품 정보")
        url = matched.iloc[0].get("url", "https://parts119.com")

        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": title,
                            "description": url,
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "링크 열기",
                                    "webLinkUrl": url
                                }
                            ]
                        }
                    }
                ]
            }
        }

    def _response_text(self, message: str):
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ]
            }
        }
