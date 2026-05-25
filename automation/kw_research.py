"""
Phase 1: KW選定エージェント
Pytrends（Google Trends）でAI関連キーワードを調査する
"""
import time
import json
from pytrends.request import TrendReq

pytrends = TrendReq(hl='ja-JP', tz=540)

# 中小企業経営者向け AI関連キーワード候補
seed_keywords = [
    "AI 業務効率化",
    "ChatGPT 使い方 ビジネス",
    "AI ツール 比較",
    "業務自動化 AI",
    "生成AI 活用",
]

results = []

print("=== Phase 1: KWリサーチ開始 ===\n")

for kw in seed_keywords:
    try:
        pytrends.build_payload([kw], cat=0, timeframe='today 12-m', geo='JP')
        interest = pytrends.interest_over_time()
        if not interest.empty:
            avg_score = int(interest[kw].mean())
            peak_score = int(interest[kw].max())
            related = pytrends.related_queries()
            top_related = []
            if related[kw]['top'] is not None:
                top_df = related[kw]['top'].head(5)
                top_related = top_df['query'].tolist()
            results.append({
                "keyword": kw,
                "trend_avg": avg_score,
                "trend_peak": peak_score,
                "related_queries": top_related
            })
            print(f"[OK] {kw}")
            print(f"     平均トレンド: {avg_score} / ピーク: {peak_score}")
            print(f"     関連KW: {', '.join(top_related[:3])}")
            print()
        time.sleep(2)
    except Exception as e:
        print(f"[SKIP] {kw}: {e}\n")
        time.sleep(5)

# 結果をJSONに保存
import os
os.makedirs("data", exist_ok=True)
with open("data/kw_research_result.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("=== 結果を data/kw_research_result.json に保存しました ===")
print(f"\nトレンドスコア上位（高いほど注目度が高い）:")
sorted_results = sorted(results, key=lambda x: x['trend_avg'], reverse=True)
for r in sorted_results:
    print(f"  {r['trend_avg']:3d}点 | {r['keyword']}")
