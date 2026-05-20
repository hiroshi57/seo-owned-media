# MEMORY.md — プロジェクト長期記憶（上限2,000文字）

セッション開始時に必ず読む。エージェントの行動を調整するための記憶インデックス。

---

## 環境

- OS: Windows 11 / PowerShell
- プロジェクトルート: `C:\Users\takiz\git_taki57\seo-owned-media`
- 起動コマンド: `bash init.sh`（APIキー・ツール疎通確認）
- Python: `python3` / yt-dlp: `pip install yt-dlp`

## ファイル構成（役割早引き）

| ファイル | 役割 |
|:--------|:----|
| `CLAUDE.md` | コマンド対応表・スケジュール定義・自己学習ループ |
| `AGENTS.md` | 7エージェント定義・自己評価チェックリスト・ルーティング |
| `PROJECT.md` | メディア設定・ペルソナ・CTA・著者情報（要カスタマイズ） |
| `Next.tasks.md` | 次にやること優先リスト（WordPress設定など） |
| `kpi_feedback.md` | 成功/失敗パターン（パイプライン冒頭で読む） |
| `context/MEMORY.md` | エージェント実行後の学習記録（蓄積式・2000字上限） |
| `context/claude-progress.md` | セッション引き継ぎ記録 |
| `context/feature_list.json` | Phase進捗管理（各PhaseのStatusを更新） |
| `.env` | 全APIキー（git管理外） |
| `docs/api-setup-guide.md` | 全APIの取得・設定手順 |

## 重要ルール（省略すると壊れる）

1. Phase 3完了後は必ずH2構成をユーザーに提示して承認を得てからPhase 4へ
2. WordPress公開（status: publish）は承認なしに実行しない
3. 品質スコアが95点未満の場合は最大3サイクル修正後にユーザー報告
4. 画像の英語テキスト混入は再生成（目視確認必須）
5. 各エージェントはSTEP A（前Phase出力レビュー）→ STEP B（自己評価）の順で実行

## セットアップ進捗（2026-05-20 時点）

### 完了済み

- [x] プロジェクトディレクトリ構成・ハーネスファイル群を生成
- [x] CLAUDE.md / AGENTS.md / MEMORY.md / Next.tasks.md 作成
- [x] context/ 配下（feature_list.json / claude-progress.md / MEMORY.md）作成
- [x] .env テンプレート・PROJECT.md・init.sh・.gitignore 作成
- [x] docs/api-setup-guide.md 作成（全API取得手順書）

### 明日実施予定（APIセットアップ）

- [ ] X(Twitter) API v2 申請（Basic プラン $100/月・承認に数時間〜数日）
  - 申請文は `docs/api-setup-guide.md` セクション2 のコピペ文を使う
- [ ] YouTube Data API v3 取得（Google Cloud Console・即日）
- [ ] Google Sheets API 設定（credentials.json 取得・スプレッドシート10タブ作成）
- [ ] Gemini API キー取得（Google AI Studio・即日）
- [ ] Ahrefs API キー確認・.mcp.json 作成

### 後回し

- [ ] Xserver 契約 → WordPress インストール（ドメインは後日決定）
- [ ] Google Indexing API 設定
- [ ] Google Analytics 4 設定
- [ ] Claude Code Scheduled Tasks 設定

### 決定済み構成

- ホスティング: Xserver（バックエンド WordPress）
- フロント: WordPress テーマそのまま表示（Headless 構成は採用しない）
- ドメイン: 後日決定（Xserver 仮ドメインで先行して動作確認可能）

## 学んだミス（実行後に追記）

<!-- フォーマット: [日付] [ミスの内容] → [対策] -->
- 2026-05-20 初期化。学習データなし。

## 成功パターン（踏襲せよ）

- （パイプライン実行後に追記）

## 関連ファイルポインタ

- 詳細手順: `SEOオウンドメディア自動化_セットアップ.md`
- APIセットアップ: `docs/api-setup-guide.md`
- 実行ログ: `automation/logs/`
