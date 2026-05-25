"""
アイキャッチ画像生成 - Imagen 4.0
"""
import os, base64, requests, json
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
WP_URL     = os.getenv('WP_URL')
WP_USER    = os.getenv('WP_USER')
WP_PASSWORD= os.getenv('WP_PASSWORD')

os.makedirs('automation/images', exist_ok=True)
image_path = 'automation/images/article_001_featured.png'

# ── 1. Imagen 4.0 で画像生成 ────────────────────
print('[INFO] Imagen 4.0 でアイキャッチ画像を生成中...')

url = (
    f'https://generativelanguage.googleapis.com/v1beta/models/'
    f'imagen-4.0-fast-generate-001:predict?key={GEMINI_KEY}'
)
payload = {
    "instances": [{
        "prompt": (
            "Professional business illustration for a Japanese blog article about ChatGPT productivity. "
            "A Japanese businessperson sitting at a clean modern desk with a laptop showing an AI chat interface. "
            "Blue and white minimalist design. Soft office background with natural light. "
            "No text, no letters, no words anywhere in the image. "
            "16:9 wide format, high quality, photorealistic style."
        )
    }],
    "parameters": {
        "sampleCount": 1,
        "aspectRatio": "16:9",
        "safetyFilterLevel": "block_few"
    }
}

resp = requests.post(url, json=payload, timeout=60)
print(f'  ステータス: {resp.status_code}')

if resp.status_code == 200:
    data = resp.json()
    img_b64 = data['predictions'][0]['bytesBase64Encoded']
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print(f'[OK] 画像生成完了: {image_path}')
else:
    print(f'[ERROR] {resp.text[:300]}')
    exit(1)

# ── 2. 英語テキスト混入チェック（目視確認を促す）──
print(f'\n[CHECK] 画像を目視確認してください: {os.path.abspath(image_path)}')
print('  → 英語テキストや文字が混入していないか確認')
print('  → 問題なければ Enter を押してWordPressにアップロード')
input()

# ── 3. WordPress に画像をアップロード ────────────
print('[INFO] WordPress に画像をアップロード中...')
with open(image_path, 'rb') as img_file:
    media_resp = requests.post(
        f'{WP_URL}/wp-json/wp/v2/media',
        auth=(WP_USER, WP_PASSWORD),
        headers={
            'Content-Disposition': 'attachment; filename="article_001_featured.png"',
            'Content-Type': 'image/png'
        },
        data=img_file.read(),
        timeout=30
    )

if media_resp.status_code in (200, 201):
    media_data = media_resp.json()
    image_id  = media_data['id']
    image_url = media_data['source_url']
    print(f'[OK] アップロード完了')
    print(f'  media_id: {image_id}')
    print(f'  URL: {image_url}')

    # ── 4. 既存の下書き投稿にアイキャッチを設定 ──
    wp_data_path = 'data/wp_post_article1.json'
    if os.path.exists(wp_data_path):
        with open(wp_data_path) as f:
            wp_info = json.load(f)
        post_id = wp_info['post_id']

        update_resp = requests.post(
            f'{WP_URL}/wp-json/wp/v2/posts/{post_id}',
            auth=(WP_USER, WP_PASSWORD),
            json={'featured_media': image_id},
            timeout=30
        )
        if update_resp.status_code == 200:
            print(f'[OK] 投稿ID {post_id} にアイキャッチを設定しました')
            # JSONを更新
            wp_info['image_id'] = image_id
            wp_info['image_url'] = image_url
            with open(wp_data_path, 'w', encoding='utf-8') as f:
                json.dump(wp_info, f, ensure_ascii=False, indent=2)
        else:
            print(f'[WARN] アイキャッチ設定失敗: {update_resp.status_code}')
    else:
        print('[WARN] wp_post_article1.json が見つかりません')
else:
    print(f'[ERROR] アップロード失敗: {media_resp.status_code}')
    print(media_resp.text[:300])
