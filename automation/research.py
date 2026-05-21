"""
Phase 2: リサーチエージェント
- Google News RSS で最新記事を収集
- YouTube Data API で関連動画を検索・字幕取得
"""
import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

TARGET_KW = "ChatGPT 業務効率化 具体例"
os.makedirs("data/youtube_transcripts", exist_ok=True)
os.makedirs("data/x_trends", exist_ok=True)

print("=== Phase 2: リサーチ開始 ===")
print(f"対象KW: {TARGET_KW}\n")

# ─────────────────────────────────────
# 1. Google News RSS
# ─────────────────────────────────────
print("--- Google News RSS 収集 ---")
query = urllib.parse.quote("ChatGPT 業務効率化")
rss_url = f"https://news.google.com/rss/search?q={query}&hl=ja&gl=JP&ceid=JP:ja"

news_items = []
try:
    req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        xml_data = response.read()
    root = ET.fromstring(xml_data)
    for item in root.findall('.//item')[:10]:
        title = item.findtext('title', '').replace(' - Google ニュース', '')
        link  = item.findtext('link', '')
        pubdate = item.findtext('pubDate', '')
        news_items.append({"title": title, "url": link, "date": pubdate})
        print(f"  [NEWS] {title[:50]}...")
    print(f"\n  → {len(news_items)}件 収集完了\n")
except Exception as e:
    print(f"  [WARN] Google News RSS 取得失敗: {e}\n")

# ─────────────────────────────────────
# 2. YouTube 動画検索
# ─────────────────────────────────────
print("--- YouTube 動画検索 ---")
yt_query = urllib.parse.quote("ChatGPT 業務効率化 使い方")
yt_url = (
    f"https://www.googleapis.com/youtube/v3/search"
    f"?part=snippet&q={yt_query}&maxResults=5&regionCode=JP"
    f"&relevanceLanguage=ja&type=video&key={YOUTUBE_API_KEY}"
)

videos = []
try:
    with urllib.request.urlopen(yt_url, timeout=15) as r:
        yt_data = json.loads(r.read())
    for item in yt_data.get('items', []):
        vid_id    = item['id']['videoId']
        vid_title = item['snippet']['title']
        channel   = item['snippet']['channelTitle']
        videos.append({"id": vid_id, "title": vid_title, "channel": channel})
        print(f"  [YT] {vid_title[:50]}...")
    print(f"\n  → {len(videos)}件 取得完了\n")
except Exception as e:
    print(f"  [WARN] YouTube API 失敗: {e}\n")

# ─────────────────────────────────────
# 3. yt-dlp で字幕取得（上位3本）
# ─────────────────────────────────────
print("--- YouTube 字幕取得 ---")
import subprocess

transcripts = []
for v in videos[:3]:
    vid_id = v['id']
    out_path = f"data/youtube_transcripts/{vid_id}"
    cmd = [
        "yt-dlp",
        "--write-auto-sub", "--sub-lang", "ja",
        "--skip-download", "--sub-format", "vtt",
        "-o", out_path,
        f"https://www.youtube.com/watch?v={vid_id}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    # vttファイルを探す
    vtt_file = f"{out_path}.ja.vtt"
    if os.path.exists(vtt_file):
        with open(vtt_file, encoding='utf-8') as f:
            raw = f.read()
        # vttからテキスト抽出（タグ・タイムスタンプ除去）
        import re
        lines = raw.split('\n')
        text_lines = []
        for line in lines:
            line = line.strip()
            if (line and not line.startswith('WEBVTT')
                    and not re.match(r'^\d{2}:', line)
                    and not re.match(r'^NOTE', line)
                    and '-->' not in line
                    and not re.match(r'^\d+$', line)):
                clean = re.sub(r'<[^>]+>', '', line)
                if clean:
                    text_lines.append(clean)
        transcript_text = ' '.join(dict.fromkeys(text_lines))[:2000]
        v['transcript'] = transcript_text
        transcripts.append(v)
        print(f"  [OK] 字幕取得: {v['title'][:40]}...")
    else:
        v['transcript'] = ''
        print(f"  [SKIP] 字幕なし: {v['title'][:40]}...")

# ─────────────────────────────────────
# 4. 結果を保存
# ─────────────────────────────────────
result = {
    "keyword": TARGET_KW,
    "collected_at": datetime.now().isoformat(),
    "news": news_items,
    "youtube": videos,
    "transcripts_count": len(transcripts)
}
with open("data/x_trends/research_article1.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n=== 収集完了 ===")
print(f"ニュース: {len(news_items)}件")
print(f"YouTube動画: {len(videos)}件（字幕取得: {len(transcripts)}件）")
print(f"保存先: data/x_trends/research_article1.json")
