import json, os

with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)

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
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: "微軟正黑體","Microsoft JhengHei",sans-serif; background: var(--bg); color: var(--dark); min-height: 100vh; }

  /* LOGIN */
  #login-screen { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; padding:24px; }
  #login-screen h1 { font-size:26px; font-weight:700; margin-bottom:6px; text-align:center; }
  #login-screen p { color:var(--gray); margin-bottom:28px; text-align:center; font-size:14px; }
  #login-card { background:var(--card); border-radius:16px; padding:32px 28px; box-shadow:0 4px 24px rgba(0,0,0,0.08); width:100%; max-width:400px; }
  #login-card label { display:block; font-size:14px; color:var(--gray); margin-bottom:8px; font-weight:600; }
  #nickname-input { width:100%; padding:12px 16px; font-size:18px; border:2px solid var(--border); border-radius:10px; font-family:inherit; outline:none; transition:border-color 0.2s; }
  #nickname-input:focus { border-color:var(--primary); }
  #start-btn { width:100%; padding:14px; margin-top:20px; background:var(--primary); color:white; border:none; border-radius:10px; font-size:16px; font-weight:700; cursor:pointer; font-family:inherit; transition:background 0.2s; }
  #start-btn:hover { background:#1d4ed8; }
  .history-box { margin-top:20px; padding:14px; background:var(--bg); border-radius:10px; }
  .history-box h3 { font-size:13px; color:var(--gray); margin-bottom:8px; }
  .history-item { font-size:13px; color:var(--dark); padding:3px 0; }

  /* APP */
  #app { display:none; }
  header { background:var(--dark); color:white; padding:12px 20px; display:flex; align-items:center; gap:12px; position:sticky; top:0; z-index:100; }
  header h2 { font-size:15px; font-weight:700; flex:1; }
  .user-badge { background:rgba(255,255,255,0.15); padding:4px 10px; border-radius:20px; font-size:13px; }
  .score-badge { background:var(--primary); padding:4px 10px; border-radius:20px; font-size:13px; font-weight:700; }

  /* TABS */
  .tabs { display:flex; background:var(--card); border-bottom:1px solid var(--border); overflow-x:auto; }
  .tab-btn { flex:1; min-width:80px; padding:12px 8px; border:none; background:none; font-family:inherit; font-size:13px; cursor:pointer; color:var(--gray); border-bottom:3px solid transparent; transition:all 0.2s; white-space:nowrap; }
  .tab-btn.active { color:var(--primary); border-bottom-color:var(--primary); font-weight:700; }

  /* FILTER */
  .filter-bar { padding:12px 16px; background:var(--card); border-bottom:1px solid var(--border); display:flex; gap:8px; flex-wrap:wrap; }
  .filter-btn { padding:6px 12px; border:2px solid var(--border); background:var(--bg); border-radius:20px; font-size:12px; cursor:pointer; font-family:inherit; color:var(--gray); transition:all 0.15s; font-weight:600; }
  .filter-btn.active { background:var(--primary); color:white; border-color:var(--primary); }

  /* QUIZ */
  main { padding:16px; max-width:800px; margin:0 auto; }
  .progress-bar { height:6px; background:var(--border); border-radius:3px; margin-bottom:8px; overflow:hidden; }
  .progress-fill { height:100%; background:var(--primary); border-radius:3px; transition:width 0.4s; }
  .progress-text { font-size:12px; color:var(--gray); text-align:right; margin-bottom:12px; }

  .question-card { background:var(--card); border-radius:14px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-bottom:16px; }
  .q-meta { display:flex; gap:8px; margin-bottom:12px; align-items:center; flex-wrap:wrap; }
  .q-num { font-size:13px; color:var(--gray); }
  .q-lesson-tag { background:var(--light-blue); color:var(--primary); padding:2px 8px; border-radius:20px; font-size:12px; font-weight:700; }
  .q-text { font-size:16px; line-height:1.7; color:var(--dark); margin-bottom:18px; white-space:pre-line; }

  .options { display:flex; flex-direction:column; gap:10px; }
  .opt-btn { display:flex; align-items:flex-start; gap:12px; padding:12px 16px; background:var(--bg); border:2px solid var(--border); border-radius:10px; cursor:pointer; text-align:left; font-family:inherit; font-size:14px; line-height:1.6; transition:all 0.15s; color:var(--dark); width:100%; }
  .opt-btn:hover:not([disabled]) { border-color:var(--primary); background:var(--light-blue); }
  .opt-letter { min-width:28px; height:28px; background:white; border:2px solid var(--border); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; }
  .opt-btn.correct { border-color:var(--green); background:var(--light-green); }
  .opt-btn.correct .opt-letter { background:var(--green); border-color:var(--green); color:white; }
  .opt-btn.wrong { border-color:var(--red); background:var(--light-red); }
  .opt-btn.wrong .opt-letter { background:var(--red); border-color:var(--red); color:white; }
  .opt-btn[disabled] { cursor:default; }

  .explanation { margin-top:16px; padding:14px; background:#fffbeb; border-left:4px solid var(--yellow); border-radius:0 8px 8px 0; font-size:14px; line-height:1.7; display:none; }
  .explanation.show { display:block; }
  .exp-title { font-weight:700; color:#92400e; margin-bottom:6px; font-size:13px; }

  #next-btn { width:100%; padding:14px; background:var(--green); color:white; border:none; border-radius:10px; font-size:16px; font-weight:700; cursor:pointer; font-family:inherit; display:none; transition:background 0.2s; margin-top:4px; }
  #next-btn:hover { background:#15803d; }
  #next-btn.show { display:block; }

  /* WRONG LIST */
  .wrong-section { padding:16px; max-width:800px; margin:0 auto; }
  .wrong-section h3 { font-size:16px; font-weight:700; margin-bottom:16px; }
  .wrong-item { background:var(--card); border-radius:12px; padding:16px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .wrong-item-q { font-size:14px; line-height:1.6; margin-bottom:8px; }
  .wrong-item-ans { font-size:13px; color:var(--green); font-weight:700; }
  .wrong-item-exp { font-size:13px; color:var(--gray); margin-top:6px; line-height:1.6; }
  .no-wrong { text-align:center; color:var(--gray); padding:40px; font-size:15px; }

  /* STATS */
  .stats-section { padding:16px; max-width:800px; margin:0 auto; }
  .stats-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-bottom:16px; }
  .stat-card { background:var(--card); border-radius:12px; padding:16px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .stat-num { font-size:28px; font-weight:700; color:var(--primary); }
  .stat-label { font-size:12px; color:var(--gray); margin-top:4px; }
  .lesson-stat { background:var(--card); border-radius:12px; padding:14px; margin-bottom:10px; box-shadow:0 1px 4px rgba(0,0,0,0.05); }
  .lesson-stat-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
  .lesson-stat-bar { height:8px; background:var(--border); border-radius:4px; overflow:hidden; }
  .lesson-stat-fill { height:100%; border-radius:4px; transition:width 0.4s; }
  .reset-btn { width:100%; padding:12px; background:#fee2e2; color:var(--red); border:none; border-radius:10px; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit; margin-top:16px; }

  /* MODAL */
  .modal-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:200; align-items:center; justify-content:center; padding:20px; }
  .modal-overlay.show { display:flex; }
  .modal { background:white; border-radius:16px; padding:28px; max-width:360px; width:100%; text-align:center; }
  .modal-emoji { font-size:48px; margin-bottom:12px; }
  .modal-title { font-size:20px; font-weight:700; margin-bottom:8px; }
  .modal-sub { color:var(--gray); font-size:14px; margin-bottom:20px; }
  .modal-score { font-size:36px; font-weight:700; color:var(--primary); margin-bottom:4px; }
  .modal-btns { display:flex; gap:10px; }
  .modal-btn { flex:1; padding:12px; border:none; border-radius:10px; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit; }
  .modal-btn.primary { background:var(--primary); color:white; }
  .modal-btn.secondary { background:var(--bg); color:var(--dark); }

  @media (max-width:480px) {
    .q-text { font-size:15px; }
    .opt-btn { font-size:13px; }
  }
</style>
</head>
<body>

<div id="login-screen">
  <h1>📖 國中國文練習</h1>
  <p>陋室銘・鳥・深藍的憂鬱・秋之味<br>共 200 題選擇題，附詳解</p>
  <div id="login-card">
    <label for="nickname-input">請輸入你的暱稱</label>
    <input type="text" id="nickname-input" placeholder="例：小明、7年3班" maxlength="20" autocomplete="off">
    <button id="start-btn" onclick="startApp()">開始練習 →</button>
    <div id="history-box" class="history-box" style="display:none">
      <h3>📊 上次紀錄</h3>
      <div id="history-content"></div>
    </div>
  </div>
</div>

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
    <div class="wrong-section">
      <h3>❌ 錯題清單 <span id="wrong-count" style="color:var(--gray);font-size:14px;font-weight:400;"></span></h3>
      <div id="wrong-list"></div>
    </div>
  </div>

  <!-- STATS TAB -->
  <div id="tab-stats" style="display:none">
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-num" id="stat-correct">0</div><div class="stat-label">答對題數</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-answered">0</div><div class="stat-label">已作答</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-accuracy">—</div><div class="stat-label">正確率</div></div>
        <div class="stat-card"><div class="stat-num" id="stat-wrong-n">0</div><div class="stat-label">錯題數</div></div>
      </div>
      <div id="lesson-stats"></div>
      <button class="reset-btn" onclick="confirmReset()">🗑️ 清除所有紀錄</button>
    </div>
  </div>
</div>

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
const ALL_QUESTIONS = QUESTIONS_PLACEHOLDER;

let nickname = '';
let currentLesson = 'all';
let sessionPool = [];
let sessionIdx = 0;
let sessionCorrect = 0;
let currentQ = null;
let answered = false;

const KEY_NICKNAME = 'cn_nickname';
const KEY_STATS = 'cn_stats';
const KEY_WRONG = 'cn_wrong';

let stats = {};
let wrongSet = new Set();

function loadStorage() {
  try {
    stats = JSON.parse(localStorage.getItem(KEY_STATS) || '{}');
    const w = JSON.parse(localStorage.getItem(KEY_WRONG) || '[]');
    wrongSet = new Set(w);
  } catch(e) { stats = {}; wrongSet = new Set(); }
}

function saveStorage() {
  localStorage.setItem(KEY_STATS, JSON.stringify(stats));
  localStorage.setItem(KEY_WRONG, JSON.stringify([...wrongSet]));
}

window.onload = function() {
  const saved = localStorage.getItem(KEY_NICKNAME);
  if (saved) {
    document.getElementById('nickname-input').value = saved;
    loadStorage();
    showLoginHistory();
  }
  document.getElementById('nickname-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') startApp();
  });
};

function showLoginHistory() {
  const total = Object.values(stats).reduce((a,v)=>a+v.correct+v.wrong,0);
  if (total === 0) return;
  const correct = Object.values(stats).reduce((a,v)=>a+v.correct,0);
  const pct = Math.round(correct/total*100);
  document.getElementById('history-box').style.display = 'block';
  document.getElementById('history-content').innerHTML =
    '<div class="history-item">已作答 <b>' + total + '</b> 題，正確率 <b>' + pct + '%</b>（' + correct + '/' + total + '）</div>' +
    '<div class="history-item">錯題清單：<b>' + wrongSet.size + '</b> 題</div>';
}

function startApp() {
  const val = document.getElementById('nickname-input').value.trim();
  if (!val) { document.getElementById('nickname-input').focus(); return; }
  nickname = val;
  localStorage.setItem(KEY_NICKNAME, nickname);
  loadStorage();
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  document.getElementById('user-badge').textContent = '👤 ' + nickname;
  setLesson('all');
  updateScoreBadge();
}

function setLesson(lesson) {
  currentLesson = lesson;
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.lesson === lesson);
  });
  buildPool();
  sessionIdx = 0;
  sessionCorrect = 0;
  showQuestion();
}

