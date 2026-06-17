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
  #login-screen { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; padding:24px; }
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

  /* ===== TABS ===== */
  .tabs { display:flex; background:var(--card); border-bottom:1px solid var(--border); }
  .tab-btn { flex:1; padding:11px 4px; border:none; background:none; font-family:inherit; font-size:12px; cursor:pointer; color:var(--gray); border-bottom:3px solid transparent; transition:all 0.2s; white-space:nowrap; }
  .tab-btn.active { color:var(--primary); border-bottom-color:var(--primary); font-weight:700; }

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

  /* ===== LEADERBOARD ===== */
  .lb-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .lb-refresh { background:var(--light-blue); color:var(--primary); border:none; border-radius:20px; padding:5px 12px; font-size:12px; font-weight:700; cursor:pointer; font-family:inherit; }
  .lb-score-formula { background:var(--card); border-radius:10px; padding:10px 14px; margin-bottom:14px; font-size:12px; color:var(--gray); border-left:4px solid var(--purple); }
  .lb-score-formula b { color:var(--purple); }
  .lb-table { background:var(--card); border-radius:12px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .lb-row { display:flex; align-items:center; padding:12px 14px; border-bottom:1px solid var(--border); gap:12px; }
  .lb-row:last-child { border-bottom:none; }
  .lb-row.top3 { background:linear-gradient(90deg, rgba(251,191,36,0.08) 0%, transparent 100%); }
  .lb-rank { min-width:32px; font-size:18px; text-align:center; }
  .lb-name { flex:1; font-weight:700; font-size:14px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .lb-score { font-size:18px; font-weight:700; color:var(--purple); min-width:50px; text-align:right; }
  .lb-detail { font-size:11px; color:var(--gray); min-width:80px; text-align:right; }
  .lb-me { background:var(--light-blue) !important; }
  .lb-loading { text-align:center; padding:30px; color:var(--gray); font-size:14px; }
  .my-rank-card { background:var(--card); border-radius:12px; padding:14px; margin-bottom:14px; box-shadow:0 1px 4px rgba(0,0,0,0.05); border-left:4px solid var(--purple); }
  .my-rank-title { font-size:12px; color:var(--gray); margin-bottom:4px; }
  .my-rank-val { font-size:22px; font-weight:700; color:var(--purple); }

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
</div>

<!-- ===== APP ===== -->
<div id="app">
  <header>
    <h2>國文練習</h2>
    <span class="user-badge" id="user-badge">👤</span>
    <span class="score-badge" id="score-badge">✓ 0/0</span>
  </header>

  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('quiz')">📝 練習</button>
    <button class="tab-btn" onclick="switchTab('wrong')">❌ 錯題</button>
    <button class="tab-btn" onclick="switchTab('stats')">📊 成績</button>
    <button class="tab-btn" onclick="switchTab('rank')">🏆 排行榜</button>
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

  <!-- RANK TAB -->
  <div id="tab-rank" style="display:none">
    <div class="section-wrap">
      <div class="lb-header">
        <h3>🏆 積分排行榜</h3>
        <button class="lb-refresh" onclick="loadLeaderboard()">重新整理</button>
      </div>
      <div class="lb-score-formula">
        積分公式：<b>作答題數 + 正確率（%）</b><br>
        例：答 100 題、正確率 80% → 積分 = 100 + 80 = <b>180</b>
      </div>
      <div class="my-rank-card" id="my-rank-card" style="display:none">
        <div class="my-rank-title">我的目前名次</div>
        <div class="my-rank-val" id="my-rank-val">—</div>
      </div>
      <div class="lb-table" id="lb-table">
        <div class="lb-loading">載入中…</div>
      </div>
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
  return totalAnswered + accuracy;
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
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function selectOption(letter, btn) {
  if (answered) return;
  answered = true;
  var correct = currentQ.answer;
  var isCorrect = letter === correct;
  document.querySelectorAll('.opt-btn').forEach(function(b) {
    b.disabled = true;
    var l = b.querySelector('.opt-letter').textContent;
    if (l === correct) b.classList.add('correct');
    if (l === letter && !isCorrect) b.classList.add('wrong');
  });
  if (!stats[currentQ.id]) stats[currentQ.id] = {correct:0, wrong:0};
  if (isCorrect) { stats[currentQ.id].correct++; wrongSet.delete(currentQ.id); sessionCorrect++; }
  else { stats[currentQ.id].wrong++; wrongSet.add(currentQ.id); }
  saveLocalStorage();
  updateScoreBadge();
  scheduleSync();
  if (currentQ.explanation) {
    document.getElementById('explanation-text').textContent = currentQ.explanation;
    document.getElementById('explanation-box').classList.add('show');
  }
  document.getElementById('next-btn').classList.add('show');
}

function nextQuestion() { sessionIdx++; showQuestion(); }

function updateScoreBadge() {
  var t = getTotals();
  document.getElementById('score-badge').textContent = '✓ ' + t.correct + '/' + t.total;
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
  ['quiz','wrong','stats','rank'].forEach(function(t){
    document.getElementById('tab-'+t).style.display = t===tab?'block':'none';
  });
  document.querySelectorAll('.tab-btn').forEach(function(b,i){
    b.classList.toggle('active', ['quiz','wrong','stats','rank'][i]===tab);
  });
  if (tab==='wrong') renderWrongList();
  if (tab==='stats') renderStats();
  if (tab==='rank') { syncScore(); loadLeaderboard(); }
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

// ===== LEADERBOARD =====
async function loadLeaderboard() {
  document.getElementById('lb-table').innerHTML = '<div class="lb-loading">🔄 載入中…</div>';
  document.getElementById('my-rank-card').style.display = 'none';
  try {
    var rows = await sbGet('cn_scores', { 'order': 'score.desc', 'limit': '10', 'select': 'nickname,total_answered,correct_count,score' });
    if (rows.length === 0) {
      document.getElementById('lb-table').innerHTML = '<div class="lb-loading">還沒有人上榜，快去練習！</div>';
      return;
    }
    var medals = ['🥇','🥈','🥉'];
    var html = rows.map(function(row, i) {
      var accuracy = row.total_answered > 0 ? Math.round(row.correct_count/row.total_answered*100) : 0;
      var isMe = row.nickname === nickname;
      return '<div class="lb-row ' + (i<3?'top3':'') + (isMe?' lb-me':'') + '">'
        + '<span class="lb-rank">' + (medals[i] || (i+1)) + '</span>'
        + '<span class="lb-name">' + escHtml(row.nickname) + (isMe?' 👈':'') + '</span>'
        + '<span class="lb-detail">' + row.total_answered + '題・' + accuracy + '%</span>'
        + '<span class="lb-score">' + Math.round(row.score) + '</span>'
        + '</div>';
    }).join('');
    document.getElementById('lb-table').innerHTML = html;

    // 顯示自己的名次
    var myRankRows = await sbGet('cn_scores', { 'select': 'nickname,score', 'order': 'score.desc' });
    var myIdx = myRankRows.findIndex(function(r){ return r.nickname === nickname; });
    if (myIdx !== -1) {
      document.getElementById('my-rank-card').style.display = 'block';
      var myScore = Math.round(myRankRows[myIdx].score);
      var rankText = myIdx === 0 ? '🥇 第 1 名' : myIdx === 1 ? '🥈 第 2 名' : myIdx === 2 ? '🥉 第 3 名' : '第 ' + (myIdx+1) + ' 名';
      document.getElementById('my-rank-val').textContent = rankText + '  ·  積分 ' + myScore;
    }
  } catch(e) {
    document.getElementById('lb-table').innerHTML = '<div class="lb-loading">⚠️ 載入失敗，請檢查網路後再試</div>';
  }
}

// ===== RESET =====
function confirmReset() {
  if (!confirm('確定要清除本機的所有練習紀錄嗎？')) return;
  stats = {}; wrongSet = new Set();
  saveLocalStorage();
  updateScoreBadge();
  renderStats();
  renderWrongList();
  syncScore();
  alert('已清除本機紀錄。');
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
