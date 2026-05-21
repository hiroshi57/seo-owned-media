# P7: ANALYTICS-AGENT — 分析・学習エージェント

**担当Phase**: Phase 7
**目的**: インデックス登録・スプレッドシート更新・内部リンク追加・KPIレポート・自己学習

---

## STEP A: 前Phase（P6）出力レビュー

P7 を開始する前に P6 の成果物を批判的にチェックする:

```
[ ] WordPress 公開URL が存在する
[ ] 記事作成ログのステータスが「公開済み」になっている
[ ] WP Post ID が記録されている
[ ] 品質スコアが記録されている
[ ] context/feature_list.json の P6 が done になっている
```

公開URLがない場合は **P6 に差し戻す**。
差し戻し理由: 「公開URLが取得できていない。WordPress公開が完了しているか確認してください」

---

## STEP B: 実行手順

### 1. Google Indexing API でインデックス登録

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'indexing-service-account.json',
    scopes=['https://www.googleapis.com/auth/indexing']
)
service = build('indexing', 'v3', credentials=credentials)
service.urlNotifications().publish(
    body={'url': '公開URL', 'type': 'URL_UPDATED'}
).execute()
```

Indexing API 未設定の場合: ユーザーに GSC の URL検査ツールで手動登録を依頼。

### 2. スプレッドシート全タブ更新

| タブ | 更新内容 |
|:----|:--------|
| ダッシュボード | 最終更新日・総公開記事数・今月公開数 |
| 記事作成ログ | ステータス「公開済み」・URL・品質スコアを記録 |
| KW戦略 | 該当KWのStatusを「公開済」に更新 |
| トピッククラスター | StatusとURLを更新 |
| KPIレポート | 新行追加（日付・総記事数・本日公開数・インデックス率） |

### 3. 既存記事への内部リンク自動追加

```
1. 公開済み全記事のH2見出しとKWを取得
2. 新規記事のKWが既存記事の本文に自然に挿入できる箇所を特定
3. WordPress REST API で既存記事を更新して内部リンクを追加（3本以上）
4. 「内部リンク管理」タブに記録
```

### 4. kpi_feedback.md の更新（自己学習ループ）

```markdown
## 成功パターン（追記ルール）
以下に該当する場合は追記する:
  - 公開7日以内にGSCで表示回数が発生した記事 → KW特性と構造を記録
  - 品質スコア97点以上の記事 → 文字数・一次情報数・Schema種類を記録
  - クラスター完成後に全体順位が上昇したケース → クラスター効果を記録

## 失敗パターン（追記ルール）
以下に該当する場合は追記する:
  - Vol=200以下のKWで記事を作成したケース
  - インデックスされていない記事の共通点
  - カニバリが発生したKWと対処法
```

### 5. context/MEMORY.md の更新

今回のセッションで気づいた改善点を追記する（2,000文字上限）:

```
追記フォーマット:
  [日付] [気づき or ミス] → [次回への対策]
```

### 6. context/claude-progress.md の更新

```
## [日付] セッション記録
- 完了した作業: Phase 1〜7（記事タイトル・KW）
- 品質スコア: XX点
- 公開URL: https://...
- 次のセッションで着手すること: 次記事のKW選定
- 注意事項: （あれば）
```

### 7. context/feature_list.json のリセット

次の記事に向けて全Phaseを `pending` に戻す:

```json
{
  "pipeline_phases": [
    {"id": "P1", "status": "pending", "evidence": "", "article_id": null},
    ...
  ]
}
```

`articles` 配列に今回の記事情報を追記してから各Phaseをリセットすること。

---

## STEP C: 自己評価チェックリスト（AI育成チェック含む）

```
[ ] Google Indexing API にリクエストを送信した（または手動登録を依頼した）
[ ] スプレッドシート「ダッシュボード」タブを更新した
[ ] スプレッドシート「記事作成ログ」のURL・品質スコアを記録した
[ ] スプレッドシート「KW戦略」のStatusを「公開済」に更新した
[ ] スプレッドシート「トピッククラスター」のStatusとURLを更新した
[ ] スプレッドシート「KPIレポート」に新行を追加した
[ ] 既存記事への内部リンクを3本以上追加した
[ ] 「内部リンク管理」タブに記録した
[ ] kpi_feedback.md の成功/失敗パターンを更新した（自己学習）
[ ] context/MEMORY.md に今回の学びを追記した（2,000字上限）
[ ] context/claude-progress.md にセッション記録を追記した
[ ] context/feature_list.json の articles 配列に今回の記事を追記した
[ ] context/feature_list.json の全Phaseを pending にリセットした
```

全項目チェックで1サイクル完了。Orchestrator に完了を報告する。
