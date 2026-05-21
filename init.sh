#!/bin/bash
# SEOオウンドメディア パイプライン ヘルスチェックスクリプト
# セッション開始時に実行してAPIキーと環境の疎通を確認する

set -e

echo "======================================"
echo " SEOオウンドメディア ヘルスチェック"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================"

# .env 読み込み
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
  echo "[OK] .env ファイルを読み込みました"
else
  echo "[ERROR] .env ファイルが見つかりません"
  echo "  → .env を作成して認証情報を設定してください"
  exit 1
fi

echo ""
echo "--- 必須APIキーの存在確認 ---"

check_env() {
  local key=$1
  local label=$2
  if [ -z "${!key}" ] || [ "${!key}" = "YOUR_${key}" ] || [[ "${!key}" == *"YOUR_"* ]]; then
    echo "[WARN] $label ($key) が未設定です"
    MISSING_KEYS=true
  else
    echo "[OK]  $label"
  fi
}

MISSING_KEYS=false

check_env "WP_URL"           "WordPress URL"
check_env "WP_USER"          "WordPress ユーザー名"
check_env "WP_PASSWORD"      "WordPress Application Password"
check_env "X_BEARER_TOKEN"   "X(Twitter) Bearer Token"
check_env "YOUTUBE_API_KEY"  "YouTube Data API v3"
check_env "SPREADSHEET_ID"   "Google Spreadsheet ID"
check_env "AHREFS_API_KEY"   "Ahrefs API Key"
check_env "GEMINI_API_KEY"   "Gemini API Key（画像生成）"

echo ""
echo "--- オプションAPIキーの確認 ---"
check_env "GA4_PROPERTY_ID"  "Google Analytics 4 Property ID"
check_env "GSC_SITE_URL"     "Google Search Console サイトURL"

echo ""
echo "--- ファイル・ディレクトリの確認 ---"

check_file() {
  local path=$1
  local label=$2
  if [ -e "$path" ]; then
    echo "[OK]  $label"
  else
    echo "[WARN] $label が見つかりません: $path"
  fi
}

check_file "PROJECT.md"                         "PROJECT.md（メディア設定）"
check_file "context/feature_list.json"         "context/feature_list.json（Phase進捗）"
check_file "context/claude-progress.md"        "context/claude-progress.md（セッション引き継ぎ）"
check_file "context/MEMORY.md"                 "context/MEMORY.md（学習記憶）"
check_file "kpi_feedback.md"                   "kpi_feedback.md（KPIフィードバック）"
check_file "articles"                          "articles/ ディレクトリ"
check_file "automation/images"                 "automation/images/ ディレクトリ"
check_file "data/x_trends"                     "data/x_trends/ ディレクトリ"
check_file "data/youtube_transcripts"          "data/youtube_transcripts/ ディレクトリ"

echo ""
echo "--- ツールの確認 ---"

check_cmd() {
  local cmd=$1
  local label=$2
  if command -v "$cmd" &> /dev/null; then
    echo "[OK]  $label"
  else
    echo "[WARN] $label が見つかりません: $cmd"
    echo "       → インストール: pip install yt-dlp"
  fi
}

check_cmd "python3"  "Python 3"
check_cmd "yt-dlp"   "yt-dlp（YouTube字幕取得）"

echo ""
echo "--- WordPress API 疎通確認 ---"
if [ -n "$WP_URL" ] && [[ "$WP_URL" != *"YOUR_"* ]]; then
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "${WP_URL}/wp-json/wp/v2/posts?per_page=1" 2>/dev/null || echo "000")
  if [ "$HTTP_STATUS" = "200" ]; then
    echo "[OK]  WordPress REST API 応答あり（HTTP $HTTP_STATUS）"
  else
    echo "[WARN] WordPress REST API の応答なし（HTTP $HTTP_STATUS）"
    echo "       → WP_URL が正しいか、REST APIが有効か確認してください"
  fi
else
  echo "[SKIP] WordPress URL 未設定のためスキップ"
fi

echo ""
echo "======================================"
if [ "$MISSING_KEYS" = true ]; then
  echo " [要対応] 未設定のAPIキーがあります"
  echo " → docs/api-setup-guide.md を参照して設定してください"
  echo " → 設定後に再度 bash init.sh を実行してください"
else
  echo " [OK] ヘルスチェック完了"
  echo " → CLAUDE.md の手順に従ってパイプラインを開始してください"
fi
echo "======================================"
