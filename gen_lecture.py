#!/usr/bin/env python3
"""ESNav 5.0 講習会メインWebサイト生成スクリプト"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load base64 images
with open('lecture-assets/images_b64.json', 'r') as f:
    imgs = json.load(f)

def img_src(key):
    val = imgs[key]
    if val.startswith('data:'):
        return val
    ext = key.split('.')[-1]
    mime = 'image/jpeg' if ext in ('jpg','jpeg') else 'image/png'
    return f'data:{mime};base64,{val}'

# Read infographic & diagram HTML
with open('lecture-assets/infographic-board.html', 'r', encoding='utf-8') as f:
    infographic_html = f.read()
with open('lecture-assets/diagrams.html', 'r', encoding='utf-8') as f:
    diagrams_html = f.read()

# Extract body from infographic (between <body> and </body>)
info_body = re.search(r'<body>(.*?)</body>', infographic_html, re.DOTALL).group(1)

# Extract sections from diagrams
diag_sections = re.findall(r'<section>.*?</section>', diagrams_html, re.DOTALL)

# Build image sources
img_slide1 = img_src('slide1_img0_Image_0.jpg')
img_slide3_1 = img_src('slide3_img1_Image_0.jpg')
img_slide3_2 = img_src('slide3_img4_Image_1.jpg')
img_slide4 = img_src('slide4_img1_Image_0.jpg')
img_slide5 = img_src('slide5_img1_Image_0.jpg')
img_slide6 = img_src('slide6_img1_Image_0.jpg')
img_s2_0 = img_src('slide2_img2_Image_0.png')
img_s2_1 = img_src('slide2_img6_Image_1.png')
img_s2_2 = img_src('slide2_img10_Image_2.png')
img_s2_3 = img_src('slide2_img14_Image_3.png')

diag_combined = '\n'.join(diag_sections)

html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ESNav 5.0 講習会 — GPS自動操舵システム操作ガイド</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-blue: #3b82f6;
    --accent-green: #22c55e;
    --accent-yellow: #fbbf24;
    --accent-red: #ef4444;
    --accent-purple: #a78bfa;
    --border: #334155;
    --radius: 16px;
  }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Noto Sans JP', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.8;
    min-height: 100vh;
  }}

  /* NAV */
  .nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(15,23,42,0.92); backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border); padding: 0 2rem;
  }}
  .nav-inner {{
    max-width: 1200px; margin: 0 auto;
    display: flex; align-items: center; gap: 2rem; height: 56px; overflow-x: auto;
  }}
  .nav-brand {{ font-weight: 700; font-size: 0.95rem; color: var(--accent-green); white-space: nowrap; flex-shrink: 0; }}
  .nav a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.82rem; font-weight: 500; white-space: nowrap; transition: color 0.2s; }}
  .nav a:hover {{ color: var(--text-primary); }}

  /* HERO */
  .hero {{
    padding: 120px 2rem 60px; text-align: center;
    background: linear-gradient(180deg, #0f172a 0%, #162032 60%, #0f172a 100%);
    position: relative; overflow: hidden;
  }}
  .hero::before {{
    content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(34,197,94,0.08) 0%, transparent 70%); pointer-events: none;
  }}
  .hero-badge {{
    display: inline-block; background: rgba(34,197,94,0.15); color: var(--accent-green);
    font-size: 0.75rem; font-weight: 700; letter-spacing: 3px; padding: 6px 20px;
    border-radius: 20px; border: 1px solid rgba(34,197,94,0.3); margin-bottom: 20px;
  }}
  .hero h1 {{
    font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 900; line-height: 1.2; margin-bottom: 16px;
    background: linear-gradient(135deg, #f1f5f9 0%, #94a3b8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }}
  .hero-sub {{ font-size: 1.1rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto 32px; }}
  .hero-date {{ font-size: 0.85rem; color: var(--text-muted); }}

  /* SECTION */
  .section {{ max-width: 1100px; margin: 0 auto; padding: 60px 2rem; }}
  .section-header {{ margin-bottom: 40px; }}
  .section-label {{ display: inline-block; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: var(--accent-blue); margin-bottom: 8px; }}
  .section-title {{ font-size: 1.8rem; font-weight: 800; line-height: 1.3; }}
  .section-desc {{ margin-top: 8px; color: var(--text-secondary); font-size: 0.95rem; }}

  /* OVERVIEW */
  .overview-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 48px; }}
  .overview-card {{
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 28px 24px; transition: transform 0.2s, border-color 0.2s;
  }}
  .overview-card:hover {{ transform: translateY(-4px); border-color: var(--accent-blue); }}
  .card-icon {{ font-size: 2rem; margin-bottom: 12px; display: block; }}
  .card-title {{ font-size: 1rem; font-weight: 700; margin-bottom: 8px; }}
  .card-text {{ font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; }}

  /* STEP */
  .step-section {{
    background: var(--bg-secondary); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 40px; margin-bottom: 32px; position: relative;
  }}
  .step-badge {{
    position: absolute; top: -16px; left: 32px;
    display: inline-flex; align-items: center; gap: 10px;
    padding: 6px 20px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; color: white;
  }}
  .step-badge.s1 {{ background: linear-gradient(135deg, #d97706, #92400e); }}
  .step-badge.s2 {{ background: linear-gradient(135deg, #2563eb, #1e3a8a); }}
  .step-badge.s3 {{ background: linear-gradient(135deg, #16a34a, #14532d); }}
  .step-badge.s4 {{ background: linear-gradient(135deg, #ea580c, #7c2d12); }}
  .step-badge.s5 {{ background: linear-gradient(135deg, #db2777, #831843); }}
  .step-content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; margin-top: 16px; }}
  .step-text h3 {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 16px; }}
  .step-text ul {{ list-style: none; padding: 0; }}
  .step-text ul li {{ padding: 6px 0 6px 20px; position: relative; font-size: 0.9rem; color: var(--text-secondary); }}
  .step-text ul li::before {{
    content: ''; position: absolute; left: 0; top: 14px;
    width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green);
  }}
  .step-images {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }}
  .step-images img {{ width: 100%; border-radius: 10px; border: 1px solid var(--border); cursor: zoom-in; transition: transform 0.2s; }}
  .step-images img:hover {{ transform: scale(1.03); }}
  .step-key {{
    display: inline-block; background: rgba(59,130,246,0.15); color: var(--accent-blue);
    padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem;
  }}

  /* INFOGRAPHIC */
  .infographic-wrap {{ border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); margin-bottom: 48px; }}
  .infographic-wrap .board {{ width: 100% !important; border-radius: 0 !important; }}

  /* DIAGRAM */
  .diagram-section {{ margin-bottom: 48px; }}
  .diagram-section .svg-wrap {{
    background: var(--bg-secondary); border-radius: var(--radius); border: 1px solid var(--border);
    padding: 1.5rem; overflow-x: auto; margin-bottom: 24px;
  }}
  .diagram-section .svg-wrap svg {{ display: block; width: 100%; height: auto; }}
  .diagram-section section h2 {{
    font-size: 1.1rem; font-weight: 600; color: var(--text-secondary);
    margin-bottom: 1rem; padding-left: 12px; border-left: 3px solid var(--accent-blue);
  }}

  /* RTK */
  .rtk-section {{
    background: linear-gradient(135deg, #0f172a 0%, #1a2744 50%, #0f172a 100%);
    border: 1px solid var(--border); border-radius: var(--radius); padding: 48px; margin-bottom: 48px;
  }}
  .rtk-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 32px; }}
  .rtk-card {{
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 24px;
  }}
  .rtk-card h4 {{ font-size: 0.95rem; font-weight: 700; margin-bottom: 12px; color: var(--accent-yellow); }}
  .rtk-card p, .rtk-card ul {{ font-size: 0.85rem; color: var(--text-secondary); line-height: 1.7; }}
  .rtk-card ul {{ list-style: none; padding: 0; }}
  .rtk-card ul li {{ padding: 3px 0 3px 16px; position: relative; }}
  .rtk-card ul li::before {{ content: '\\25B8'; position: absolute; left: 0; color: var(--accent-yellow); font-size: 0.7rem; top: 5px; }}
  .rtk-highlight {{
    display: inline-block; background: rgba(251,191,36,0.15); color: var(--accent-yellow);
    padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 0.82rem;
  }}
  .rtk-comparison {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 0.82rem; }}
  .rtk-comparison th {{
    background: rgba(251,191,36,0.1); color: var(--accent-yellow);
    padding: 10px 14px; text-align: left; font-weight: 600; border-bottom: 1px solid var(--border);
  }}
  .rtk-comparison td {{ padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text-secondary); }}
  .rtk-comparison tr:hover td {{ background: rgba(255,255,255,0.02); }}

  /* KEY NUMBERS */
  .key-numbers-standalone {{
    background: linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%);
    border-radius: var(--radius); padding: 40px; margin: 48px 0;
  }}
  .kn-label {{ font-size: 0.7rem; font-weight: 700; letter-spacing: 4px; color: var(--text-muted); text-transform: uppercase; text-align: center; margin-bottom: 28px; }}
  .kn-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
  .kn-card {{ text-align: center; padding: 24px 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }}
  .kn-value {{ font-size: 3rem; font-weight: 900; line-height: 1; margin-bottom: 8px; }}
  .kn-unit {{ font-size: 1.2rem; }}
  .kn-label-text {{ font-size: 0.85rem; color: var(--text-secondary); }}
  .kn-desc {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }}

  /* FOOTER */
  .site-footer {{ text-align: center; padding: 40px 2rem; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 0.8rem; }}

  /* LIGHTBOX */
  .lightbox {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.9); z-index: 1000; justify-content: center; align-items: center; cursor: zoom-out; }}
  .lightbox.active {{ display: flex; }}
  .lightbox img {{ max-width: 90vw; max-height: 90vh; border-radius: 8px; }}

  @media (max-width: 768px) {{
    .step-content {{ grid-template-columns: 1fr; }}
    .rtk-section {{ padding: 24px; }}
    .step-section {{ padding: 24px; }}
  }}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <span class="nav-brand">ESNav 5.0</span>
    <a href="#overview">概要</a>
    <a href="#steps">操作手順</a>
    <a href="#infographic">フローボード</a>
    <a href="#diagrams">技術図解</a>
    <a href="#rtk">ホクレンRTK</a>
    <a href="#qa">Q&A</a>
  </div>
</nav>

<header class="hero" id="top">
  <div class="hero-badge">LECTURE MATERIAL</div>
  <h1>ESNav 5.0 操作ガイド</h1>
  <p class="hero-sub">GPS自動操舵システム &mdash; 境界線・AB線・曲線の作成方法</p>
  <p class="hero-date">2026年2月24日 講習会資料</p>
</header>

<!-- OVERVIEW -->
<div class="section" id="overview">
  <div class="section-header">
    <span class="section-label">Overview</span>
    <h2 class="section-title">ESNav 5.0 とは</h2>
    <p class="section-desc">中国製GPS自動操舵システム。RTK-GNSS技術により&plusmn;2.5cmの高精度でトラクターを自動誘導します。</p>
  </div>
  <div class="overview-grid">
    <div class="overview-card">
      <span class="card-icon">&#x1F6F0;</span>
      <div class="card-title">RTK-GNSS</div>
      <div class="card-text">GPS + みちびき（準天頂衛星）の補正信号で&plusmn;2.5cm精度を実現</div>
    </div>
    <div class="overview-card">
      <span class="card-icon">&#x1F69C;</span>
      <div class="card-title">自動操舵</div>
      <div class="card-text">油圧モーターでハンドルを自動制御。オペレーターは作業機の操作に集中可能</div>
    </div>
    <div class="overview-card">
      <span class="card-icon">&#x1F4F1;</span>
      <div class="card-title">タッチ操作</div>
      <div class="card-text">タブレット端末で境界線・ガイドラインを簡単作成</div>
    </div>
    <div class="overview-card">
      <span class="card-icon">&#x1F4B0;</span>
      <div class="card-title">コスト削減</div>
      <div class="card-text">燃料費削減・作業効率UP・疲労軽減で2-3年で投資回収</div>
    </div>
  </div>
  <div class="key-numbers-standalone">
    <div class="kn-label">Key Numbers</div>
    <div class="kn-grid">
      <div class="kn-card">
        <div class="kn-value" style="color:#22c55e;">&plusmn;2.5<span class="kn-unit" style="color:#86efac;">cm</span></div>
        <div class="kn-label-text">GPS誘導精度</div>
        <div class="kn-desc">RTK-GNSSによる高精度自動操舵</div>
      </div>
      <div class="kn-card">
        <div class="kn-value" style="color:#fbbf24;">5<span class="kn-unit" style="color:#fcd34d;">Step</span></div>
        <div class="kn-label-text">操作ステップ</div>
        <div class="kn-desc">境界作成→記録→ガイドライン→確認→走行</div>
      </div>
      <div class="kn-card">
        <div class="kn-value" style="color:#ef4444;">2-3<span class="kn-unit" style="color:#fca5a5;">年</span></div>
        <div class="kn-label-text">投資回収期間</div>
        <div class="kn-desc">作業効率向上・燃料費削減で早期回収</div>
      </div>
      <div class="kn-card">
        <div class="kn-value" style="color:#a78bfa;">2<span class="kn-unit" style="color:#c4b5fd;">種</span></div>
        <div class="kn-label-text">ガイドラインタイプ</div>
        <div class="kn-desc">AB線（直線）と自由曲線（カーブ）</div>
      </div>
    </div>
  </div>
</div>

<!-- STEPS -->
<div class="section" id="steps">
  <div class="section-header">
    <span class="section-label">Step by Step</span>
    <h2 class="section-title">操作手順ガイド</h2>
    <p class="section-desc">ESNav 5.0 でガイドラインを作成し、自動走行を開始するまでの5ステップ</p>
  </div>

  <div class="step-section">
    <div class="step-badge s1">Step 1 &mdash; 境界線の作成</div>
    <div class="step-content">
      <div class="step-text">
        <h3>圃場の輪郭を登録する</h3>
        <ul>
          <li>圃場管理画面から <span class="step-key">「境界」タブ</span> を選択</li>
          <li><span class="step-key">「作成」</span> をタップして新規境界線を開始</li>
          <li>計画方法で境界線を左右どちらで引くか選択</li>
          <li><span class="step-key">「確認」</span> を押して境界作成モードに入る</li>
        </ul>
      </div>
      <div class="step-images">
        <img src="{img_slide3_1}" alt="境界線作成画面1" onclick="openLightbox(this)">
        <img src="{img_slide3_2}" alt="境界線作成画面2" onclick="openLightbox(this)">
      </div>
    </div>
  </div>

  <div class="step-section">
    <div class="step-badge s2">Step 2 &mdash; 境界線の記録</div>
    <div class="step-content">
      <div class="step-text">
        <h3>RECで走行記録する</h3>
        <ul>
          <li><span class="step-key">REC ボタン</span> を押して記録開始</li>
          <li>圃場の境界線に沿って走行（青いポイントが記録される）</li>
          <li>すべての辺を一周回る</li>
          <li><span class="step-key">緑のチェックマーク</span> で記録を保存</li>
        </ul>
      </div>
      <div class="step-images">
        <img src="{img_slide4}" alt="境界線記録画面" onclick="openLightbox(this)">
      </div>
    </div>
  </div>

  <div class="step-section">
    <div class="step-badge s3">Step 3 &mdash; ガイドラインの生成</div>
    <div class="step-content">
      <div class="step-text">
        <h3>A点・B点でガイドラインを作る</h3>
        <ul>
          <li><span class="step-key">A点</span> と <span class="step-key">B点</span> を選択</li>
          <li>タイプ選択: <span class="step-key">AB線</span>（直線）または <span class="step-key">自由曲線</span>（カーブ）</li>
          <li>ガイドラインの方向を選択（曲線の場合）</li>
          <li>オフセット距離（作業幅）を設定</li>
          <li>ラインの作成 &rarr; 作成画面終了</li>
        </ul>
      </div>
      <div class="step-images">
        <img src="{img_slide5}" alt="ガイドライン生成画面" onclick="openLightbox(this)">
      </div>
    </div>
  </div>

  <div class="step-section">
    <div class="step-badge s4">Step 4 &mdash; 線の確認</div>
    <div class="step-content">
      <div class="step-text">
        <h3>ガイドラインを確認する</h3>
        <ul>
          <li><span class="step-key">ガイドライン切り替えボタン</span> を押す</li>
          <li>作成したガイドラインが画面上に反映されていることを確認</li>
          <li>圃場管理 &rarr; ガイドラインからABラインの <span class="step-key">削除・編集</span> も可能</li>
        </ul>
      </div>
      <div class="step-images">
        <img src="{img_slide6}" alt="線の確認画面" onclick="openLightbox(this)">
      </div>
    </div>
  </div>

  <div class="step-section">
    <div class="step-badge s5">Step 5 &mdash; 自動操舵で走行</div>
    <div class="step-content">
      <div class="step-text">
        <h3>GPSに従い自動走行開始</h3>
        <ul>
          <li>ガイドラインに沿って <span class="step-key">自動でハンドルが操作</span> される</li>
          <li>オペレーターは作業機の操作に集中できる</li>
          <li>精度 <span class="step-key">&plusmn;2.5cm</span> の高精度走行</li>
          <li>ガイドラインからの逸脱時は警告音でお知らせ</li>
        </ul>
      </div>
      <div class="step-images">
        <img src="{img_slide1}" alt="ESNav 5.0 自動走行" onclick="openLightbox(this)">
      </div>
    </div>
  </div>
</div>

<!-- INFOGRAPHIC BOARD -->
<div class="section" id="infographic">
  <div class="section-header">
    <span class="section-label">Infographic</span>
    <h2 class="section-title">操作フロー付箋ボード</h2>
    <p class="section-desc">5ステップの操作手順を一覧できるインフォグラフィック</p>
  </div>
  <div class="infographic-wrap">
    {info_body}
  </div>
</div>

<!-- DIAGRAMS -->
<div class="section diagram-section" id="diagrams">
  <div class="section-header">
    <span class="section-label">Technical Diagrams</span>
    <h2 class="section-title">技術図解</h2>
    <p class="section-desc">操作フロー、RTK-GPS の仕組み、ガイドライン比較の3図</p>
  </div>
  {diag_combined}
</div>

<!-- HOKUREN RTK -->
<div class="section" id="rtk">
  <div class="section-header">
    <span class="section-label">Hokuren RTK</span>
    <h2 class="section-title">ホクレンRTK基地局サービス</h2>
    <p class="section-desc">北海道で利用可能なRTK補正データ配信サービスの概要と利用方法</p>
  </div>

  <div class="rtk-section">
    <h3 style="font-size:1.3rem;font-weight:700;margin-bottom:24px;color:var(--accent-yellow);">ホクレンRTKとは</h3>
    <p style="color:var(--text-secondary);margin-bottom:24px;font-size:0.9rem;">
      ホクレン農業協同組合連合会が北海道内の農家向けに提供するRTK-GNSS補正データ配信サービスです。
      北海道各地に設置された基地局から、Ntrip（Networked Transport of RTCM via Internet Protocol）方式で
      リアルタイム補正データを配信し、対応する自動操舵システムに&plusmn;2〜3cmの測位精度を提供します。
    </p>

    <div class="rtk-grid">
      <div class="rtk-card">
        <h4>サービス概要</h4>
        <ul>
          <li>北海道全域をカバーするRTK基地局ネットワーク</li>
          <li>Ntrip方式でインターネット経由の補正データ配信</li>
          <li>RTCM3.2フォーマット対応</li>
          <li>24時間365日の安定運用</li>
          <li>各JAを通じた契約・利用が可能</li>
        </ul>
      </div>
      <div class="rtk-card">
        <h4>利用に必要なもの</h4>
        <ul>
          <li>RTK対応GPS受信機（ESNav等の自動操舵システム）</li>
          <li>携帯電話回線（4G/LTE）によるインターネット接続</li>
          <li>Ntripクライアント設定（IP・ポート・マウントポイント）</li>
          <li>ホクレンとの利用契約</li>
          <li>SIMカード内蔵 or テザリング対応端末</li>
        </ul>
      </div>
      <div class="rtk-card">
        <h4>ESNavでの接続手順</h4>
        <ul>
          <li>ESNav設定画面 &rarr; <span class="rtk-highlight">補正データ</span> メニューを開く</li>
          <li>接続方式を <span class="rtk-highlight">Ntrip</span> に設定</li>
          <li>サーバーIP・ポート番号・マウントポイントを入力</li>
          <li>ユーザーID・パスワードを入力</li>
          <li><span class="rtk-highlight">接続</span> &rarr; RTK FIXステータスを確認</li>
        </ul>
      </div>
      <div class="rtk-card">
        <h4>精度と注意点</h4>
        <ul>
          <li>RTK FIX時: <span class="rtk-highlight">&plusmn;2〜3cm</span> の高精度</li>
          <li>FLOAT時は精度低下（&plusmn;30cm程度）</li>
          <li>基地局からの距離が離れると精度低下</li>
          <li>携帯電波の受信状況に依存</li>
          <li>山間部・谷間では精度が落ちる場合あり</li>
          <li>FIXに要する時間: 通常1〜3分</li>
        </ul>
      </div>
    </div>

    <h3 style="font-size:1.1rem;font-weight:700;margin:32px 0 16px;color:var(--accent-yellow);">RTK補正サービス比較</h3>
    <table class="rtk-comparison">
      <thead>
        <tr>
          <th>項目</th>
          <th>ホクレンRTK</th>
          <th>みちびきCLAS</th>
          <th>自前基地局</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>精度</td><td>&plusmn;2〜3cm</td><td>&plusmn;6〜12cm</td><td>&plusmn;1〜2cm</td></tr>
        <tr><td>月額費用</td><td>有（契約制）</td><td>無料</td><td>初期投資のみ</td></tr>
        <tr><td>通信環境</td><td>携帯電波必須</td><td>不要（衛星直受信）</td><td>UHF or WiFi</td></tr>
        <tr><td>カバーエリア</td><td>北海道全域</td><td>日本全国</td><td>半径10〜15km</td></tr>
        <tr><td>初期設定</td><td>Ntrip設定のみ</td><td>CLAS対応機が必要</td><td>基地局設置が必要</td></tr>
        <tr><td>安定性</td><td>電波状況に依存</td><td>天候に強い</td><td>近距離で安定</td></tr>
      </tbody>
    </table>

    <h3 style="font-size:1.1rem;font-weight:700;margin:32px 0 16px;color:var(--accent-yellow);">Ntrip接続の仕組み（図解）</h3>
    <div class="svg-wrap" style="background:var(--bg-secondary);border-radius:12px;border:1px solid var(--border);padding:1.5rem;">
      <svg viewBox="0 0 800 260" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrowR" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#fbbf24"/>
          </marker>
        </defs>
        <!-- 基地局 -->
        <rect x="20" y="60" width="160" height="80" rx="10" fill="#1e293b" stroke="#22c55e" stroke-width="2"/>
        <text x="100" y="95" text-anchor="middle" fill="#e2e8f0" font-size="13" font-weight="700">ホクレン基地局</text>
        <text x="100" y="115" text-anchor="middle" fill="#86efac" font-size="10">既知座標・補正算出</text>
        <line x1="100" y1="60" x2="100" y2="35" stroke="#86efac" stroke-width="2"/>
        <circle cx="100" cy="30" r="6" fill="#86efac"/>

        <!-- 矢印: 基地局→Ntripキャスター -->
        <line x1="182" y1="100" x2="268" y2="100" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrowR)"/>
        <text x="225" y="88" text-anchor="middle" fill="#94a3b8" font-size="9">RTCM3.2</text>

        <!-- Ntripキャスター -->
        <rect x="270" y="50" width="180" height="100" rx="10" fill="#1e293b" stroke="#fbbf24" stroke-width="2"/>
        <text x="360" y="85" text-anchor="middle" fill="#e2e8f0" font-size="13" font-weight="700">Ntripキャスター</text>
        <text x="360" y="105" text-anchor="middle" fill="#fde68a" font-size="10">インターネット配信</text>
        <text x="360" y="122" text-anchor="middle" fill="#94a3b8" font-size="9">IP:Port/MountPoint</text>

        <!-- 矢印: キャスター→受信機 -->
        <line x1="452" y1="100" x2="538" y2="100" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrowR)"/>
        <text x="495" y="88" text-anchor="middle" fill="#94a3b8" font-size="9">4G/LTE</text>

        <!-- トラクター受信機 -->
        <rect x="540" y="50" width="200" height="100" rx="10" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
        <text x="640" y="85" text-anchor="middle" fill="#e2e8f0" font-size="13" font-weight="700">ESNav 受信機</text>
        <text x="640" y="105" text-anchor="middle" fill="#93c5fd" font-size="10">Ntripクライアント内蔵</text>
        <text x="640" y="122" text-anchor="middle" fill="#86efac" font-size="10">RTK FIX → &plusmn;2cm</text>

        <!-- 下段ラベル -->
        <rect x="20" y="180" width="720" height="60" rx="8" fill="rgba(251,191,36,0.05)" stroke="rgba(251,191,36,0.2)" stroke-width="1"/>
        <text x="380" y="205" text-anchor="middle" fill="#fde68a" font-size="12" font-weight="600">設定に必要な情報</text>
        <text x="140" y="228" text-anchor="middle" fill="#94a3b8" font-size="10">サーバーIP</text>
        <text x="300" y="228" text-anchor="middle" fill="#94a3b8" font-size="10">ポート番号</text>
        <text x="460" y="228" text-anchor="middle" fill="#94a3b8" font-size="10">マウントポイント名</text>
        <text x="640" y="228" text-anchor="middle" fill="#94a3b8" font-size="10">ユーザーID / PW</text>
      </svg>
    </div>
  </div>
</div>

<!-- Q&A -->
<div class="section" id="qa">
  <div class="section-header">
    <span class="section-label">Q & A</span>
    <h2 class="section-title">よくある質問</h2>
  </div>
  <div class="overview-grid">
    <div class="overview-card">
      <div class="card-title">Q: 精度が出ないときは？</div>
      <div class="card-text">RTK FIXになっているか確認。FLOAT状態だと精度が低下します。携帯電波の受信状況と、基地局との距離を確認してください。</div>
    </div>
    <div class="overview-card">
      <div class="card-title">Q: AB線と自由曲線の使い分けは？</div>
      <div class="card-text">四角い圃場にはAB線（2点指定で簡単）、変形圃場や棚田にはカーブに追従する自由曲線がおすすめです。</div>
    </div>
    <div class="overview-card">
      <div class="card-title">Q: 作業幅の設定は？</div>
      <div class="card-text">使用する作業機の幅に合わせてオフセット距離を設定します。重なりが必要な場合は少し狭めに設定。</div>
    </div>
    <div class="overview-card">
      <div class="card-title">Q: ホクレンRTKの申込み方法は？</div>
      <div class="card-text">所属のJA（農協）を通じてホクレンに申し込みます。利用契約後にNtrip接続情報が発行されます。</div>
    </div>
  </div>
</div>

<footer class="site-footer">
  <p>ESNav 5.0 GPS自動操舵システム 講習会資料</p>
  <p style="margin-top:6px;">操作手順は実際の画面と多少異なる場合があります | 2026年2月24日</p>
</footer>

<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <img id="lightbox-img" src="" alt="">
</div>

<script>
function openLightbox(el) {{
  const lb = document.getElementById('lightbox');
  document.getElementById('lightbox-img').src = el.src;
  lb.classList.add('active');
}}
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('active');
}}
document.addEventListener('keydown', e => {{ if(e.key === 'Escape') closeLightbox(); }});
</script>

</body>
</html>'''

with open('esnav-lecture.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written: esnav-lecture.html ({len(html):,} chars)")
