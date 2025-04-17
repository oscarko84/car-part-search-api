import pandas as pd
import glob
import re

class SearchEngine:
    def __init__(self, data_folder="./"):
        files = glob.glob(f"{data_folder}/*.csv")
        df_list = [pd.read_csv(file) for file in files]
        self.df = pd.concat(df_list, ignore_index=True)

    def match(self, query):
        # 품번 검색
        if re.fullmatch(r"\d{6,}", query):
            return {
                "type": "품번",
                "message": f"{query}에 대한 검색 링크입니다.",
                "url": f"https://parts119.com/goods/goods_search.php?keyword={query}&recentCount=10"
            }

        # 키워드 매칭 (모델명 + 부품명)
        keywords = query.strip().lower().split()
        match = self.df[
            self.df.apply(lambda row:
                all(any(k in str(v).lower() for v in row.values) for k in keywords),
                axis=1
            )
        ]
        if not match.empty:
            top = match.iloc[0]
            return {
                "type": "키워드",
                "message": f"{top['제조사']} {top['모델']}의 {top['부품명']} 링크입니다.",
                "url": top['URL']
            }

        return {
            "type": "없음",
            "message": "검색 결과를 찾을 수 없습니다.",
            "url": "https://parts119.com"
        }
