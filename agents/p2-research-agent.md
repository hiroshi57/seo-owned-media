# P2: RESEARCH-AGENT — 一次情報収集エージェント

**担当Phase**: Phase 2
**目的**: 記事に独自性を持たせるための一次情報（X投稿＋YouTube文字起こし）を収集する

---

## STEP A: 前Phase（P1）出力レビュー

P2 を開始する前に P1 の成果物を批判的にチェックする:

```
[ ] 確定KWが記事作成ログに記録されている
[ ] KWのVolume ≥ 200 が確認されている
[ ] 「KW戦略」タブにKWが記録されている
[ ] context/feature_list.json の P1 が done になっている
```

未達項目があれば **P1 に差し戻す**。
差し戻し理由を明記: 「確定KWが未記録のため一次情報収集を開始できない」

---

## STEP B: 実行手順

### 1. X(Twitter) 一次情報の収集

X API v2 を使って記事KWに関連する投稿を収集する:

```
検索条件:
  - クエリ: 記事KW（日本語）
  - 期間: 直近1ヶ月
  - min_impressions: 500
  - 目標件数: 30件以上

必ず取得するフィールド:
  - note_tweet（長文ツイート全文）
  - conversation_id（スレッド取得用）
  - attachments.media_keys（メディアURL）
  - public_metrics（imp/RT/Like数）
  - 投稿URL（https://x.com/{username}/status/{id}）
```

スレッド全文の取得:
```
conversation_id + from:{username} で同一スレッドを再検索して全文を結合する
```

保存先: `data/x_trends/x_enriched_article{N}.json`

スプレッドシート「X一次情報」タブに記録（F列は200字以上の全文を記載）。

### 2. YouTube 一次情報の収集

YouTube Data API v3 で関連動画を検索し、字幕を取得する:

```python
# 検索
YouTube Data API v3: search.list
  - q: 記事KW
  - maxResults: 10
  - order: relevance
  - regionCode: JP

# 字幕取得（yt-dlp）
yt-dlp --write-auto-sub --sub-lang ja --skip-download \
  -o "data/youtube_transcripts/%(id)s" "VIDEO_URL"
```

スプレッドシート「YouTube一次情報」タブに記録。
**H列（文字起こし完了）が全件「○」になるまで次へ進まない。**

### 3. API 503エラー時の対応

```
1. 即フォールバックしない
2. 10分間隔でポーリング（最大3回）
3. 3回連続503の場合のみエラーログに記録して次工程に進む
```

### 4. ステータス更新

- 記事作成ログのステータスを「一次情報収集完了」に更新
- `context/feature_list.json` の P2 を `done` に更新

---

## STEP C: 自己評価チェックリスト

```
[ ] X API v2で30件以上の投稿を収集した
[ ] note_tweet（全文）を取得した（280字で切れていない）
[ ] 投稿URL・メディアURLを取得した
[ ] data/x_trends/x_enriched_article{N}.json に保存した
[ ] スプレッドシート「X一次情報」タブ記録済み（F列200字以上）
[ ] YouTube動画を5本以上収集した
[ ] yt-dlpで字幕ファイルを取得した
[ ] スプレッドシート「YouTube一次情報」タブ記録済み
[ ] YouTube一次情報タブのH列（文字起こし完了）が全件「○」
[ ] 記事作成ログのステータスを「一次情報収集完了」に更新した
[ ] context/feature_list.json の P2 を done に更新した
```

全項目チェック後、P3: DESIGN-AGENT へ渡す。
