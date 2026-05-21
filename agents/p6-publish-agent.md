# P6: PUBLISH-AGENT — 公開エージェント

**担当Phase**: Phase 6
**目的**: アイキャッチ画像と記事内図解を生成し、WordPressに公開する

---

## STEP A: 前Phase（P5）出力レビュー

P6 を開始する前に P5 の成果物を批判的にチェックする:

```
[ ] 品質スコアが95点以上である
[ ] context/feature_list.json の P5 が done になっている
[ ] quality_score フィールドに数値が記録されている
[ ] 記事作成ログのステータスが「品質チェック完了」になっている
```

品質スコアが95点未満の場合は **P5 に差し戻す**。
差し戻し理由: 「品質スコアが95点未満。修正ループを継続してください」

---

## STEP B: 実行手順

### 1. アイキャッチ画像生成

Gemini API または NanoBanana を使って生成する:

```
仕様:
  - アスペクト比: 16:9
  - スタイル: フラットイラスト、カテゴリカラー準拠
  - プロンプトに必ず含める: "No English text whatsoever. Japanese text only or no text at all."

フォールバック順序:
  NanoBanana Pro → NanoBanana Flash → Gemini Flash
```

**生成後に必ず目視確認。英語テキストが混入していたら再生成。**

保存先: `automation/images/eyecatch-article{N}.png`

### 2. H2直下の図解画像生成

```
仕様:
  - 形式: フラットベクターイラスト（テキストなし or 日本語テキストのみ）
  - 生成枚数: 3〜5枚（視覚化が効果的なH2を選ぶ）
  - プロンプトに必ず含める: "No English text whatsoever."

生成後チェック:
  - 英語テキスト混入がないか目視確認
  - 文字化けがないか確認
  - 問題があれば再生成
```

保存先: `automation/images/fig-article{N}-h{M}.png`

### 3. Markdown → HTML 変換

```python
# Python markdown ライブラリを使用
import markdown
html = markdown.markdown(md_text, extensions=['tables', 'extra'])

# Gutenbergブロックの処理
# 変換前に <!-- wp:*** --> ブロックを退避
# 変換後に復元する
```

### 4. WordPress に下書き投稿

`.env` の WP_URL / WP_USER / WP_PASSWORD を使用:

```bash
# 記事投稿
curl -X POST "${WP_URL}/wp-json/wp/v2/posts" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "記事タイトル",
    "content": "HTML本文",
    "status": "draft",
    "categories": [カテゴリID],
    "slug": "url-slug",
    "excerpt": "メタディスクリプション"
  }'
# → wp_post_id を取得して記録する
```

### 5. 画像アップロード

```bash
# アップロード
curl -X POST "${WP_URL}/wp-json/wp/v2/media" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Disposition: attachment; filename=eyecatch.png" \
  --data-binary @automation/images/eyecatch-article{N}.png

# アイキャッチ設定
curl -X POST "${WP_URL}/wp-json/wp/v2/posts/${WP_POST_ID}" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{"featured_media": MEDIA_ID}'
```

### 6. Rank Math SEO設定

```bash
curl -X POST "${WP_URL}/wp-json/rankmath/v1/updateMeta" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{
    "objectID": POST_ID,
    "objectType": "post",
    "meta": {
      "rank_math_title": "SEOタイトル（KW含む・30文字以内）",
      "rank_math_description": "メタディスクリプション（120文字以内）",
      "rank_math_focus_keyword": "フォーカスKW",
      "rank_math_robots": ["index", "follow"]
    }
  }'
```

### 7. FAQ Schema設定

```bash
curl -X POST "${WP_URL}/wp-json/rankmath/v1/updateSchemas" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{
    "objectID": POST_ID,
    "objectType": "post",
    "schemas": {
      "schema-FAQPage-1": {
        "schema-type": "FAQPage",
        "schema-data": {
          "@type": "FAQPage",
          "mainEntity": [
            {"@type": "Question", "name": "Q1", "acceptedAnswer": {"@type": "Answer", "text": "A1"}}
          ]
        }
      }
    }
  }'
```

### 8. 公開（ユーザー確認後）

```bash
# ユーザーが承認した後に実行
curl -X POST "${WP_URL}/wp-json/wp/v2/posts/${WP_POST_ID}" \
  -u "${WP_USER}:${WP_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{"status": "publish"}'
```

**自動実行モード以外では、ユーザーの承認なしに publish を実行しない。**

### 9. ステータス更新

- 記事作成ログのステータスを「公開済み」に更新
- WP Post ID を記録
- 公開URLを記録
- `context/feature_list.json` の P6 を `done`・`wp_post_id` に記録

---

## STEP C: 自己評価チェックリスト

```
[ ] アイキャッチ画像を生成した（英語テキストなし目視確認済み）
[ ] H2直下図解を3〜5枚生成した（英語テキストなし目視確認済み）
[ ] Markdown → HTML 変換が正常に完了した
[ ] WordPress に draft で投稿した（wp_post_id 取得済み）
[ ] アイキャッチ画像をアップロードして featured_media に設定した
[ ] Rank Math でSEOタイトル・メタディスクリプション・フォーカスKWを設定した
[ ] FAQ Schema を5問以上設定した
[ ] ユーザー確認後に status: publish に変更した
[ ] 記事作成ログのステータスを「公開済み」に更新した
[ ] WP Post ID と公開URLを記録した
[ ] context/feature_list.json の P6 を done に更新した
```

全項目チェック後、P7: ANALYTICS-AGENT へ公開URLと WP Post ID を渡す。