function buildPool() {
  let pool;
  if (currentLesson === 'all') {
    pool = ALL_QUESTIONS.slice();
  } else if (currentLesson === 'wrong') {
    pool = ALL_QUESTIONS.filter(q => wrongSet.has(q.id));
  } else {
    pool = ALL_QUESTIONS.filter(q => q.lesson === currentLesson);
  }
  // Shuffle
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  sessionPool = pool;
}

function showQuestion() {
  if (sessionPool.length === 0) {
    document.getElementById('q-text').innerHTML = currentLesson === 'wrong'
      ? '<span style="color:var(--green)">🎉 目前沒有錯題，繼續加油！</span>'
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

  if (sessionIdx >= sessionPool.length) {
    showCompleteModal();
    return;
  }

  answered = false;
  currentQ = sessionPool[sessionIdx];

  const total = sessionPool.length;
  const pct = Math.round(sessionIdx / total * 100);
  document.getElementById('progress-fill').style.width = pct + '%';
  document.getElementById('progress-text').textContent = '第 ' + (sessionIdx+1) + ' / ' + total + ' 題';
  document.getElementById('q-num').textContent = '題目 #' + currentQ.id;
  document.getElementById('q-lesson-tag').textContent = currentQ.lesson;
  document.getElementById('q-text').textContent = currentQ.question;

  const container = document.getElementById('options-container');
  container.innerHTML = '';
  ['A','B','C','D'].forEach(function(letter) {
    const text = currentQ.options[letter];
    if (!text) return;
    const btn = document.createElement('button');
    btn.className = 'opt-btn';
    btn.innerHTML = '<span class="opt-letter">' + letter + '</span><span>' + escHtml(text) + '</span>';
    btn.addEventListener('click', function() { selectOption(letter, btn); });
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

  const correct = currentQ.answer;
  const isCorrect = letter === correct;

  document.querySelectorAll('.opt-btn').forEach(function(b) {
    b.disabled = true;
    const l = b.querySelector('.opt-letter').textContent;
    if (l === correct) b.classList.add('correct');
    if (l === letter && !isCorrect) b.classList.add('wrong');
  });

  if (!stats[currentQ.id]) stats[currentQ.id] = {correct:0, wrong:0};
  if (isCorrect) {
    stats[currentQ.id].correct++;
    wrongSet.delete(currentQ.id);
    sessionCorrect++;
  } else {
    stats[currentQ.id].wrong++;
    wrongSet.add(currentQ.id);
  }
  saveStorage();
  updateScoreBadge();

  if (currentQ.explanation) {
    document.getElementById('explanation-text').textContent = currentQ.explanation;
    document.getElementById('explanation-box').classList.add('show');
  }
  document.getElementById('next-btn').classList.add('show');
}

function nextQuestion() {
  sessionIdx++;
  showQuestion();
}

function updateScoreBadge() {
  const total = Object.values(stats).reduce(function(a,v){return a+v.correct+v.wrong;},0);
  const correct = Object.values(stats).reduce(function(a,v){return a+v.correct;},0);
  document.getElementById('score-badge').textContent = '✓ ' + correct + '/' + total;
}

function showCompleteModal() {
  const total = sessionPool.length;
  const pct = Math.round(sessionCorrect/total*100);
  const emoji = pct>=90?'🏆':pct>=70?'🎉':pct>=50?'💪':'📚';
  const msg = pct>=90?'太厲害了！':pct>=70?'不錯唷！':pct>=50?'繼續加油！':'多練習就會進步！';
  const lessonLabel = currentLesson==='all'?'全部題目':currentLesson==='wrong'?'錯題複習':currentLesson;
  document.getElementById('modal-emoji').textContent = emoji;
  document.getElementById('modal-title').textContent = lessonLabel + ' 完成！';
  document.getElementById('modal-score').textContent = sessionCorrect + ' / ' + total;
  document.getElementById('modal-sub').textContent = '正確率 ' + pct + '% — ' + msg;
  document.getElementById('complete-modal').classList.add('show');
}

function closeModal() {
  document.getElementById('complete-modal').classList.remove('show');
  switchTab('wrong');
}

function restartLesson() {
  document.getElementById('complete-modal').classList.remove('show');
  setLesson(currentLesson);
}

function switchTab(tab) {
  ['quiz','wrong','stats'].forEach(function(t) {
    document.getElementById('tab-'+t).style.display = t===tab?'block':'none';
  });
  document.querySelectorAll('.tab-btn').forEach(function(b,i) {
    b.classList.toggle('active', ['quiz','wrong','stats'][i]===tab);
  });
  if (tab==='wrong') renderWrongList();
  if (tab==='stats') renderStats();
}

function renderWrongList() {
  const container = document.getElementById('wrong-list');
  const wrongQs = ALL_QUESTIONS.filter(function(q){ return wrongSet.has(q.id); });
  document.getElementById('wrong-count').textContent = '（' + wrongQs.length + ' 題）';
  if (wrongQs.length === 0) {
    container.innerHTML = '<div class="no-wrong">🎉 太棒了！目前沒有錯題</div>';
    return;
  }
  container.innerHTML = wrongQs.map(function(q) {
    const exp = q.explanation ? q.explanation.slice(0,150) + (q.explanation.length>150?'…':'') : '';
    return '<div class="wrong-item">' +
      '<div class="q-meta" style="margin-bottom:8px">' +
        '<span class="q-num" style="font-size:12px">#' + q.id + '</span>' +
        '<span class="q-lesson-tag">' + q.lesson + '</span>' +
      '</div>' +
      '<div class="wrong-item-q">' + escHtml(q.question) + '</div>' +
      '<div class="wrong-item-ans">✓ 正確答案：(' + q.answer + ') ' + escHtml(q.options[q.answer]||'') + '</div>' +
      (exp ? '<div class="wrong-item-exp">📌 ' + escHtml(exp) + '</div>' : '') +
      '</div>';
  }).join('');
}

function renderStats() {
  const total = Object.values(stats).reduce(function(a,v){return a+v.correct+v.wrong;},0);
  const correct = Object.values(stats).reduce(function(a,v){return a+v.correct;},0);
  document.getElementById('stat-correct').textContent = correct;
  document.getElementById('stat-answered').textContent = total;
  document.getElementById('stat-accuracy').textContent = total>0 ? Math.round(correct/total*100)+'%' : '—';
  document.getElementById('stat-wrong-n').textContent = wrongSet.size;

  const lessons = ['陋室銘','鳥','深藍的憂鬱','秋之味'];
  const colors = {'陋室銘':'#2563eb','鳥':'#16a34a','深藍的憂鬱':'#9333ea','秋之味':'#ea580c'};
  document.getElementById('lesson-stats').innerHTML = lessons.map(function(lesson) {
    const qs = ALL_QUESTIONS.filter(function(q){return q.lesson===lesson;});
    const done = qs.filter(function(q){return stats[q.id];});
    const c = done.reduce(function(a,q){return a+(stats[q.id]?stats[q.id].correct:0);},0);
    const t = done.reduce(function(a,q){return a+(stats[q.id]?stats[q.id].correct+stats[q.id].wrong:0);},0);
    const pct = t>0?Math.round(c/t*100):0;
    const color = colors[lesson];
    return '<div class="lesson-stat">' +
      '<div class="lesson-stat-row">' +
        '<span style="font-weight:700;color:' + color + '">' + lesson + '</span>' +
        '<span style="font-size:13px;color:var(--gray)">' + c + '/' + t + ' 題・' + (t>0?pct+'%':'未作答') + '</span>' +
      '</div>' +
      '<div class="lesson-stat-bar"><div class="lesson-stat-fill" style="width:' + pct + '%;background:' + color + '"></div></div>' +
      '</div>';
  }).join('');
}

function confirmReset() {
  if (!confirm('確定要清除所有練習紀錄嗎？')) return;
  stats = {}; wrongSet = new Set();
  saveStorage();
  updateScoreBadge();
  renderStats();
  renderWrongList();
  alert('已清除所有紀錄。');
}
</script>
</body>
</html>"""

# Embed questions data
html = html_template.replace('QUESTIONS_PLACEHOLDER', questions_js)

output_path = '國文練習網站.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {output_path}")
print(f"File size: {os.path.getsize(output_path):,} bytes")
