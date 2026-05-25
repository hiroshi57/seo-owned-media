---
name: project-overview
description: SEOオウンドメディア全自動パイプライン — 7フェーズ構成・ジャンル・ルール概要
metadata:
  type: project
---

## プロジェクト概要

AI・テクノロジー系オウンドメディアを Claude Code + 複数 API で全自動運営するパイプライン。

**Why:** 中小企業経営者向けに SEO 記事を自動生成・公開・分析することで、コンテンツマーケティングを省力化する。

**How to apply:** タスク実装時は必ずパイプラインの Phase 順序と依存関係を守る。

---

## パイプライン 7 フェーズ

| Phase | 名称 | 主な API |
|-------|------|---------|
| P1 | KW選定 | Ahrefs |
| P2 | リサーチ | X API v2, YouTube |
| P3 | 設計 | Ahrefs（SERP分析）|
| P4 | 執筆 | Claude |
| P5 | 品質チェック | Claude（5エージェント並列）|
| P6 | 公開 | WordPress, Gemini |
| P7 | 分析 | Google Indexing, Sheets, GA4 |

---

## 重要制約

1. Phase 3 完了後 → H2構成をユーザーに提示・承認後に Phase 4 へ
2. WordPress 公開（status: publish）は **承認なしに実行しない**
3. 品質スコア 95点未満 → 最大3サイクル修正 → それでも未達ならユーザー報告
4. 画像の英語テキスト混入 → 再生成（目視確認必須）

---

## 主要ファイル

| ファイル | 役割 |
|---------|------|
| `CLAUDE.md` | コマンド対応表・スケジュール定義 |
| `AGENTS.md` | 7エージェント定義 |
| `PROJECT.md` | メディア設定・ペルソナ |
| `kpi_feedback.md` | 成功/失敗パターン |
| `context/claude-progress.md` | セッション引き継ぎ記録 |
| `context/feature_list.json` | Phase 進捗管理 |
| `docs/api-setup-guide.md` | API取得手順書（詳細） |
