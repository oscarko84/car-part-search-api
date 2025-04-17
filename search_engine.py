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

        df = pd.read_csv(file_path, encoding="utf-8")
        return df

    def match(self, user_query):
        # 검색 대상 컬럼
        search_columns = ["제조사", "시리즈", "모델", "바디연식", "부품명"]

        # 입력 키워드를 공백 기준으로 나누기
        keywords = user_query.strip().split()

        # 키워드가 모두 하나의 행 안의 컬럼 중 어디엔가 포함되어야 한다
        def row_matches(row):
            return all(
                any(keyword.lower() in str(row[col]).lower() for col in search_columns)
                for keyword in keywords
            )

        # 필터링
        matched = self.df[self.df.apply(row_matches, axis=1)]

        # 결과 없음 처리
        if matched.empty:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": f'"{user_query}"에 대한 검색 결과가 없습니다.',
                            }
                        }
                    ]
                }
            }

        # 결과 응답
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
