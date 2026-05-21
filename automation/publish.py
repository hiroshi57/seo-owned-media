"""
Phase 6: 公開エージェント
1. アイキャッチ画像を Gemini で生成
2. Markdown → HTML 変換
3. WordPress に下書き投稿
"""
import os, re, json, base64, requests
from dotenv import load_dotenv

load_dotenv()
WP_URL      = os.getenv('WP_URL')
WP_USER     = os.getenv('WP_USER')
WP_PASSWORD = os.getenv('WP_PASSWORD')
GEMINI_KEY  = os.getenv('GEMINI_API_KEY')

ARTICLE_PATH = 'articles/article_001_draft.md'
os.makedirs('automation/images', exist_ok=True)

# ── 1. Markdown 読み込み ───────────────────────
with open(ARTICLE_PATH, encoding='utf-8') as f:
    md_text = f.read()

# フロントマター除去（# タイトル行まで）
lines = md_text.split('\n')
content_lines = [l for l in lines if not l.startswith('**対象KW**')
                 and not l.startswith('**ステータス**')
                 and not l.startswith('**文字数**')
                 and not l.startswith('**作成日**')]
md_clean = '\n'.join(content_lines)

# タイトル抽出
title_match = re.search(r'^# (.+)', md_clean, re.MULTILINE)
title = title_match.group(1) if title_match else 'ChatGPT業務効率化の具体例15選'
# 本文（H1行を除く）
body_md = re.sub(r'^# .+\n', '', md_clean, count=1).strip()

# ── 2. Markdown → HTML 変換 ─────────────────────
try:
    import markdown
    html_content = markdown.markdown(
        body_md,
        extensions=['tables', 'fenced_code', 'nl2br']
    )
    print('[OK] Markdown → HTML 変換完了')
except ImportError:
    # fallback: 簡易変換
    html_content = body_md.replace('\n\n', '</p><p>').replace('\n', '<br>')
    html_content = f'<p>{html_content}</p>'
    print('[WARN] markdown ライブラリなし、簡易変換使用')

# ── 3. Gemini でアイキャッチ画像生成 ───────────────
print('\n[INFO] アイキャッチ画像を生成中...')
image_path = 'automation/images/article_001_featured.png'
image_id   = None

gemini_url = (
    'https://generativelanguage.googleapis.com/v1beta/models/'
    f'imagen-3.0-generate-001:predict?key={GEMINI_KEY}'
)
payload = {
    "instances": [{
        "prompt": (
            "Professional business illustration, Japanese office setting, "
            "a business person using laptop with AI assistant interface, "
            "clean modern design, blue and white color scheme, "
            "no text, no English letters, 16:9 aspect ratio"
        )
    }],
    "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}
}
resp = requests.post(gemini_url, json=payload, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    img_b64 = data['predictions'][0]['bytesBase64Encoded']
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print(f'[OK] 画像生成完了: {image_path}')

    # WordPress に画像アップロード
    print('[INFO] WordPress に画像をアップロード中...')
    with open(image_path, 'rb') as img_file:
        media_resp = requests.post(
            f'{WP_URL}/wp-json/wp/v2/media',
            auth=(WP_USER, WP_PASSWORD),
            headers={'Content-Disposition': 'attachment; filename="article_001_featured.png"',
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

# ── 4. WordPress に下書き投稿 ───────────────────
print('\n[INFO] WordPress に下書き投稿中...')
post_data = {
    'title':   title,
    'content': html_content,
    'status':  'draft',
    'excerpt': 'MIXIが月間17,600時間削減した具体的な方法を、中小企業向けプロンプト付きで15例紹介します。',
    'meta': {
        'rank_math_focus_keyword': 'ChatGPT 業務効率化 具体例',
        'rank_math_description': 'ChatGPT業務効率化の具体例を15個、コピペで使えるプロンプト付きで紹介。MIXIの月17,600時間削減事例など一次情報も掲載。中小企業経営者向け。'
    }
}
if image_id:
    post_data['featured_media'] = image_id

post_resp = requests.post(
    f'{WP_URL}/wp-json/wp/v2/posts',
    auth=(WP_USER, WP_PASSWORD),
    json=post_data,
    timeout=30
)

if post_resp.status_code in (200, 201):
    post = post_resp.json()
    post_id  = post['id']
    post_url = post.get('link', '')
    edit_url = f'{WP_URL}/wp-admin/post.php?post={post_id}&action=edit'

    print(f'\n[OK] 下書き投稿完了！')
    print(f'  投稿ID  : {post_id}')
    print(f'  編集URL : {edit_url}')
    print(f'  下書きURL: {post_url}')

    # 結果を保存
    with open('data/wp_post_article1.json', 'w', encoding='utf-8') as f:
        json.dump({'post_id': post_id, 'edit_url': edit_url,
                   'draft_url': post_url, 'image_id': image_id}, f, ensure_ascii=False, indent=2)
else:
    print(f'[ERROR] 投稿失敗: {post_resp.status_code}')
    print(post_resp.text[:500])
