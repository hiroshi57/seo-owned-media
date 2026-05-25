"""
Phase 6: 公開エージェント
1. アイキャッチ画像を Gemini で生成
2. Markdown → HTML 変換
3. WordPress に下書き投稿
"""
import os, re, json, base64, requests
from dotenv import load_dotenv

load_dotenv(override=True)
WP_URL      = os.getenv('WP_URL')
WP_USER     = os.getenv('WP_USER')
WP_PASSWORD = os.getenv('WP_PASSWORD')
GEMINI_KEY  = os.getenv('GEMINI_API_KEY')

ARTICLE_PATH = 'articles/article_002_draft.md'
ARTICLE_NUM  = '002'
os.makedirs('automation/images', exist_ok=True)

# ── 1. Markdown 読み込み ───────────────────────
with open(ARTICLE_PATH, encoding='utf-8') as f:
    md_text = f.read()

# フロントマター除去（# タイトル行まで）
lines = md_text.split('\n')
content_lines = [l for l in lines if not l.startswith('**対象KW**')
                 and not l.startswith('**ステータス**')
                 and not l.startswith('**文字数**')
                 and not l.startswith('**作成日**')
                 and not l.startswith('**カテゴリ**')]
md_clean = '\n'.join(content_lines)

# タイトル抽出
title_match = re.search(r'^# (.+)', md_clean, re.MULTILINE)
title = title_match.group(1) if title_match else '中小企業向け業務自動化ツール8選比較'
# 本文（H1行を除く）
body_md = re.sub(r'^# .+\n', '', md_clean, count=1).strip()

# ── 2. Markdown → HTML 変換 ─────────────────────
import re as _re

