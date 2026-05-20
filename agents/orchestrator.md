# Orchestrator — パイプライン司令塔

パイプライン全体を制御する。次に動かすエージェントを決め、差し戻しと完了を管理する。

---

## 起動時の確認手順

1. `context/feature_list.json` を読んで各Phase の status を確認
2. `context/claude-progress.md` を読んで前回の中断箇所を確認
3. `kpi_feedback.md` を読んで失敗パターンを確認
4. 以下のルーティング表に従って次のエージェントを決定する

---

## ルーティング優先度

```
優先度 | 条件                                        | 次のアクション
1      | .env に未設定APIキーがある                   | PAUSE → ユーザーに設定を依頼
2      | 記事作成ログに「未着手」行がある               | P1: KW-AGENT を起動
3      | P1=done / P2=pending                        | P2: RESEARCH-AGENT を起動
4      | P2=done / P3=pending                        | P3: DESIGN-AGENT を起動
5      | P3=done / P4=pending                        | P4: WRITER-AGENT を起動
6      | P4=done / P5=pending                        | P5: QA-AGENT を起動
7      | P5=done / P6=pending                        | P6: PUBLISH-AGENT を起動
8      | P6=done / P7=pending                        | P7: ANALYTICS-AGENT を起動
9      | 全Phase=done                                | 次記事へ → P1 に戻る
```

---

## 差し戻しの処理

各エージェントが差し戻しを出した場合:

```
差し戻しを受け取る
  → 差し戻し先の Phase を pending に戻す
  → 差し戻し理由を context/claude-progress.md に記録
  → 差し戻し先エージェントを再起動
```

差し戻しは1段階のみ許可（P4→P3 はOK、P4→P2 は不可）。

---

## セッション終了時の処理

```
1. context/feature_list.json の全 Phase status を最新状態に更新
2. context/claude-progress.md に今回の進捗を追記
3. 次回の再開ポイントを明記する
```

---

## 出力フォーマット

```
--- ORCHESTRATOR ---
現在のPhase: [Px]
次のエージェント: [エージェント名]
理由: [なぜそのエージェントを選んだか]
--------------------
```
