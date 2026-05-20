# APIセットアップガイド — SEOオウンドメディア全自動パイプライン

`.env` に設定する全APIキーの取得手順をまとめたガイド。
**このファイルは `.gitignore` 対象外。APIキー自体は絶対にこのファイルに書かないこと。**

---

## セットアップの全体順序

```
1. WordPress（最初に必要）
2. X(Twitter) API v2
3. YouTube Data API v3
4. Google Sheets API
5. Google Indexing API
6. Ahrefs API（MCP経由）
7. 画像生成（Gemini API または NanoBanana）
8. Google Analytics 4（任意）
9. Google Search Console（任意）
```

---

## 1. WordPress — REST API + Application Password

**用途**: 記事投稿・画像アップロード・Rank Math設定（Phase 6）

### 手順

1. **WordPress サイトを用意する**
   - ホスティング例: Xserver、ConoHa WING、さくらインターネット
   - WordPress 4.7以降（REST APIがデフォルト有効）

2. **Application Password を作成する**
   - WordPress管理画面 → ユーザー → あなたのプロフィール
   - 下部の「アプリケーションパスワード」セクション
   - 「新しいアプリケーションパスワードの名前」に「SEO Pipeline」と入力
   - 「新しいアプリケーションパスワードを追加」ボタンをクリック
   - 表示されたパスワード（スペース区切り24文字）をコピー → **一度しか表示されない**

3. **Rank Math プラグインをインストール**
   - WordPress管理画面 → プラグイン → 新規追加 → 「Rank Math」で検索
   - インストール → 有効化
   - Rank Math設定ウィザードを完了する

4. **パーマリンク設定**
   - 設定 → パーマリンク → `/%category%/%postname%/` を選択 → 変更を保存

5. **カテゴリ作成**
   - 投稿 → カテゴリー → 以下を作成:
     - AI活用事例
     - AIツール比較
     - AI導入ガイド
     - 業務自動化
     - 最新AIトレンド
   - 各カテゴリのIDを控える（URLの `?tag_ID=XX` で確認可能）

6. **.env に設定**