# 前処理: フロントマター区切りの --- を除去、info-box/cta-box を一時退避して変換
def preprocess_md(text):
    # フロントマター行末尾の --- を除去
    text = _re.sub(r'^---\s*$', '', text, flags=_re.MULTILINE)
    # <div class="..."> 内の markdown を変換するため、div ブロックを抽出・変換
    def convert_div(m):
        tag_open  = m.group(1)   # <div class="...">
        inner_md  = m.group(2)   # div内のmarkdown
        tag_close = m.group(3)   # </div>
        inner_html = markdown.markdown(
            inner_md.strip(),
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        return f'{tag_open}\n{inner_html}\n{tag_close}'
    text = _re.sub(
        r'(<div[^>]*>)(.*?)(</div>)',
        convert_div, text, flags=_re.DOTALL
    )
    return text

try:
    import markdown
    clean_md   = preprocess_md(body_md)
    html_content = markdown.markdown(
        clean_md,
        extensions=['tables', 'fenced_code', 'nl2br']
    )
    # 連続 <hr> を1つに圧縮、先頭 <hr> を除去
    html_content = _re.sub(r'(<hr\s*/?>[\s\n]*)+', '<hr />\n', html_content)
    html_content = _re.sub(r'^\s*<hr\s*/?>\s*', '', html_content)
    print('[OK] Markdown → HTML 変換完了')
except ImportError:
    html_content = body_md.replace('\n\n', '</p><p>').replace('\n', '<br>')
    html_content = f'<p>{html_content}</p>'
    print('[WARN] markdown ライブラリなし、簡易変換使用')

# ── 3. Gemini でアイキャッチ画像生成 ───────────────
print('\n[INFO] アイキャッチ画像を生成中...')
image_path = f'automation/images/article_{ARTICLE_NUM}_featured.png'
image_id   = None

gemini_url = (
    'https://generativelanguage.googleapis.com/v1beta/models/'
    f'gemini-2.5-flash-image:generateContent?key={GEMINI_KEY}'
)
payload = {
    "contents": [{
        "parts": [{
            "text": (
                "Professional business illustration for a Japanese blog article "
                "about business automation tools for small and medium enterprises. "
                "Workflow automation concept: connected app icons, gears, arrows, "
                "business efficiency theme, clean modern flat design, "
                "blue and green color scheme, wide 16:9 format, "
                "absolutely no text, no letters, no words anywhere in the image."
            )
        }]
    }],
    "generationConfig": {
        "responseModalities": ["IMAGE"]
    }
}
resp = requests.post(gemini_url, json=payload, timeout=60)
if resp.status_code == 200:
    data = resp.json()
    img_b64 = data['candidates'][0]['content']['parts'][0]['inlineData']['data']
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print(f'[OK] 画像生成完了: {image_path}')

    # WordPress に画像アップロード
    print('[INFO] WordPress に画像をアップロード中...')
    with open(image_path, 'rb') as img_file:
        media_resp = requests.post(
            f'{WP_URL}/wp-json/wp/v2/media',
            auth=(WP_USER, WP_PASSWORD),
            headers={'Content-Disposition': f'attachment; filename="article_{ARTICLE_NUM}_featured.png"',
                     'Content-Type': 'image/png'},
            data=img_file.read(),
            timeout=30
        )
    if media_resp.status_code in (200, 201):
        image_id = media_resp.json()['id']
        print(f'[OK] 画像アップロード完了 (media_id: {image_id})')
    else:
        print(f'[WARN] 画像アップロード失敗: {media_resp.status_code}')
else:
    print(f'[WARN] 画像生成失敗: {resp.status_code} {resp.text[:200]}')
    print('[INFO] アイキャッチなしで投稿を続行します')

# ── 4. WordPress に投稿（既存記事は UPDATE、新規は POST）───────
existing_json = f'data/wp_post_article{ARTICLE_NUM}.json'
existing_post_id = None
if os.path.exists(existing_json):
    with open(existing_json, encoding='utf-8') as f:
        existing_post_id = json.load(f).get('post_id')

# タイトルから安全なスラッグを生成（｜・などの特殊文字を除去）
import unicodedata as _ud
slug_base = _re.sub(r'[｜|・／/【】「」『』《》〈〉\s]+', '-', title)
slug_base = _re.sub(r'[-]+', '-', slug_base).strip('-')
slug_base = slug_base[:60]  # WordPress推奨の最大長

post_data = {
    'title':   title,
    'slug':    slug_base,
    'content': html_content,
    'status':  'publish',
    'excerpt': 'Zapier・Make・Power Automate・kintoneなど、中小企業が導入しやすい業務自動化ツール8選をコスト・難易度・おすすめシーン別に比較します。',
    'meta': {
        'rank_math_focus_keyword': '業務自動化 ツール 中小企業',
        'rank_math_description': '中小企業向け業務自動化ツール8選を徹底比較。Zapier・Power Automate・kintoneなど導入コスト・難易度・おすすめシーン別にわかりやすく解説。'
    }
}
if image_id:
    post_data['featured_media'] = image_id

if existing_post_id:
    print(f'\n[INFO] 既存記事 (ID: {existing_post_id}) を更新中...')
    post_resp = requests.post(
        f'{WP_URL}/wp-json/wp/v2/posts/{existing_post_id}',
        auth=(WP_USER, WP_PASSWORD),
        json=post_data,
        timeout=30
    )
    action_label = '更新'
else:
    print(f'\n[INFO] WordPress に新規投稿中...')
    post_resp = requests.post(
        f'{WP_URL}/wp-json/wp/v2/posts',
        auth=(WP_USER, WP_PASSWORD),
        json=post_data,
        timeout=30
    )
    action_label = '新規投稿'

if post_resp.status_code in (200, 201):
    post = post_resp.json()
    post_id  = post['id']
    post_url = post.get('link', '')
    edit_url = f'{WP_URL}/wp-admin/post.php?post={post_id}&action=edit'

    print(f'\n[OK] {action_label}完了！')
    print(f'  投稿ID  : {post_id}')
    print(f'  編集URL : {edit_url}')
    print(f'  公開URL : {post_url}')

    with open(existing_json, 'w', encoding='utf-8') as f:
        json.dump({'post_id': post_id, 'edit_url': edit_url,
                   'publish_url': post_url, 'image_id': image_id}, f, ensure_ascii=False, indent=2)
else:
    print(f'[ERROR] {action_label}失敗: {post_resp.status_code}')
    print(post_resp.text[:500])
