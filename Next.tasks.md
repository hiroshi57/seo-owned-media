# Next.tasks.md — 次にやること（優先順）

パイプライン実行前に必ず消化するタスク。完了したら `[ ]` を `[x]` に変更し、日付を記入する。

---

## MUST（これがないとパイプラインが動かない）

- [ ] **WordPress サイトを立ち上げる**
  - ホスティング契約 → WordPress インストール → SSL設定
  - Application Password を作成して `.env` に設定
  - Rank Math プラグインをインストール・有効化
  - カテゴリ5つ作成（AI活用事例 / AIツール比較 / AI導入ガイド / 業務自動化 / 最新AIトレンド）
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション1

- [ ] **X(Twitter) API v2 を取得する**
  - Basic プラン以上に申請（`note_tweet` フィールド取得に必須）
  - Bearer Token / API Key / API Secret を `.env` に設定
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション2

- [ ] **YouTube Data API v3 を取得する**
  - Google Cloud Console でプロジェクト作成 → API有効化 → APIキー取得
  - `yt-dlp` をインストール（`pip install yt-dlp`）
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション3

- [ ] **Google Sheets API を設定する**
  - OAuth 2.0 credentials.json を取得・配置
  - ~~スプレッドシートを10タブ構成で作成~~ ✅ 2026-05-20
  - ~~SPREADSHEET_ID を `.env` に設定~~ ✅ 2026-05-20
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション4

- [ ] **Ahrefs API / MCP を設定する**
  - APIキーを取得
  - `.mcp.json` を作成（[docs/api-setup-guide.md](docs/api-setup-guide.md) セクション6参照）

- [ ] **Gemini API キーを取得する**（画像生成用）
  - Google AI Studio でAPIキー取得 → `.env` に設定
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション7

- [ ] **`PROJECT.md` をカスタマイズする**
  - 運営者名・肩書き・実績を記入（E-E-A-T著者情報）
  - CTA文言・CTAリンクを設定
  - Ahrefsで競合サイトを調査して記入

- [ ] **`bash init.sh` を実行して全項目 `[OK]` を確認する**

---

## SHOULD（品質向上に効く）

- [ ] **Google Indexing API を設定する**（公開後即時インデックス登録）
  - サービスアカウント作成 → GSCでオーナー権限付与
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション5

- [ ] **Google Analytics 4 を設定する**（KPIレポートのPVデータ取得）
  - GA4プロパティ作成 → サービスアカウントに閲覧者権限付与
  - 参照: [docs/api-setup-guide.md](docs/api-setup-guide.md) セクション8

- [ ] **Claude Code Scheduled Tasks を設定する**（完全自動化）
  - Morning Pipeline: 毎日 5:00 JST
  - Afternoon Pipeline: 毎日 14:00 JST
  - Daily KPI Report: 毎日 22:13 JST
  - Weekly Optimize: 月曜 10:23 JST

---

## COULD（余裕があれば）

- [ ] NanoBanana API を取得する（高品質画像生成のフォールバック）
- [ ] Google Search Console を設定する（CTR・平均順位の取得）
- [ ] Slack Webhook を設定する（パイプライン完了通知）

---

## 完了済み

- [x] プロジェクトディレクトリ構成を作成（2026-05-20）
- [x] ハーネスファイル群を生成（CLAUDE.md, AGENTS.md, context/, init.sh）（2026-05-20）
- [x] `.env` テンプレートを作成（2026-05-20）
- [x] `PROJECT.md` にメディア設定を定義（2026-05-20）
- [x] `docs/api-setup-guide.md` を作成（2026-05-20）
