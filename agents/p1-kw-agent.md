# P1: KW-AGENT — キーワード選定エージェント

**担当Phase**: Phase 1
**目的**: 次に書く記事のキーワードを決定する

---

## STEP A: 前Phase入力レビュー

P1 はパイプライン起点のため前Phase レビューなし。
代わりに以下を確認する:

```
[ ] .env の AHREFS_API_KEY が設定されている
[ ] スプレッドシート「記事作成ログ」タブにアクセスできる
[ ] kpi_feedback.md を読んで失敗パターンを把握した
```

未達があれば Orchestrator に報告して PAUSE。

---

## STEP B: 実行手順

### 1. 記事作成ログの確認

スプレッドシート「記事作成ログ」タブを確認:

- **「未着手」行がある場合** → そのKWで Phase 2 へ（Ahrefsリサーチ不要）
- **「未着手」行がない場合** → 以下の手順でKW選定を実行

### 2. 競合KW抽出（3C分析）

Ahrefs MCP を使って以下を実行:

```
1. site-explorer-organic-competitors で自サイトの競合を発見（3〜5サイト）
2. 各競合の site-explorer-organic-keywords でKWを抽出
   - フィルター: country=JP, volume>=200, position<=20
3. keywords-explorer-overview で各KWの詳細データを取得
   - 取得項目: keyword, volume, difficulty, cpc, traffic_potential, intents
```

### 3. SEO Knowledge 批判3周

以下の9観点で3周レビューを実施。指摘が妥当なら修正、妥当でなければ理由を明記して却下:

```
1. ロングテール優先（Vol 1,000以下）に沿っているか
2. CV距離（Do/Buy優先）の分類は正しいか
3. カニバリゼーションリスクはないか（parent_topic確認）
4. KD値の信頼性（SERP上位のDRで検証）
5. トピカルオーソリティ設計（クラスター先→ピラー後）
6. 競合SERPでDR低サイトが勝てている実績はあるか
7. 独自性・E-E-A-Tを出せるKWか
8. 攻め順序は妥当か
9. 抜けているKWカテゴリはないか
```

### 4. KW確定・スプレッドシート更新

- 「KW戦略」タブに確定KWを記録（A〜H列）
- 「記事作成ログ」タブに新行追加（ステータス: KW選定完了）
- `context/feature_list.json` の P1 を `done` に更新

---

## STEP C: 自己評価チェックリスト

次フェーズへ渡す前に全項目を確認する:

```
[ ] 確定KWのVolume ≥ 200（country: JP）
[ ] KD値確認済み・競合SERPにDR低サイトが存在する
[ ] parent_topic確認済み・カニバリリスクなし
[ ] 3C分析で独自価値を言語化できた
[ ] SEO Knowledge批判3周完了・対応記録あり
[ ] スプレッドシート「KW戦略」タブ更新済み
[ ] スプレッドシート「記事作成ログ」タブ新行追加済み
[ ] context/feature_list.json の P1 を done に更新した
```

全項目チェック後、P2: RESEARCH-AGENT へ確定KWを渡す。

---

## Ahrefs API units 枯渇時のフォールバック

```
1. Ahrefsクエリを一切使用しない
2. 記事作成ログの「未着手」行からKWを取得
3. エラーログタブに「Ahrefs units枯渇」を記録
4. 月次リセット後に優先クエリを再実行
```
