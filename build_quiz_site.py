import json, os

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)

SUPABASE_URL = 'https://kqmshtjzosiurntxldrj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtxbXNodGp6b3NpdXJudHhsZHJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU1NjY1NjksImV4cCI6MjA5MTE0MjU2OX0.LqKom6FOfET9G22z52sbgq3ypUKga4RvSOOYWBtQVLk'

html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>國中國文練習 — 陋室銘・鳥・深藍的憂鬱・秋之味</title>
<style>
  :root {
    --bg: #f0f4f8;
    --card: #ffffff;
    --primary: #2563eb;
    --green: #16a34a;
    --red: #dc2626;
    --gray: #64748b;
    --dark: #1e293b;
    --border: #e2e8f0;
    --yellow: #fbbf24;
    --light-green: #dcfce7;
    --light-red: #fee2e2;
    --light-blue: #dbeafe;
    --purple: #9333ea;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: "微軟正黑體","Microsoft JhengHei",sans-serif; background: var(--bg); color: var(--dark); min-height: 100vh; }

  /* ===== LOGIN ===== */
  #login-screen { display:flex; flex-direction:column; align-items:center; min-height:100vh; padding:24px 16px 48px; }
  #login-screen > h1 { margin-top:40px; }

  /* ===== INFO SECTION ===== */
  #info-section { width:100%; max-width:680px; margin-top:40px; }
  .info-card { background:var(--card); border-radius:14px; padding:20px 22px; box-shadow:0 2px 10px rgba(0,0,0,0.06); margin-bottom:16px; }
  .info-card-title { font-size:16px; font-weight:700; color:#1d4ed8; margin-bottom:12px; padding-bottom:8px; border-bottom:2px solid #dbeafe; display:flex; align-items:center; gap:6px; }
  .info-body { font-size:13px; color:#334155; line-height:1.8; }
  .info-body li { margin-left:18px; margin-bottom:4px; }
  .score-formula-box { background:linear-gradient(135deg,#fef9c3,#fef3c7); border:2px solid #fbbf24; border-radius:10px; padding:12px 16px; text-align:center; margin:10px 0; }
  .score-formula-box .formula { font-size:18px; font-weight:900; color:#92400e; }
  .score-formula-box .example { font-size:12px; color:#b45309; margin-top:4px; }
  .evo-table { width:100%; border-collapse:collapse; font-size:13px; margin-top:6px; }
  .evo-table th { background:#1e40af; color:#fff; padding:8px 10px; text-align:center; }
  .evo-table td { padding:7px 10px; border-bottom:1px solid #e2e8f0; }
  .evo-table tr:nth-child(even) td { background:#f0f9ff; }
  .evo-table td:first-child { text-align:center; font-weight:700; }
  .evo-table td:nth-child(2) { text-align:center; font-size:18px; }
  .combo-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
  .combo-badge { background:#fff7ed; border:1px solid #fed7aa; border-radius:20px; padding:4px 12px; font-size:13px; font-weight:700; color:#c2410c; white-space:nowrap; }
  .combo-desc { font-size:13px; color:#334155; }
  #login-screen h1 { font-size:26px; font-weight:700; margin-bottom:6px; text-align:center; }
  #login-screen p.sub { color:var(--gray); margin-bottom:28px; text-align:center; font-size:14px; }
  #login-card { background:var(--card); border-radius:16px; padding:32px 28px; box-shadow:0 4px 24px rgba(0,0,0,0.08); width:100%; max-width:400px; }
  .login-label { display:block; font-size:13px; color:var(--gray); margin-bottom:6px; font-weight:600; }
  .login-input { width:100%; padding:12px 16px; font-size:16px; border:2px solid var(--border); border-radius:10px; font-family:inherit; outline:none; transition:border-color 0.2s; margin-bottom:12px; }
  .login-input:focus { border-color:var(--primary); }
  .login-btn { width:100%; padding:13px; background:var(--primary); color:white; border:none; border-radius:10px; font-size:15px; font-weight:700; cursor:pointer; font-family:inherit; transition:background 0.2s; }
  .login-btn:hover { background:#1d4ed8; }
  .login-btn:disabled { background:#94a3b8; cursor:default; }
  .login-btn.green { background:var(--green); }
  .login-btn.green:hover { background:#15803d; }
  .login-msg { margin-top:12px; padding:10px 14px; border-radius:8px; font-size:13px; display:none; }
  .login-msg.error { background:#fee2e2; color:var(--red); display:block; }
  .login-msg.info { background:var(--light-blue); color:var(--primary); display:block; }
  .login-back { background:none; border:none; color:var(--gray); font-size:13px; cursor:pointer; font-family:inherit; margin-top:10px; text-decoration:underline; }
  #login-step1, #login-step2 { }
  #login-step2 { display:none; }
  .step2-who { font-size:15px; font-weight:700; margin-bottom:16px; color:var(--dark); }

  /* ===== APP ===== */
  #app { display:none; }
  header { background:var(--dark); color:white; padding:10px 16px; display:flex; align-items:center; gap:10px; position:sticky; top:0; z-index:100; }
  header h2 { font-size:14px; font-weight:700; flex:1; }
  .user-badge { background:rgba(255,255,255,0.15); padding:4px 10px; border-radius:20px; font-size:12px; max-width:120px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .score-badge { background:var(--primary); padding:4px 10px; border-radius:20px; font-size:12px; font-weight:700; white-space:nowrap; }
  .evo-badge { padding:4px 10px; border-radius:20px; font-size:12px; font-weight:700; white-space:nowrap; background:rgba(255,255,255,0.18); }

  /* ===== COMBO TOAST ===== */
  #combo-toast { position:fixed; top:70px; left:50%; transform:translateX(-50%) translateY(-20px); background:linear-gradient(135deg,#f97316,#ef4444); color:#fff; font-size:18px; font-weight:900; padding:10px 28px; border-radius:999px; box-shadow:0 4px 20px rgba(239,68,68,0.5); z-index:9999; opacity:0; pointer-events:none; transition:opacity 0.3s, transform 0.3s; white-space:nowrap; }
  #combo-toast.show { opacity:1; transform:translateX(-50%) translateY(0); }

  /* ===== EVOLUTION OVERLAY ===== */
  #evo-overlay { position:fixed; inset:0; z-index:10000; display:flex; flex-direction:column; align-items:center; justify-content:center; background:radial-gradient(circle at center, #1e1b4b 0%, #0f172a 100%); opacity:0; pointer-events:none; transition:opacity 0.4s; }
  #evo-overlay.show { opacity:1; pointer-events:auto; }
  .evo-icon { font-size:100px; animation:evoBounce 0.6s ease; }
  .evo-label { font-size:14px; color:rgba(255,255,255,0.6); margin-top:16px; letter-spacing:2px; }
  .evo-name { font-size:42px; font-weight:900; color:#fff; margin-top:8px; text-shadow:0 0 30px rgba(251,191,36,0.8); }
  .evo-msg { font-size:16px; color:rgba(255,255,255,0.7); margin-top:12px; }
  @keyframes evoBounce { 0%{transform:scale(0.3) rotate(-15deg);opacity:0;} 60%{transform:scale(1.2) rotate(5deg);} 100%{transform:scale(1) rotate(0deg);opacity:1;} }
  @keyframes evoStar { 0%,100%{opacity:0;transform:scale(0);} 50%{opacity:1;transform:scale(1);} }
  .evo-stars { position:absolute; inset:0; overflow:hidden; pointer-events:none; }
  .evo-star { position:absolute; border-radius:50%; animation:evoStar 1.2s ease infinite; }
  .evo-tap-hint { margin-top:32px; font-size:13px; color:rgba(255,255,255,0.35); }

  /* ===== TIMER ===== */
  .timer-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
  .timer-bar-bg { flex:1; height:8px; background:var(--border); border-radius:4px; overflow:hidden; }
  .timer-bar-fill { height:100%; border-radius:4px; transition:width 1s linear, background 1s; }
  .timer-num { font-size:13px; font-weight:700; min-width:28px; text-align:right; }

  /* ===== TABS ===== */
  .tabs { display:flex; background:var(--card); border-bottom:1px solid var(--border); overflow-x:auto; scrollbar-width:none; }
  .tabs::-webkit-scrollbar { display:none; }
  .tab-btn { flex:1; min-width:fit-content; padding:11px 8px; border:none; background:none; font-family:inherit; font-size:12px; cursor:pointer; color:var(--gray); border-bottom:3px solid transparent; transition:all 0.2s; white-space:nowrap; }
  .tab-btn.active { color:var(--primary); border-bottom-color:var(--primary); font-weight:700; }
  .tab-btn.admin-tab { color:#7c3aed; }
  .tab-btn.admin-tab.active { color:#7c3aed; border-bottom-color:#7c3aed; }

  /* ===== ADMIN PANEL ===== */
  #tab-admin { display:none; }
  .admin-summary { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; padding:14px 12px 0; }
  .admin-stat { background:var(--card); border-radius:10px; padding:12px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
  .admin-stat-num { font-size:22px; font-weight:700; color:#7c3aed; }
  .admin-stat-label { font-size:11px; color:var(--gray); margin-top:2px; }
  .admin-table-wrap { padding:12px; overflow-x:auto; }
  .admin-table { width:100%; border-collapse:collapse; font-size:13px; min-width:500px; }
  .admin-table th { background:#f8fafc; padding:8px 10px; text-align:left; font-size:11px; color:var(--gray); border-bottom:2px solid var(--border); white-space:nowrap; }
  .admin-table td { padding:9px 10px; border-bottom:1px solid var(--border); vertical-align:middle; }
  .admin-table tr:hover td { background:#f8fafc; }
  .admin-del-btn { background:#fee2e2; color:#dc2626; border:none; border-radius:6px; padding:4px 10px; font-size:12px; cursor:pointer; font-family:inherit; font-weight:600; }
  .admin-del-btn:hover { background:#fca5a5; }
  .admin-acc-bar { display:inline-flex; align-items:center; gap:6px; }
  .admin-bar-bg { width:60px; height:5px; background:var(--border); border-radius:3px; overflow:hidden; display:inline-block; }
  .admin-bar-fill { height:5px; border-radius:3px; }

  /* ===== FILTER ===== */
  .filter-bar { padding:10px 12px; background:var(--card); border-bottom:1px solid var(--border); display:flex; gap:6px; overflow-x:auto; flex-wrap:nowrap; -webkit-overflow-scrolling:touch; scrollbar-width:none; }
  .filter-bar::-webkit-scrollbar { display:none; }
  .filter-btn { padding:6px 10px; border:2px solid var(--border); background:var(--bg); border-radius:20px; font-size:12px; cursor:pointer; font-family:inherit; color:var(--gray); transition:all 0.15s; font-weight:600; white-space:nowrap; flex-shrink:0; }
  .filter-btn.active { background:var(--primary); color:white; border-color:var(--primary); }

  /* ===== QUIZ ===== */
  main { padding:12px; max-width:800px; margin:0 auto; }
  .progress-bar { height:6px; background:var(--border); border-radius:3px; margin-bottom:6px; overflow:hidden; }
  .progress-fill { height:100%; background:var(--primary); border-radius:3px; transition:width 0.4s; }
  .progress-text { font-size:12px; color:var(--gray); text-align:right; margin-bottom:10px; }
  .question-card { background:var(--card); border-radius:14px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-bottom:12px; }
  .q-meta { display:flex; gap:8px; margin-bottom:10px; align-items:center; flex-wrap:wrap; }
  .q-num { font-size:12px; color:var(--gray); }
  .q-lesson-tag { background:var(--light-blue); color:var(--primary); padding:2px 8px; border-radius:20px; font-size:12px; font-weight:700; }
  .q-text { font-size:15px; line-height:1.7; color:var(--dark); margin-bottom:16px; white-space:pre-line; }
  .options { display:flex; flex-direction:column; gap:9px; }
  .opt-btn { display:flex; align-items:flex-start; gap:10px; padding:11px 13px; background:var(--bg); border:2px solid var(--border); border-radius:10px; cursor:pointer; text-align:left; font-family:inherit; font-size:14px; line-height:1.6; transition:all 0.15s; color:var(--dark); width:100%; touch-action:manipulation; -webkit-tap-highlight-color:transparent; }
  .opt-btn:hover:not([disabled]) { border-color:var(--primary); background:var(--light-blue); }
  .opt-letter { min-width:26px; height:26px; background:white; border:2px solid var(--border); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0; }
  .opt-btn.correct { border-color:var(--green); background:var(--light-green); }
  .opt-btn.correct .opt-letter { background:var(--green); border-color:var(--green); color:white; }
  .opt-btn.wrong { border-color:var(--red); background:var(--light-red); }
  .opt-btn.wrong .opt-letter { background:var(--red); border-color:var(--red); color:white; }
  .opt-btn[disabled] { cursor:default; }
  .explanation { margin-top:14px; padding:12px 14px; background:#fffbeb; border-left:4px solid var(--yellow); border-radius:0 8px 8px 0; font-size:13px; line-height:1.7; display:none; }
  .explanation.show { display:block; }
  .exp-title { font-weight:700; color:#92400e; margin-bottom:5px; font-size:12px; }
  #next-btn { width:100%; padding:13px; background:var(--green); color:white; border:none; border-radius:12px; font-size:15px; font-weight:700; cursor:pointer; font-family:inherit; display:none; transition:background 0.2s; margin-top:4px; position:sticky; bottom:12px; box-shadow:0 4px 16px rgba(22,163,74,0.3); touch-action:manipulation; }
  #next-btn:hover { background:#15803d; }
  #next-btn.show { display:block; }

  /* ===== WRONG LIST ===== */
  .section-wrap { padding:12px; max-width:800px; margin:0 auto; }
  .section-wrap h3 { font-size:15px; font-weight:700; margin-bottom:14px; }
  .wrong-item { background:var(--card); border-radius:12px; padding:14px; margin-bottom:10px; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .wrong-item-q { font-size:13px; line-height:1.6; margin-bottom:8px; }
  .wrong-item-ans { font-size:13px; color:var(--green); font-weight:700; }
  .wrong-item-exp { font-size:12px; color:var(--gray); margin-top:5px; line-height:1.6; }
  .no-data { text-align:center; color:var(--gray); padding:40px; font-size:15px; }

  /* ===== STATS ===== */
  .stats-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:14px; }
  .stat-card { background:var(--card); border-radius:12px; padding:14px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .stat-num { font-size:26px; font-weight:700; color:var(--primary); }
  .stat-label { font-size:11px; color:var(--gray); margin-top:3px; }
  .lesson-stat { background:var(--card); border-radius:12px; padding:13px; margin-bottom:9px; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .lesson-stat-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:7px; }
  .lesson-stat-bar { height:8px; background:var(--border); border-radius:4px; overflow:hidden; }
  .lesson-stat-fill { height:100%; border-radius:4px; transition:width 0.4s; }
  .reset-btn { width:100%; padding:11px; background:#fee2e2; color:var(--red); border:none; border-radius:10px; font-size:13px; font-weight:700; cursor:pointer; font-family:inherit; margin-top:14px; touch-action:manipulation; }

  /* ===== LEADERBOARD GAME STYLE ===== */
  .lb-bg { background:linear-gradient(160deg,#0f172a 0%,#1e293b 60%,#0f172a 100%); min-height:100%; padding:16px 14px 32px; }
  .lb-top-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }
  .lb-title { font-size:18px; font-weight:700; color:#fff; letter-spacing:1px; }
  .lb-refresh-btn { background:rgba(255,255,255,0.12); color:#cbd5e1; border:1px solid rgba(255,255,255,0.15); border-radius:20px; padding:5px 12px; font-size:12px; cursor:pointer; font-family:inherit; transition:background 0.2s; }
  .lb-refresh-btn:hover { background:rgba(255,255,255,0.2); }
  .lb-formula-pill { display:inline-block; background:rgba(147,51,234,0.2); border:1px solid rgba(147,51,234,0.4); color:#c4b5fd; border-radius:20px; padding:4px 12px; font-size:11px; margin-bottom:16px; }

  /* My rank banner */
  .my-banner { background:linear-gradient(135deg,#7c3aed,#4f46e5); border-radius:14px; padding:14px 16px; margin-bottom:16px; display:flex; align-items:center; gap:12px; box-shadow:0 4px 20px rgba(124,58,237,0.4); }
  .my-banner-icon { font-size:28px; }
  .my-banner-info { flex:1; }
  .my-banner-rank { font-size:13px; color:#c4b5fd; }
  .my-banner-score { font-size:22px; font-weight:700; color:#fff; }
  .my-banner-detail { font-size:11px; color:#a5b4fc; margin-top:2px; }

  /* Podium */
  .lb-podium { display:flex; align-items:flex-end; gap:8px; margin-bottom:16px; }
  .podium-card { flex:1; border-radius:16px; padding:14px 8px 12px; text-align:center; position:relative; animation:podiumIn 0.5s ease both; }
  .podium-card.p1 { background:linear-gradient(160deg,#f59e0b,#d97706); box-shadow:0 8px 24px rgba(245,158,11,0.5); padding-top:20px; }
  .podium-card.p2 { background:linear-gradient(160deg,#94a3b8,#64748b); box-shadow:0 6px 16px rgba(148,163,184,0.4); }
  .podium-card.p3 { background:linear-gradient(160deg,#cd7c3c,#92400e); box-shadow:0 6px 16px rgba(180,83,9,0.4); }
  .podium-crown { font-size:20px; position:absolute; top:-14px; left:50%; transform:translateX(-50%); }
  .podium-avatar { width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:700; color:#fff; margin:0 auto 6px; border:3px solid rgba(255,255,255,0.4); }
  .podium-name { font-size:12px; font-weight:700; color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; margin-bottom:4px; }
  .podium-score { font-size:20px; font-weight:700; color:#fff; }
  .podium-label { font-size:10px; color:rgba(255,255,255,0.7); }
  .podium-me-ring { box-shadow:0 0 0 3px #fff, 0 0 0 5px #7c3aed; }
  @keyframes podiumIn { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
  .podium-card.p1 { animation-delay:0.1s; }
  .podium-card.p2 { animation-delay:0.2s; }
  .podium-card.p3 { animation-delay:0.3s; }

  /* Rank list (4~10) */
  .lb-list { display:flex; flex-direction:column; gap:8px; }
  .lb-list-item { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:11px 14px; display:flex; align-items:center; gap:10px; animation:slideIn 0.4s ease both; }
  .lb-list-item.lb-me { background:rgba(79,70,229,0.25); border-color:rgba(129,140,248,0.5); }
  @keyframes slideIn { from { opacity:0; transform:translateX(20px); } to { opacity:1; transform:translateX(0); } }
  .lb-list-rank { min-width:28px; font-size:14px; font-weight:700; color:#64748b; text-align:center; }
  .lb-list-avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:700; color:#fff; flex-shrink:0; }
  .lb-list-name { flex:1; font-size:13px; font-weight:700; color:#e2e8f0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .lb-level { font-size:10px; padding:2px 7px; border-radius:10px; font-weight:700; margin-left:4px; }
  .lb-list-right { text-align:right; }
  .lb-list-score { font-size:17px; font-weight:700; color:#a78bfa; }
  .lb-list-detail { font-size:10px; color:#64748b; }
  .lb-loading { text-align:center; padding:40px; color:#64748b; font-size:14px; }

  /* ===== MODAL ===== */
  .modal-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:200; align-items:center; justify-content:center; padding:20px; }
  .modal-overlay.show { display:flex; }
  .modal { background:white; border-radius:16px; padding:24px 20px; max-width:340px; width:100%; text-align:center; }
  .modal-emoji { font-size:44px; margin-bottom:10px; }
  .modal-title { font-size:18px; font-weight:700; margin-bottom:6px; }
  .modal-sub { color:var(--gray); font-size:13px; margin-bottom:16px; }
  .modal-score { font-size:32px; font-weight:700; color:var(--primary); margin-bottom:4px; }
  .modal-btns { display:flex; gap:8px; }
  .modal-btn { flex:1; padding:11px; border:none; border-radius:10px; font-size:13px; font-weight:700; cursor:pointer; font-family:inherit; touch-action:manipulation; }
  .modal-btn.primary { background:var(--primary); color:white; }
  .modal-btn.secondary { background:var(--bg); color:var(--dark); }

  button { touch-action:manipulation; -webkit-tap-highlight-color:transparent; }

  @media (max-width:600px) {
    header { padding:10px 14px; gap:8px; }
    header h2 { display:none; }
    main { padding:10px; }
    .question-card { padding:14px; }
    .q-text { font-size:14px; }
    .opt-btn { font-size:13px; padding:10px 11px; }
    .section-wrap { padding:10px; }
    .stats-section { padding:10px; }
    .stat-num { font-size:22px; }
    #login-screen h1 { font-size:22px; }
    #login-card { padding:24px 18px; }
  }
  @media (max-width:360px) {
    .stat-num { font-size:19px; }
    .q-text { font-size:13px; }
    .opt-btn { font-size:12px; }
    .lb-score { font-size:15px; }
  }
</style>
</head>
<body>

<!-- ===== LOGIN ===== -->
<div id="login-screen">
  <h1>📖 國中國文練習</h1>
  <p class="sub">陋室銘・鳥・深藍的憂鬱・秋之味<br>共 200 題，附解析 · 積分排行榜</p>
  <div id="login-card">
    <!-- Step 1: 輸入暱稱 -->
    <div id="login-step1">
      <label class="login-label" for="nickname-input">暱稱</label>
      <input type="text" id="nickname-input" class="login-input" placeholder="例：小明、7年3班" maxlength="20" autocomplete="off">
      <button class="login-btn" id="step1-btn" onclick="step1Next()">繼續 →</button>
      <div id="step1-msg" class="login-msg"></div>
    </div>
    <!-- Step 2: 密碼 -->
    <div id="login-step2">
      <div class="step2-who" id="step2-who"></div>
      <label class="login-label" for="password-input" id="pw-label">密碼</label>
      <input type="password" id="password-input" class="login-input" placeholder="請輸入密碼" maxlength="30" autocomplete="off">
      <input type="password" id="password-confirm" class="login-input" placeholder="再輸入一次確認" maxlength="30" autocomplete="off" style="display:none">
      <button class="login-btn green" id="step2-btn" onclick="step2Submit()">登入</button>
      <div id="step2-msg" class="login-msg"></div>
      <button class="login-back" onclick="backToStep1()">← 換一個暱稱</button>
    </div>
  </div>

  <!-- 警示訊息 -->
  <div style="width:100%;max-width:400px;margin-top:14px;background:#fef2f2;border:2px solid #fca5a5;border-radius:12px;padding:14px 20px;text-align:center">
    <div style="font-size:17px;font-weight:900;color:#dc2626">⚠️ 不雅帳號會被刪除，不要亂取名喔！</div>
  </div>

  <!-- ===== 說明區塊 ===== -->
  <div id="info-section">

    <!-- 帳號與登入 -->
    <div class="info-card">
      <div class="info-card-title">🔐 帳號與登入</div>
      <div class="info-body">
        <ol>
          <li>首次使用請輸入自訂暱稱（建議用班號＋座號，例如：703-01）</li>
          <li>設定密碼（至少 4 個字元），下次以相同暱稱與密碼登入即可</li>
          <li>練習紀錄自動儲存至雲端，可跨裝置查看</li>
        </ol>
      </div>
    </div>

    <!-- 積分公式 -->
    <div class="info-card">
      <div class="info-card-title">🧮 積分計算公式</div>
      <div class="score-formula-box">
        <div class="formula">積分 ＝ 已作答題數 ＋ 正確率（%）</div>
        <div class="example">範例：答了 80 題、答對 60 題 → 正確率 75% → 積分 = 80 + 75 = 155 分</div>
      </div>
      <div class="info-body" style="margin-top:8px">💡 提升積分的關鍵是<strong>正確率</strong>，不只是多答題！</div>
      <div class="info-body" style="margin-top:6px;color:#dc2626">⚠️ 正確率低於 30% 時，積分折半計算。</div>
    </div>

    <!-- 排行榜 -->
    <div class="info-card">
      <div class="info-card-title">🏆 排行榜規則</div>
      <div class="info-body">
        <ol>
          <li>排行榜顯示全班積分前 10 名，每次作答後即時同步</li>
          <li>前三名顯示金銀銅獎台，並標示段位稱號</li>
          <li>可跨裝置查看排名，隨時掌握自己的名次</li>
        </ol>
      </div>
    </div>

    <!-- 進化段位 -->
    <div class="info-card">
      <div class="info-card-title">⚡ 進化段位系統（學者進化）</div>
      <div class="info-body" style="margin-bottom:10px">根據累積積分自動升級，升級時會出現進化動畫特效！🎉</div>
      <table class="evo-table">
        <tr><th>段位</th><th>圖示</th><th>所需積分</th><th>描述</th></tr>
        <tr><td>書蟲蛋</td><td>🥚</td><td>0–49 分</td><td>剛開始練習的新手</td></tr>
        <tr><td>小書蟲</td><td>🐛</td><td>50–99 分</td><td>已有基本答題能力</td></tr>
        <tr><td>閱讀蝶</td><td>🦋</td><td>100–149 分</td><td>答題正確率明顯提升</td></tr>
        <tr><td>文字師</td><td>📖</td><td>150–199 分</td><td>對課文有深入理解</td></tr>
        <tr><td>詩詞士</td><td>⚔️</td><td>200–249 分</td><td>達到高手程度</td></tr>
        <tr><td>文學龍</td><td>🐉</td><td>250 分以上</td><td>傳說中的文學王者！</td></tr>
      </table>
    </div>

    <!-- 連勝 Combo -->
    <div class="info-card">
      <div class="info-card-title">🔥 連勝獎勵（Combo）</div>
      <div class="info-body" style="margin-bottom:10px">連續答對題目可獲得連勝提示，答錯一題即重置！</div>
      <div class="combo-row"><span class="combo-badge">🔥 3 連勝</span><span class="combo-desc">連續答對 3 題</span></div>
      <div class="combo-row"><span class="combo-badge">🔥🔥 5 連勝</span><span class="combo-desc">連續答對 5 題</span></div>
      <div class="combo-row"><span class="combo-badge">🔥🔥🔥 10 連勝</span><span class="combo-desc">連續答對 10 題（最強！）</span></div>
    </div>

    <!-- 練習建議 -->
    <div class="info-card">
      <div class="info-card-title">📚 練習建議</div>
      <div class="info-body">
        <ul>
          <li>建議每天練習 20～30 題，養成習慣</li>
          <li>善用「錯題複習」功能，反覆練習弱點題目</li>
          <li>衝刺積分的關鍵是提高正確率，而非只追求題數</li>
          <li>登入後可隨時查看個人成績統計與各課文進度</li>
        </ul>
      </div>
    </div>

    <div style="text-align:center;color:#94a3b8;font-size:13px;margin-top:8px;padding-bottom:8px">🐉 目標：成為傳說中的文學龍！加油！</div>

  </div>
</div>

<!-- ===== APP ===== -->
<div id="app">
  <header>
    <h2>國文練習</h2>
    <span class="user-badge" id="user-badge">👤</span>
    <span class="evo-badge" id="evo-badge">🥚 書蟲蛋</span>
    <span class="score-badge" id="score-badge">✓ 0/0</span>
  </header>

  <!-- COMBO TOAST -->
  <div id="combo-toast">🔥 3 連勝！</div>

  <!-- EVOLUTION OVERLAY -->
  <div id="evo-overlay" onclick="closeEvoOverlay()">
    <div class="evo-stars" id="evo-stars"></div>
    <div class="evo-icon" id="evo-icon">🥚</div>
    <div class="evo-label">✨ 進化了！✨</div>
    <div class="evo-name" id="evo-name">書蟲蛋</div>
    <div class="evo-msg" id="evo-msg"></div>
    <div class="evo-tap-hint">點擊任意處繼續</div>
  </div>

  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('quiz')">📝 練習</button>
    <button class="tab-btn" onclick="switchTab('wrong')">❌ 錯題</button>
    <button class="tab-btn" onclick="switchTab('stats')">📊 成績</button>
    <button class="tab-btn" onclick="switchTab('rank')">🏆 排行榜</button>
    <button class="tab-btn admin-tab" id="admin-tab-btn" onclick="switchTab('admin')" style="display:none">🔑 管理</button>
  </div>

  <!-- QUIZ TAB -->
  <div id="tab-quiz">
    <div class="filter-bar">
      <button class="filter-btn active" onclick="setLesson('all')" data-lesson="all">全部</button>
      <button class="filter-btn" onclick="setLesson('陋室銘')" data-lesson="陋室銘">陋室銘</button>
      <button class="filter-btn" onclick="setLesson('鳥')" data-lesson="鳥">鳥</button>
      <button class="filter-btn" onclick="setLesson('深藍的憂鬱')" data-lesson="深藍的憂鬱">深藍的憂鬱</button>
      <button class="filter-btn" onclick="setLesson('秋之味')" data-lesson="秋之味">秋之味</button>
      <button class="filter-btn" onclick="setLesson('wrong')" data-lesson="wrong">🔁 錯題複習</button>
    </div>
    <main>
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-text" id="progress-text"></div>
      <div class="timer-row">
        <div class="timer-bar-bg"><div class="timer-bar-fill" id="timer-bar" style="width:100%;background:#22c55e"></div></div>
        <span class="timer-num" id="timer-num" style="color:#22c55e">60</span>
      </div>
      <div class="question-card">
        <div class="q-meta">
          <span class="q-num" id="q-num"></span>
          <span class="q-lesson-tag" id="q-lesson-tag"></span>
        </div>
        <div class="q-text" id="q-text"></div>
        <div class="options" id="options-container"></div>
        <div class="explanation" id="explanation-box">
          <div class="exp-title">📌 解析</div>
          <div id="explanation-text"></div>
        </div>
      </div>
      <button id="next-btn" onclick="nextQuestion()">下一題 →</button>
    </main>
  </div>

  <!-- WRONG TAB -->
  <div id="tab-wrong" style="display:none">
    <div class="section-wrap">
      <h3>❌ 錯題清單 <span id="wrong-count" style="color:var(--gray);font-size:13px;font-weight:400;"></span></h3>
      <div id="wrong-list"></div>
    </div>
  </div>

  <!-- STATS TAB -->
  <div id="tab-stats" style="display:none">
    <div class="section-wrap">
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-num" id="stat-correct">0</div><div class="stat-label">答對題數</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-answered">0</div><div class="stat-label">已作答</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-accuracy">—</div><div class="stat-label">正確率</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-wrong-n">0</div><div class="stat-label">錯題數</div></div>
      </div>
      <div id="lesson-stats"></div>
      <button class="reset-btn" onclick="confirmReset()">🗑️ 清除本機紀錄</button>
    </div>
  </div>

  <!-- ADMIN TAB -->
  <div id="tab-admin" style="display:none">
    <div class="admin-summary" id="admin-summary"></div>
    <div class="admin-table-wrap">
      <div id="admin-loading" style="text-align:center;padding:20px;color:var(--gray)">🔄 載入中…</div>
      <table class="admin-table" id="admin-table" style="display:none">
        <thead>
          <tr>
            <th>名次</th><th>暱稱</th><th>積分</th><th>作答</th><th>正確率</th><th>最後更新</th><th>操作</th>
          </tr>
        </thead>
        <tbody id="admin-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- RANK TAB -->
  <div id="tab-rank" style="display:none">
    <div class="lb-bg">
      <div class="lb-top-row">
        <div class="lb-title">🏆 積分排行榜</div>
        <button class="lb-refresh-btn" onclick="loadLeaderboard()">🔄 重整</button>
      </div>
      <div class="lb-formula-pill">積分 = 作答題數 + 正確率(%)</div>
      <div id="my-banner" class="my-banner" style="display:none">
        <div class="my-banner-icon" id="my-banner-icon">🎮</div>
        <div class="my-banner-info">
          <div class="my-banner-rank" id="my-banner-rank">我的名次</div>
          <div class="my-banner-score" id="my-banner-score">0 分</div>
          <div class="my-banner-detail" id="my-banner-detail"></div>
        </div>
      </div>
      <div id="lb-podium" class="lb-podium" style="display:none"></div>
      <div id="lb-list" class="lb-list"></div>
      <div id="lb-loading" class="lb-loading">🔄 載入中…</div>
    </div>
  </div>
</div>

<!-- COMPLETE MODAL -->
<div class="modal-overlay" id="complete-modal">
  <div class="modal">
    <div class="modal-emoji" id="modal-emoji">🎉</div>
    <div class="modal-title" id="modal-title">完成！</div>
    <div class="modal-score" id="modal-score"></div>
    <div class="modal-sub" id="modal-sub"></div>
    <div class="modal-btns">
      <button class="modal-btn secondary" onclick="closeModal()">查看錯題</button>
      <button class="modal-btn primary" onclick="restartLesson()">再練一次</button>
    </div>
  </div>
</div>

<script>
// ===== CONFIG =====
const SUPABASE_URL = 'SUPABASE_URL_PLACEHOLDER';
const SUPABASE_KEY = 'SUPABASE_KEY_PLACEHOLDER';
const ALL_QUESTIONS = QUESTIONS_PLACEHOLDER;

// ===== SUPABASE HELPERS =====
async function sbGet(table, params) {
  const url = new URL(SUPABASE_URL + '/rest/v1/' + table);
  if (params) Object.entries(params).forEach(function(e) { url.searchParams.set(e[0], e[1]); });
  const res = await fetch(url.toString(), {
    headers: { 'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY }
  });
  if (!res.ok) throw new Error('sb get error ' + res.status);
  return res.json();
}

async function sbPost(table, data, prefer) {
  const headers = {
    'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY,
    'Content-Type': 'application/json'
  };
  if (prefer) headers['Prefer'] = prefer;
  const res = await fetch(SUPABASE_URL + '/rest/v1/' + table, {
    method: 'POST', headers: headers, body: JSON.stringify(data)
  });
  return res;
}

async function sbUpsert(table, data) {
  return sbPost(table, data, 'resolution=merge-duplicates');
}

// ===== SHA-256 =====
async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(function(b){ return b.toString(16).padStart(2,'0'); }).join('');
}

// ===== STATE =====
let nickname = '';
let currentLesson = 'all';
let sessionPool = [];
let sessionIdx = 0;
let sessionCorrect = 0;
let currentQ = null;
let answered = false;
let syncTimer = null;
let streak = 0;
let lastEvoLevel = -1;
let timerCount = 60;
let timerInterval = null;
const TIMER_SEC = 60;

const KEY_STATS = 'cn_stats';
const KEY_WRONG = 'cn_wrong';
let stats = {};
let wrongSet = new Set();

function loadLocalStorage() {
  try {
    stats = JSON.parse(localStorage.getItem(KEY_STATS) || '{}');
    wrongSet = new Set(JSON.parse(localStorage.getItem(KEY_WRONG) || '[]'));
  } catch(e) { stats = {}; wrongSet = new Set(); }
}
function saveLocalStorage() {
  localStorage.setItem(KEY_STATS, JSON.stringify(stats));
  localStorage.setItem(KEY_WRONG, JSON.stringify([...wrongSet]));
}

// ===== SCORE FORMULA =====
function computeScore(totalAnswered, correctCount) {
  if (totalAnswered === 0) return 0;
  var accuracy = Math.round(correctCount / totalAnswered * 100);
  var score = totalAnswered + accuracy;
  if (accuracy < 30) score = Math.round(score / 2);
  return score;
}
function getTotals() {
  var total = 0, correct = 0;
  Object.values(stats).forEach(function(v){ total += v.correct + v.wrong; correct += v.correct; });
  return { total: total, correct: correct };
}

// ===== SYNC TO SUPABASE =====
async function syncScore() {
  if (!nickname) return;
  var t = getTotals();
  var score = computeScore(t.total, t.correct);
  try {
    await sbUpsert('cn_scores', {
      nickname: nickname,
      total_answered: t.total,
      correct_count: t.correct,
      score: score,
      updated_at: new Date().toISOString()
    });
  } catch(e) { /* silent fail */ }
}

function scheduleSync() {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(syncScore, 3000);
}

// ===== LOGIN FLOW =====
var loginMode = ''; // 'new' or 'existing'

window.onload = function() {
  document.getElementById('nickname-input').addEventListener('keydown', function(e){
    if(e.key==='Enter') step1Next();
  });
  document.getElementById('password-input').addEventListener('keydown', function(e){
    if(e.key==='Enter') step2Submit();
  });
  document.getElementById('password-confirm').addEventListener('keydown', function(e){
    if(e.key==='Enter') step2Submit();
  });
};

async function step1Next() {
  var name = document.getElementById('nickname-input').value.trim();
  if (!name) { document.getElementById('nickname-input').focus(); return; }
  var btn = document.getElementById('step1-btn');
  var msg = document.getElementById('step1-msg');
  btn.disabled = true;
  btn.textContent = '查詢中…';
  msg.className = 'login-msg';
  msg.style.display = 'none';
  try {
    var rows = await sbGet('cn_users', { 'nickname': 'eq.' + name, 'select': 'nickname' });
    if (rows.length === 0) {
      // 新用戶
      loginMode = 'new';
      document.getElementById('step2-who').textContent = '👋 「' + name + '」是新帳號，請設定密碼';
      document.getElementById('pw-label').textContent = '設定密碼';
      document.getElementById('password-confirm').style.display = 'block';
      document.getElementById('step2-btn').textContent = '建立帳號';
    } else {
      // 既有用戶
      loginMode = 'existing';
      document.getElementById('step2-who').textContent = '👤 歡迎回來，' + name + '！';
      document.getElementById('pw-label').textContent = '輸入密碼';
      document.getElementById('password-confirm').style.display = 'none';
      document.getElementById('step2-btn').textContent = '登入';
    }
    document.getElementById('login-step1').style.display = 'none';
    document.getElementById('login-step2').style.display = 'block';
    document.getElementById('password-input').value = '';
    document.getElementById('password-confirm').value = '';
    document.getElementById('step2-msg').className = 'login-msg';
    document.getElementById('step2-msg').style.display = 'none';
    setTimeout(function(){ document.getElementById('password-input').focus(); }, 100);
  } catch(e) {
    msg.textContent = '⚠️ 網路錯誤，請稍後再試';
    msg.className = 'login-msg error';
  }
  btn.disabled = false;
  btn.textContent = '繼續 →';
}

async function step2Submit() {
  var name = document.getElementById('nickname-input').value.trim();
  var pw = document.getElementById('password-input').value;
  var pw2 = document.getElementById('password-confirm').value;
  var msg = document.getElementById('step2-msg');
  var btn = document.getElementById('step2-btn');

  if (!pw) { document.getElementById('password-input').focus(); return; }

  if (loginMode === 'new') {
    if (pw !== pw2) {
      msg.textContent = '❌ 兩次密碼不一致，請重新輸入';
      msg.className = 'login-msg error';
      return;
    }
    if (pw.length < 4) {
      msg.textContent = '❌ 密碼至少需要 4 個字元';
      msg.className = 'login-msg error';
      return;
    }
  }

  btn.disabled = true;
  btn.textContent = loginMode === 'new' ? '建立中…' : '驗證中…';
  msg.className = 'login-msg';
  msg.style.display = 'none';

  try {
    var hash = await sha256(pw);
    if (loginMode === 'new') {
      var res = await sbPost('cn_users', { nickname: name, password_hash: hash });
      if (!res.ok) {
        var body = await res.json();
        if (body.code === '23505') {
          msg.textContent = '❌ 這個暱稱已被使用，請換一個';
        } else {
          msg.textContent = '❌ 建立失敗，請稍後再試';
        }
        msg.className = 'login-msg error';
        btn.disabled = false;
        btn.textContent = '建立帳號';
        return;
      }
    } else {
      var rows = await sbGet('cn_users', { 'nickname': 'eq.' + name, 'select': 'password_hash' });
      if (rows.length === 0 || rows[0].password_hash !== hash) {
        msg.textContent = '❌ 密碼錯誤，請再試一次';
        msg.className = 'login-msg error';
        btn.disabled = false;
        btn.textContent = '登入';
        return;
      }
    }
    enterApp(name);
  } catch(e) {
    msg.textContent = '⚠️ 網路錯誤，請稍後再試';
    msg.className = 'login-msg error';
    btn.disabled = false;
    btn.textContent = loginMode === 'new' ? '建立帳號' : '登入';
  }
}

function backToStep1() {
  document.getElementById('login-step1').style.display = 'block';
  document.getElementById('login-step2').style.display = 'none';
}

function enterApp(name) {
  nickname = name;
  loadLocalStorage();
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  document.getElementById('user-badge').textContent = '👤 ' + nickname;
  setLesson('all');
  updateScoreBadge();
  // 初始化進化等級（不觸發動畫）
  var t = getTotals();
  lastEvoLevel = getEvolution(computeScore(t.total, t.correct)).level;
  // 管理員 Tab（僅 piliwu）
  if (name === 'piliwu') {
    document.getElementById('admin-tab-btn').style.display = '';
  }
}

// ===== QUIZ =====
function setLesson(lesson) {
  currentLesson = lesson;
  document.querySelectorAll('.filter-btn').forEach(function(b){
    b.classList.toggle('active', b.dataset.lesson === lesson);
  });
  buildPool();
  sessionIdx = 0; sessionCorrect = 0;
  showQuestion();
}

function buildPool() {
  var pool;
  if (currentLesson === 'all') pool = ALL_QUESTIONS.slice();
  else if (currentLesson === 'wrong') pool = ALL_QUESTIONS.filter(function(q){ return wrongSet.has(q.id); });
  else pool = ALL_QUESTIONS.filter(function(q){ return q.lesson === currentLesson; });
  for (var i = pool.length-1; i > 0; i--) {
    var j = Math.floor(Math.random()*(i+1));
    var tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp;
  }
  sessionPool = pool;
}

function showQuestion() {
  if (sessionPool.length === 0) {
    document.getElementById('q-text').innerHTML = currentLesson === 'wrong'
      ? '<span style="color:var(--green)">🎉 目前沒有錯題！</span>'
      : '<span style="color:var(--gray)">沒有題目</span>';
    document.getElementById('q-num').textContent = '';
    document.getElementById('q-lesson-tag').textContent = '';
    document.getElementById('options-container').innerHTML = '';
    document.getElementById('explanation-box').classList.remove('show');
    document.getElementById('next-btn').classList.remove('show');
    document.getElementById('progress-text').textContent = '';
    document.getElementById('progress-fill').style.width = '0%';
    return;
  }
  if (sessionIdx >= sessionPool.length) { showCompleteModal(); return; }

  answered = false;
  currentQ = sessionPool[sessionIdx];
  var total = sessionPool.length;
  document.getElementById('progress-fill').style.width = Math.round(sessionIdx/total*100) + '%';
  document.getElementById('progress-text').textContent = '第 ' + (sessionIdx+1) + ' / ' + total + ' 題';
  document.getElementById('q-num').textContent = '題目 #' + currentQ.id;
  document.getElementById('q-lesson-tag').textContent = currentQ.lesson;
  document.getElementById('q-text').textContent = currentQ.question;

  var container = document.getElementById('options-container');
  container.innerHTML = '';
  ['A','B','C','D'].forEach(function(letter) {
    var text = currentQ.options[letter];
    if (!text) return;
    var btn = document.createElement('button');
    btn.className = 'opt-btn';
    btn.innerHTML = '<span class="opt-letter">' + letter + '</span><span>' + escHtml(text) + '</span>';
    btn.addEventListener('click', function(){ selectOption(letter, btn); });
    container.appendChild(btn);
  });
  document.getElementById('explanation-box').classList.remove('show');
  document.getElementById('next-btn').classList.remove('show');
  startTimer();
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function selectOption(letter, btn) {
  if (answered) return;
  answered = true;
  clearTimer();
  var correct = currentQ.answer;
  var isCorrect = letter === correct;
  document.querySelectorAll('.opt-btn').forEach(function(b) {
    b.disabled = true;
    var l = b.querySelector('.opt-letter').textContent;
    if (l === correct) b.classList.add('correct');
    if (l === letter && !isCorrect) b.classList.add('wrong');
  });
  if (!stats[currentQ.id]) stats[currentQ.id] = {correct:0, wrong:0};
  if (isCorrect) {
    stats[currentQ.id].correct++;
    wrongSet.delete(currentQ.id);
    sessionCorrect++;
    streak++;
    if (streak === 3 || streak === 5 || streak === 10 || (streak > 10 && streak % 5 === 0)) {
      showComboToast(streak);
    }
  } else {
    stats[currentQ.id].wrong++;
    wrongSet.add(currentQ.id);
    streak = 0;
  }
  saveLocalStorage();
  updateScoreBadge();
  checkEvoChange();
  scheduleSync();
  if (currentQ.explanation) {
    document.getElementById('explanation-text').textContent = currentQ.explanation;
    document.getElementById('explanation-box').classList.add('show');
  }
  document.getElementById('next-btn').classList.add('show');
}

// ===== TIMER =====
function startTimer() {
  clearTimer();
  timerCount = TIMER_SEC;
  updateTimerUI();
  timerInterval = setInterval(function() {
    timerCount--;
    updateTimerUI();
    if (timerCount <= 0) {
      clearTimer();
      if (!answered) timeUp();
    }
  }, 1000);
}
function clearTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}
function updateTimerUI() {
  var pct = timerCount / TIMER_SEC * 100;
  var color = timerCount > 30 ? '#22c55e' : timerCount > 10 ? '#f97316' : '#ef4444';
  var bar = document.getElementById('timer-bar');
  var num = document.getElementById('timer-num');
  if (bar) { bar.style.width = pct + '%'; bar.style.background = color; }
  if (num) { num.textContent = timerCount; num.style.color = color; }
}
function timeUp() {
  if (answered) return;
  answered = true;
  var correct = currentQ.answer;
  document.querySelectorAll('.opt-btn').forEach(function(b) {
    b.disabled = true;
    if (b.querySelector('.opt-letter').textContent === correct) b.classList.add('correct');
  });
  if (!stats[currentQ.id]) stats[currentQ.id] = {correct:0, wrong:0};
  stats[currentQ.id].wrong++;
  wrongSet.add(currentQ.id);
  streak = 0;
  saveLocalStorage();
  updateScoreBadge();
  checkEvoChange();
  scheduleSync();
  if (currentQ.explanation) {
    document.getElementById('explanation-text').textContent = '⏰ 時間到！' + currentQ.explanation;
    document.getElementById('explanation-box').classList.add('show');
  }
  document.getElementById('next-btn').classList.add('show');
}

function nextQuestion() { sessionIdx++; showQuestion(); }

function getEvolution(score) {
  if (score >= 250) return {level:5, icon:'🐉', name:'文學龍',  color:'#fbbf24', bg:'rgba(251,191,36,0.2)'};
  if (score >= 200) return {level:4, icon:'⚔️', name:'詩詞士',  color:'#a855f7', bg:'rgba(168,85,247,0.2)'};
  if (score >= 150) return {level:3, icon:'📖', name:'文字師',  color:'#3b82f6', bg:'rgba(59,130,246,0.2)'};
  if (score >= 100) return {level:2, icon:'🦋', name:'閱讀蝶',  color:'#22c55e', bg:'rgba(34,197,94,0.2)'};
  if (score >= 50)  return {level:1, icon:'🐛', name:'小書蟲',  color:'#f97316', bg:'rgba(249,115,22,0.2)'};
  return                       {level:0, icon:'🥚', name:'書蟲蛋',  color:'#94a3b8', bg:'rgba(148,163,184,0.2)'};
}

function updateScoreBadge() {
  var t = getTotals();
  document.getElementById('score-badge').textContent = '✓ ' + t.correct + '/' + t.total;
  var sc = computeScore(t.total, t.correct);
  var evo = getEvolution(sc);
  var badge = document.getElementById('evo-badge');
  badge.textContent = evo.icon + ' ' + evo.name;
  badge.style.color = evo.color;
}

function checkEvoChange() {
  var t = getTotals();
  var sc = computeScore(t.total, t.correct);
  var evo = getEvolution(sc);
  if (evo.level > lastEvoLevel && lastEvoLevel !== -1) {
    showEvoOverlay(evo);
  }
  lastEvoLevel = evo.level;
}

// ===== COMBO TOAST =====
var comboToastTimer = null;
function showComboToast(n) {
  var el = document.getElementById('combo-toast');
  var emoji = n >= 10 ? '🔥🔥🔥' : n >= 5 ? '🔥🔥' : '🔥';
  el.textContent = emoji + ' ' + n + ' 連勝！';
  el.classList.add('show');
  clearTimeout(comboToastTimer);
  comboToastTimer = setTimeout(function() { el.classList.remove('show'); }, 1800);
}

// ===== EVOLUTION OVERLAY =====
function showEvoOverlay(evo) {
  document.getElementById('evo-icon').textContent = evo.icon;
  document.getElementById('evo-name').textContent = evo.name;
  document.getElementById('evo-msg').textContent = '恭喜升級！繼續努力！';
  // generate stars
  var stars = document.getElementById('evo-stars');
  stars.innerHTML = '';
  var colors = ['#fbbf24','#f472b6','#60a5fa','#34d399','#a78bfa'];
  for (var i = 0; i < 20; i++) {
    var s = document.createElement('div');
    s.className = 'evo-star';
    var size = Math.random() * 10 + 4;
    s.style.cssText = 'width:' + size + 'px;height:' + size + 'px;left:' + Math.random()*100 + '%;top:' + Math.random()*100 + '%;background:' + colors[i%colors.length] + ';animation-delay:' + (Math.random()*1.2) + 's;animation-duration:' + (0.8+Math.random()*0.8) + 's;';
    stars.appendChild(s);
  }
  var overlay = document.getElementById('evo-overlay');
  overlay.style.background = 'radial-gradient(circle at center, ' + (evo.level >= 4 ? '#451a03' : evo.level >= 3 ? '#1e1b4b' : '#042f2e') + ' 0%, #0f172a 100%)';
  overlay.classList.add('show');
}
function closeEvoOverlay() {
  document.getElementById('evo-overlay').classList.remove('show');
}

// ===== COMPLETE MODAL =====
function showCompleteModal() {
  var total = sessionPool.length;
  var pct = Math.round(sessionCorrect/total*100);
  var emoji = pct>=90?'🏆':pct>=70?'🎉':pct>=50?'💪':'📚';
  var msg = pct>=90?'太厲害了！':pct>=70?'不錯唷！':pct>=50?'繼續加油！':'多練習就會進步！';
  var label = currentLesson==='all'?'全部題目':currentLesson==='wrong'?'錯題複習':currentLesson;
  document.getElementById('modal-emoji').textContent = emoji;
  document.getElementById('modal-title').textContent = label + ' 完成！';
  document.getElementById('modal-score').textContent = sessionCorrect + ' / ' + total;
  document.getElementById('modal-sub').textContent = '正確率 ' + pct + '% — ' + msg;
  document.getElementById('complete-modal').classList.add('show');
  syncScore();
}
function closeModal() { document.getElementById('complete-modal').classList.remove('show'); switchTab('wrong'); }
function restartLesson() { document.getElementById('complete-modal').classList.remove('show'); setLesson(currentLesson); }

// ===== TABS =====
function switchTab(tab) {
  var allTabs = ['quiz','wrong','stats','rank','admin'];
  allTabs.forEach(function(t){
    document.getElementById('tab-'+t).style.display = t===tab?'block':'none';
  });
  document.querySelectorAll('.tab-btn').forEach(function(b){
    var tid = b.getAttribute('onclick').match(/'(\w+)'/);
    if (tid) b.classList.toggle('active', tid[1]===tab);
  });
  if (tab==='wrong') renderWrongList();
  if (tab==='stats') renderStats();
  if (tab==='rank') { syncScore(); loadLeaderboard(); }
  if (tab==='admin') loadAdminPanel();
}

// ===== ADMIN PANEL =====
async function loadAdminPanel() {
  document.getElementById('admin-loading').style.display = 'block';
  document.getElementById('admin-table').style.display = 'none';
  document.getElementById('admin-summary').innerHTML = '';
  try {
    var rows = await sbGet('cn_scores', { order:'score.desc', select:'nickname,total_answered,correct_count,score,updated_at' });
    document.getElementById('admin-loading').style.display = 'none';
    var active = rows.filter(function(r){ return r.total_answered > 0; });
    var avgAcc = active.length ? Math.round(active.reduce(function(s,r){ return s + (r.total_answered>0?r.correct_count/r.total_answered:0); },0)/active.length*100) : 0;
    document.getElementById('admin-summary').innerHTML =
      '<div class="admin-stat"><div class="admin-stat-num">' + rows.length + '</div><div class="admin-stat-label">帳號總數</div></div>' +
      '<div class="admin-stat"><div class="admin-stat-num">' + active.length + '</div><div class="admin-stat-label">有作答人數</div></div>' +
      '<div class="admin-stat"><div class="admin-stat-num">' + avgAcc + '%</div><div class="admin-stat-label">平均正確率</div></div>';
    var tbody = document.getElementById('admin-tbody');
    tbody.innerHTML = '';
    rows.forEach(function(row, i) {
      var acc = row.total_answered > 0 ? Math.round(row.correct_count/row.total_answered*100) : null;
      var date = row.updated_at ? row.updated_at.slice(0,10) : '-';
      var accColor = acc === null ? '#94a3b8' : acc >= 60 ? '#16a34a' : acc >= 40 ? '#f97316' : '#dc2626';
      var tr = document.createElement('tr');
      tr.innerHTML = '<td>' + (i+1) + '</td>'
        + '<td style="font-weight:600">' + escHtml(row.nickname) + '</td>'
        + '<td style="font-weight:700;color:#7c3aed">' + Math.round(row.score) + '</td>'
        + '<td>' + row.total_answered + '</td>'
        + '<td><div class="admin-acc-bar"><span style="color:' + accColor + ';font-weight:600;min-width:36px">' + (acc!==null?acc+'%':'—') + '</span><span class="admin-bar-bg"><span class="admin-bar-fill" style="width:' + (acc||0) + '%;background:' + accColor + '"></span></span></div></td>'
        + '<td style="color:#94a3b8;font-size:12px">' + date + '</td>'
        + '<td><button class="admin-del-btn">刪除</button></td>';
      var delBtn = tr.querySelector('.admin-del-btn');
      delBtn.dataset.name = row.nickname;
      delBtn.addEventListener('click', function(){ adminDelete(this.dataset.name, this); });
      tbody.appendChild(tr);
    });
    document.getElementById('admin-table').style.display = 'table';
  } catch(e) {
    document.getElementById('admin-loading').textContent = '⚠️ 載入失敗，請稍後再試';
  }
}

async function adminDelete(name, btn) {
  if (!confirm('確定刪除「' + name + '」的帳號與成績？')) return;
  btn.disabled = true;
  btn.textContent = '刪除中…';
  try {
    await sbDelete('cn_scores', 'nickname=eq.' + encodeURIComponent(name));
    await sbDelete('cn_users', 'nickname=eq.' + encodeURIComponent(name));
    btn.closest('tr').remove();
    loadAdminPanel();
  } catch(e) {
    btn.disabled = false;
    btn.textContent = '刪除';
    alert('刪除失敗，請重試');
  }
}

async function sbDelete(table, filter) {
  var res = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?' + filter, {
    method: 'DELETE',
    headers: { 'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY, 'Prefer': 'return=representation' }
  });
  if (!res.ok) throw new Error('delete error ' + res.status);
  return res.json();
}

// ===== WRONG LIST =====
function renderWrongList() {
  var container = document.getElementById('wrong-list');
  var wrongQs = ALL_QUESTIONS.filter(function(q){ return wrongSet.has(q.id); });
  document.getElementById('wrong-count').textContent = '（' + wrongQs.length + ' 題）';
  if (wrongQs.length === 0) { container.innerHTML = '<div class="no-data">🎉 太棒了！目前沒有錯題</div>'; return; }
  container.innerHTML = wrongQs.map(function(q) {
    var exp = q.explanation ? q.explanation.slice(0,150) + (q.explanation.length>150?'…':'') : '';
    return '<div class="wrong-item">'
      + '<div class="q-meta" style="margin-bottom:7px"><span class="q-num" style="font-size:11px">#' + q.id + '</span><span class="q-lesson-tag">' + q.lesson + '</span></div>'
      + '<div class="wrong-item-q">' + escHtml(q.question) + '</div>'
      + '<div class="wrong-item-ans">✓ 正確答案：(' + q.answer + ') ' + escHtml(q.options[q.answer]||'') + '</div>'
      + (exp ? '<div class="wrong-item-exp">📌 ' + escHtml(exp) + '</div>' : '')
      + '</div>';
  }).join('');
}

// ===== STATS =====
function renderStats() {
  var t = getTotals();
  document.getElementById('stat-correct').textContent = t.correct;
  document.getElementById('stat-answered').textContent = t.total;
  document.getElementById('stat-accuracy').textContent = t.total > 0 ? Math.round(t.correct/t.total*100)+'%' : '—';
  document.getElementById('stat-wrong-n').textContent = wrongSet.size;
  var lessons = ['陋室銘','鳥','深藍的憂鬱','秋之味'];
  var colors = {'陋室銘':'#2563eb','鳥':'#16a34a','深藍的憂鬱':'#9333ea','秋之味':'#ea580c'};
  document.getElementById('lesson-stats').innerHTML = lessons.map(function(lesson) {
    var qs = ALL_QUESTIONS.filter(function(q){return q.lesson===lesson;});
    var c = 0, tot = 0;
    qs.forEach(function(q){ if(stats[q.id]){ c+=stats[q.id].correct; tot+=stats[q.id].correct+stats[q.id].wrong; } });
    var pct = tot>0?Math.round(c/tot*100):0;
    return '<div class="lesson-stat">'
      + '<div class="lesson-stat-row"><span style="font-weight:700;color:' + colors[lesson] + '">' + lesson + '</span>'
      + '<span style="font-size:12px;color:var(--gray)">' + c + '/' + tot + ' 題・' + (tot>0?pct+'%':'未作答') + '</span></div>'
      + '<div class="lesson-stat-bar"><div class="lesson-stat-fill" style="width:' + pct + '%;background:' + colors[lesson] + '"></div></div></div>';
  }).join('');
}

// ===== LEADERBOARD GAME STYLE =====
function nicknameColor(name) {
  var palette = ['#ef4444','#f97316','#eab308','#22c55e','#06b6d4','#3b82f6','#8b5cf6','#ec4899','#14b8a6','#f43f5e'];
  var h = 0;
  for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffffffff;
  return palette[Math.abs(h) % palette.length];
}
function getLevel(score) {
  var e = getEvolution(score);
  return {name: e.icon + e.name, color: e.color, bg: e.bg};
}
function avatarEl(name, size, extraClass) {
  var color = nicknameColor(name);
  var ch = name.charAt(0);
  return '<div class="' + (extraClass||'lb-list-avatar') + '" style="background:' + color + ';width:' + size + 'px;height:' + size + 'px;font-size:' + Math.round(size*0.42) + 'px">' + ch + '</div>';
}
function animScore(el, target) {
  var start = 0, dur = 800, begin = performance.now();
  function step(now) {
    var t = Math.min((now - begin) / dur, 1);
    var ease = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(ease * target);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

async function loadLeaderboard() {
  document.getElementById('lb-loading').style.display = 'block';
  document.getElementById('lb-podium').style.display = 'none';
  document.getElementById('lb-list').innerHTML = '';
  document.getElementById('my-banner').style.display = 'none';
  try {
    var rows = await sbGet('cn_scores', { 'order': 'score.desc', 'limit': '10', 'select': 'nickname,total_answered,correct_count,score' });
    document.getElementById('lb-loading').style.display = 'none';

    if (rows.length === 0) {
      document.getElementById('lb-list').innerHTML = '<div class="lb-loading" style="display:block">還沒有人上榜，快去練習！</div>';
      return;
    }

    // Find my rank across all
    var allRows = await sbGet('cn_scores', { 'order': 'score.desc', 'select': 'nickname,score,total_answered,correct_count' });
    var myIdx = allRows.findIndex(function(r){ return r.nickname === nickname; });
    if (myIdx !== -1) {
      var me = allRows[myIdx];
      var myAcc = me.total_answered > 0 ? Math.round(me.correct_count/me.total_answered*100) : 0;
      var rankIcons = ['🥇','🥈','🥉'];
      var rankLabel = myIdx < 3 ? rankIcons[myIdx] + ' 第 ' + (myIdx+1) + ' 名' : '第 ' + (myIdx+1) + ' 名';
      var lv = getLevel(Math.round(me.score));
      document.getElementById('my-banner').style.display = 'flex';
      document.getElementById('my-banner-icon').textContent = myIdx===0?'👑':myIdx===1?'🥈':myIdx===2?'🥉':'🎮';
      document.getElementById('my-banner-rank').textContent = rankLabel + '  ·  ' + lv.name;
      var scoreEl = document.getElementById('my-banner-score');
      scoreEl.textContent = '0 分';
      animScore(scoreEl, Math.round(me.score));
      scoreEl.textContent += ' '; // trick: animScore will overwrite, add suffix after
      document.getElementById('my-banner-detail').textContent = '作答 ' + me.total_answered + ' 題 · 正確率 ' + myAcc + '%';
      // re-attach suffix after animation
      setTimeout(function(){ document.getElementById('my-banner-score').textContent = Math.round(me.score) + ' 分'; }, 850);
    }

    // Podium (top 3)
    var top3 = rows.slice(0, Math.min(3, rows.length));
    var podiumOrder = top3.length >= 3 ? [top3[1], top3[0], top3[2]] : top3.length === 2 ? [top3[1], top3[0]] : [top3[0]];
    var pClasses = top3.length >= 3 ? ['p2','p1','p3'] : top3.length === 2 ? ['p2','p1'] : ['p1'];
    var pLabels = top3.length >= 3 ? ['🥈','🥇 👑','🥉'] : top3.length === 2 ? ['🥈','🥇 👑'] : ['🥇 👑'];
    var pHeights = top3.length >= 3 ? ['','',''] : ['',''];

    var podiumHtml = podiumOrder.map(function(row, i) {
      var isMe = row.nickname === nickname;
      var acc = row.total_answered > 0 ? Math.round(row.correct_count/row.total_answered*100) : 0;
      var color = nicknameColor(row.nickname);
      var cls = pClasses[i];
      return '<div class="podium-card ' + cls + '">'
        + (cls==='p1' ? '<div class="podium-crown">👑</div>' : '')
        + '<div class="podium-avatar' + (isMe?' podium-me-ring':'') + '" style="background:' + color + '">' + row.nickname.charAt(0) + '</div>'
        + '<div class="podium-name">' + escHtml(row.nickname) + '</div>'
        + '<div class="podium-score" id="ps_' + i + '">0</div>'
        + '<div class="podium-label">' + pLabels[i] + '</div>'
        + '</div>';
    }).join('');
    document.getElementById('lb-podium').innerHTML = podiumHtml;
    document.getElementById('lb-podium').style.display = 'flex';
    podiumOrder.forEach(function(row, i) {
      var el = document.getElementById('ps_' + i);
      if (el) animScore(el, Math.round(row.score));
    });

    // List (rank 4~10)
    var rest = rows.slice(3);
    if (rest.length > 0) {
      document.getElementById('lb-list').innerHTML = rest.map(function(row, i) {
        var rank = i + 4;
        var isMe = row.nickname === nickname;
        var acc = row.total_answered > 0 ? Math.round(row.correct_count/row.total_answered*100) : 0;
        var lv = getLevel(Math.round(row.score));
        return '<div class="lb-list-item' + (isMe?' lb-me':'') + '" style="animation-delay:' + (i*0.06) + 's">'
          + '<div class="lb-list-rank">' + rank + '</div>'
          + avatarEl(row.nickname, 36, 'lb-list-avatar')
          + '<div class="lb-list-name">' + escHtml(row.nickname) + (isMe?' 👈':'')
            + '<span class="lb-level" style="color:' + lv.color + ';background:' + lv.bg + '">' + lv.name + '</span></div>'
          + '<div class="lb-list-right">'
            + '<div class="lb-list-score">' + Math.round(row.score) + '</div>'
            + '<div class="lb-list-detail">' + row.total_answered + '題・' + acc + '%</div>'
          + '</div>'
          + '</div>';
      }).join('');
    }
  } catch(e) {
    document.getElementById('lb-loading').style.display = 'none';
    document.getElementById('lb-list').innerHTML = '<div class="lb-loading" style="display:block;color:#f87171">⚠️ 載入失敗，請重試</div>';
  }
}

// ===== RESET =====
function confirmReset() {
  if (!confirm('確定要清除本機的所有練習紀錄嗎？（雲端排行榜分數不受影響）')) return;
  stats = {}; wrongSet = new Set();
  saveLocalStorage();
  updateScoreBadge();
  renderStats();
  renderWrongList();
  alert('已清除本機紀錄。雲端分數保留不變。');
}
</script>
</body>
</html>"""

html = html_template.replace('QUESTIONS_PLACEHOLDER', questions_js)
html = html.replace('SUPABASE_URL_PLACEHOLDER', SUPABASE_URL)
html = html.replace('SUPABASE_KEY_PLACEHOLDER', SUPABASE_KEY)

output_path = '國文練習網站.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {output_path}")
print(f"File size: {os.path.getsize(output_path):,} bytes")
