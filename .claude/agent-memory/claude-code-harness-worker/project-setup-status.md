---
name: project-setup-status
description: APIセットアップ進捗と次のアクション（2026-05-21時点）
metadata:
  type: project
---

## 現在の状態（2026-05-21）

セットアップ完了・パイプライン未実行の状態。全 Phase は pending。

**Why:** 2026-05-20 に初期ファイル群を生成したが、API キーと WordPress がまだ未設定のためパイプライン実行不可。

**How to apply:** APIセットアップ完了を確認してからパイプライン実行タスクを受け付ける。

---

## APIセットアップ状況

| API | 状態 | 備考 |
|-----|------|------|
| WordPress REST API | ❌ 未設定 | Xserver契約・ドメイン決定が先決 |
| X(Twitter) API v2 Basic | ❌ 未申請 | $100/月・承認に数時間〜数日 |
| YouTube Data API v3 | ❌ 未取得 | Google Cloud Console・即日可 |
| Google Sheets API | ❌ 未設定 | credentials.json 取得要・10タブ作成要 |
| Google Indexing API | ❌ 未設定 | サービスアカウント・GSCオーナー権限要 |
| Ahrefs API | ❌ 未設定 | .mcp.json 作成要 |
| Gemini API | ❌ 未取得 | Google AI Studio・即日可・無料枠あり |
| GA4 | ❌ 未設定 | 任意 |

---

## .env 状態

テンプレートのみ。実際の値は未設定。

---

## 次のアクション優先順

1. WordPress サイト構築（Xserver）
2. Google Cloud プロジェクト作成 → YouTube + Sheets + Indexing API 一括有効化
3. Gemini API 取得
4. X API v2 申請（承認待ち期間があるので早めに）
5. Ahrefs APIキー確認 → .mcp.json 作成
6. .env に全キーを設定 → `bash init.sh` で疎通確認
