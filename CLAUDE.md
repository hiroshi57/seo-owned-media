# SEOオウンドメディア 全自動パイプライン

## セッション開始時の手順（必ず守ること）

1. このファイルを読む
2. `context/claude-progress.md` を読む（前回の状態を把握）
3. `context/feature_list.json` を読む（Phase進捗を確認）
4. `kpi_feedback.md` を読む（前日の成功/失敗パターンを反映）
5. `PROJECT.md` を読む（メディア設定・ペルソナ確認）

## コマンド対応表

| ユーザーの言葉 | 実行内容 |
|:-------------|:--------|
| 「記事を書いて」「パイプライン実行」 | `SEOオウンドメディア自動化_セットアップ.md` の Phase 1〜7 を順番に実行 |
| 「KPI確認」 | Phase 7 の KPIレポート生成を実行 |
| 「リライト」 | `SEOオウンドメディア自動化_セットアップ.md` セクション8の週次最適化を実行 |
| 「KW選定」 | Phase 1 のみ実行 |
| 「品質チェック」 | Phase 5 の5エージェント採点のみ実行 |

## 作業ルール

- **一度に実行するPhaseは一つのみ**。Phase完了を確認してから次へ進む
- 「完了」と宣言する前に必ず検証コマンドを実行する（品質チェック95点以上）
- Phase完了後は必ず `context/claude-progress.md` と `context/feature_list.json` を更新する
- 詳細な実行手順は `SEOオウンドメディア自動化_セットアップ.md` を読むこと
- エラー発生時はスプレッドシートの「エラーログ」タブに記録する

## 完了の定義（ISC形式）

- [ ] 対象Phaseの全手順が完了している
- [ ] スプレッドシートの記事作成ログが更新されている
- [ ] 品質スコアが95点以上である（Phase 5通過後）
- [ ] `context/claude-progress.md` に今回の作業内容を追記した
- [ ] `context/feature_list.json` のStatusを更新した

## 自己学習ループ（AIを自動で育てる）

パイプライン実行後、毎回以下を実行すること:

1. `kpi_feedback.md` の「成功パターン」「失敗パターン」を更新
2. `context/MEMORY.md` に今回のセッションで気づいた改善点を追記
3. 次回のパイプライン冒頭で `kpi_feedback.md` を読み込んで反映

## 環境設定

- `.env` ファイルに全APIキーを設定すること（`.gitignore` 対象）
- `PROJECT.md` でメディア固有設定をカスタマイズすること
- 詳細なセットアップ手順は `SEOオウンドメディア自動化_セットアップ.md` セクション3を参照

## スケジュール実行（Claude Code Scheduled Tasks）

```
Morning Pipeline:   毎日 5:00 JST  → Phase 1〜7 実行
Afternoon Pipeline: 毎日 14:00 JST → Phase 1〜7 実行
Daily KPI Report:   毎日 22:13 JST → KPIレポート生成
Weekly Optimize:    月曜 10:23 JST → カニバリ検出・リライト・最適化
```
