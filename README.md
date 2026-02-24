# ESNav 5.0 自動操舵 講習会資料

中華製GPS自動操舵システム ESNav 5.0 の操作ガイド講習会用Webサイト。

## ファイル構成

- `esnav-lecture.html` — 完成品（単体で動作するセルフコンテインドHTML）
- `gen_lecture.py` — HTML生成スクリプト
- `lecture-assets/` — 素材ファイル
  - `images_b64.json` — PPTXから抽出した画像（Base64）
  - `infographic-board.html` — インフォグラフィック（付箋ボード）
  - `diagrams.html` — SVGダイアグラム3点
  - `slide*.jpg/png` — 元画像ファイル

## 使い方

`esnav-lecture.html` をブラウザで開くだけ。サーバー不要。

### 再生成する場合

```bash
cd lecture-assets
python ../gen_lecture.py
```

## 内容

1. ESNav 5.0 操作手順（5ステップ）
2. インフォグラフィック（付箋ボード風まとめ）
3. 技術ダイアグラム（操作フロー / RTK-GPS構成 / AB直線 vs 自由曲線）
4. ホクレンRTK接続ガイド
5. Q&A