```
WP_URL=https://あなたのドメイン.com
WP_USER=WordPressのユーザー名
WP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

### 疎通確認

```bash
curl -s "https://あなたのドメイン.com/wp-json/wp/v2/posts?per_page=1" | head -c 100
```
`[` で始まるJSONが返れば成功。

---

## 2. X(Twitter) API v2 — Bearer Token + API Key

**用途**: 関連投稿30件+全文(note_tweet)収集（Phase 2）

### 前提条件
- X(Twitter) アカウントが必要
- **Basic プラン以上**が必要（Free プランでは `note_tweet` フィールド取得不可）
  - Basic: 月$100。`note_tweet` フィールド対応
  - Pro: 月$5,000。大量収集が必要な場合

### 手順

1. X Developer Portal にアクセス: `https://developer.twitter.com/`

2. 「Sign up for Free Account」または「Developer account」を申請
   - 利用用途の説明を英語で記入（例: "I'm building a content marketing tool to analyze trending topics in Japanese market for SEO-optimized blog posts."）
   - 承認まで数時間〜数日かかる場合がある

3. **アプリを作成する**
   - Developer Portal → Projects & Apps → Overview → 「New App」
   - App name: `seo-media-pipeline`
   - 表示される Keys and Tokens をコピー:
     - API Key
     - API Key Secret
     - Bearer Token（これが最重要）

4. **App の権限設定**
   - App Settings → User authentication settings
   - App permissions: Read のみでOK
   - Type of App: Web App

5. **.env に設定**

```
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxx...（長い文字列）
X_API_KEY=xxxxxxxxxxxxxxxxxxxx
X_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 注意事項
- `note_tweet` フィールドは Basic プラン以上が必要
- Free プランでは通常の `text` フィールド（280字）しか取得できない
- 月の検索上限: Basic は 10,000 tweets/月

---

## 3. YouTube Data API v3

**用途**: 関連動画検索・字幕取得（Phase 2）

### 手順

1. Google Cloud Console にアクセス: `https://console.cloud.google.com/`

2. **プロジェクトを作成する**
   - 上部「プロジェクトを選択」→「新しいプロジェクト」
   - プロジェクト名: `seo-media-pipeline`
   - 作成

3. **YouTube Data API v3 を有効にする**
   - APIとサービス → ライブラリ → 「YouTube Data API v3」で検索
   - 有効にする

4. **APIキーを作成する**
   - APIとサービス → 認証情報 → 「認証情報を作成」→「APIキー」
   - 作成されたAPIキーをコピー
   - 「キーを制限」をクリック → APIの制限 → YouTube Data API v3 のみに制限（推奨）

5. **.env に設定**

```
YOUTUBE_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### yt-dlp のインストール（字幕取得ツール）

```bash
pip install yt-dlp
```

または

```bash
pip3 install yt-dlp
```

### 疎通確認

```bash
curl -s "https://www.googleapis.com/youtube/v3/search?part=snippet&q=AIツール&maxResults=1&key=YOUR_API_KEY" | python3 -m json.tool | head -20
```

---

## 4. Google Sheets API — OAuth 2.0

**用途**: スプレッドシート10タブへのデータ書き込み（Phase 1〜7全体）

### 手順

1. Google Cloud Console（上記と同じプロジェクトを使う）

2. **Google Sheets API を有効にする**
   - APIとサービス → ライブラリ → 「Google Sheets API」で検索
   - 有効にする

3. **OAuth 2.0 クライアントIDを作成する**
   - APIとサービス → 認証情報 → 「認証情報を作成」→「OAuth クライアント ID」
   - アプリケーションの種類: デスクトップアプリ
   - 名前: `seo-pipeline-sheets`
   - 作成 → 「JSONをダウンロード」
   - ダウンロードしたファイルを `credentials.json` にリネームしてプロジェクトルートに配置

4. **Google Sheets スプレッドシートを作成する**
   - Google Sheets で新規スプレッドシートを作成
   - 以下の10タブを作成（タブ名を正確に入力）:
     - KW戦略
     - トピッククラスター
     - X一次情報
     - YouTube一次情報
     - ダッシュボード
     - 記事作成ログ
     - KPIレポート
     - 内部リンク管理
     - リライトログ
     - エラーログ
   - URLからスプレッドシートIDをコピー:
     `https://docs.google.com/spreadsheets/d/【ここがID】/edit`

5. **.env に設定**

```
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials.json
GOOGLE_SHEETS_TOKEN_PATH=./sheets-token.json
SPREADSHEET_ID=1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

6. **初回認証（ブラウザでの認証が必要）**
   - パイプライン初回実行時にブラウザが開いてGoogleアカウント認証を求められる
   - 認証後、`sheets-token.json` が自動生成される
   - 以降は自動更新される（有効期限7日）

---

## 5. Google Indexing API — サービスアカウント

**用途**: 記事公開後の即時インデックス登録（Phase 7）

### 手順

1. Google Cloud Console（同じプロジェクト）

2. **Indexing API を有効にする**
   - APIとサービス → ライブラリ → 「Indexing API」で検索
   - 有効にする

3. **サービスアカウントを作成する**
   - APIとサービス → 認証情報 → 「認証情報を作成」→「サービスアカウント」
   - サービスアカウント名: `indexing-agent`
   - 作成して続行 → ロールは不要（スキップ）→ 完了
   - 作成されたサービスアカウントをクリック
   - 「キー」タブ → 「鍵を追加」→「新しい鍵を作成」→ JSON → 作成
   - ダウンロードされたJSONを `indexing-service-account.json` にリネームしてプロジェクトルートに配置

4. **Google Search Console でオーナー権限を付与する**
   - Google Search Console にアクセス: `https://search.google.com/search-console/`
   - 対象サイトを選択 → 設定 → ユーザーと権限
   - 「ユーザーを追加」→ サービスアカウントのメールアドレス（`indexing-agent@プロジェクトID.iam.gserviceaccount.com`）を入力
   - 権限: **オーナー**（重要: 確認済みオーナーである必要がある）

5. **.env に設定**

```
INDEXING_SERVICE_ACCOUNT_PATH=./indexing-service-account.json
GSC_SITE_URL=https://あなたのドメイン.com/
```

---

## 6. Ahrefs API — MCP経由

**用途**: KW調査・競合分析・SERP概要取得（Phase 1・3）

### 前提条件
- Ahrefs の有料プランが必要（Standard以上推奨）
- APIは別途 API units が消費される

### 手順

1. Ahrefs にログイン → Account Settings → API

2. APIキーを生成してコピー

3. **MCP設定** — `.mcp.json` をプロジェクトルートに作成:

```json
{
  "mcpServers": {
    "ahrefs": {
      "command": "npx",
      "args": ["-y", "@ahrefs/mcp-server"],
      "env": {
        "AHREFS_API_KEY": "あなたのAhrefsAPIキー"
      }
    }
  }
}
```

4. **.env にも設定**（init.shの確認用）

```
AHREFS_API_KEY=あなたのAhrefsAPIキー
```

### APIユニットの節約
- Phase 1（KW選定）と Phase 3（SERP概要）でのみ使用
- 月次リセット前はクエリを最小限に絞る
- 枯渇時は記事作成ログの「未着手」行からKWを取得（Ahrefsリサーチ不要）

---

## 7. 画像生成 API — Gemini または NanoBanana

**用途**: アイキャッチ画像・H2直下図解生成（Phase 6）

### Gemini API（推奨: 無料枠あり）

1. Google AI Studio にアクセス: `https://aistudio.google.com/`

2. 「Get API key」→「Create API key」→ 上記と同じCloud Projectを選択

3. **.env に設定**

```
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### NanoBanana（高品質な場合の選択肢）

1. NanoBanana にサインアップ（有料サービス）
2. APIキーを取得
3. **.env に設定**

```
NANOBANANA_API_KEY=あなたのNanoBananaキー
```

---

## 8. Google Analytics 4（任意）

**用途**: PV・エンゲージメント時間取得（Phase 7 KPIレポート）

### 手順

1. Google Analytics にアクセス: `https://analytics.google.com/`
2. 管理 → GA4プロパティを作成 → ウェブを選択 → URLを入力
3. プロパティIDをコピー（`properties/` の後の数字）
4. Cloud Console で **Google Analytics Data API** を有効化
5. 上記のサービスアカウントに GA4 の閲覧者権限を付与

```
GA4_PROPERTY_ID=123456789
```

---

## セットアップ完了チェックリスト

```
[ ] WordPress 構築完了・Application Password 取得済み
[ ] Rank Math インストール済み
[ ] カテゴリ5つ作成済み（IDを控えた）
[ ] X API v2 Basic プラン契約・Bearer Token 取得済み
[ ] YouTube Data API v3 APIキー取得済み
[ ] yt-dlp インストール済み
[ ] Google Sheets API credentials.json 配置済み
[ ] Googleスプレッドシート10タブ作成済み（SPREADSHEET_ID を.envに設定）
[ ] Google Indexing API サービスアカウント設定済み・GSCでオーナー権限付与済み
[ ] Ahrefs API キー取得済み・.mcp.json 作成済み
[ ] Gemini API キー取得済み
[ ] .env の全項目に実際の値を設定した
[ ] bash init.sh を実行して [OK] が全項目に表示された
[ ] PROJECT.md の著者情報・CTA・競合サイトを記入した
```

全項目が揃ったら `「記事を書いて」` でパイプライン開始。
