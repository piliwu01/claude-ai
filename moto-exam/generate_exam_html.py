import json, os

with open('questions.json', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    if not q['question']:
        q['question'] = '（本題含圖示，請參閱原始題庫）'

qs_json = json.dumps(questions, ensure_ascii=False)
total = len(questions)

HTML = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>機車駕照筆試練習｜全 __TOTAL__ 題</title>
<style>
  :root {{
    --blue: #2563eb; --green: #16a34a; --red: #dc2626;
    --gray: #64748b; --bg: #f0f4f8; --card: #fff;
    --border: #e2e8f0; --text: #1e293b;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "微軟正黑體","Microsoft JhengHei","Noto Sans TC",sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
  header {{ background: var(--blue); color: #fff; padding: 14px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }}
  header h1 {{ font-size: 18px; font-weight: 700; }}
  .score-badge {{ background: rgba(255,255,255,.2); border-radius: 20px; padding: 4px 14px; font-size: 14px; font-weight: 600; }}
  .main {{ max-width: 780px; margin: 24px auto; padding: 0 16px; }}
  .controls {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center; }}
  .btn {{ padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; font-weight: 600; font-family: inherit; transition: opacity .15s; }}
  .btn:hover {{ opacity: .85; }}
  .btn-blue  {{ background: var(--blue); color: #fff; }}
  .btn-green {{ background: var(--green); color: #fff; }}
  .btn-gray  {{ background: var(--border); color: var(--text); }}
  .btn-red   {{ background: var(--red); color: #fff; }}
  .btn-sm {{ padding: 5px 12px; font-size: 13px; }}
  select, input[type=number] {{ padding: 7px 10px; border-radius: 8px; border: 1.5px solid var(--border); font-size: 14px; font-family: inherit; background: #fff; }}
  .progress-wrap {{ height: 6px; background: var(--border); border-radius: 4px; margin-bottom: 16px; overflow: hidden; }}
  .progress-bar {{ height: 100%; background: var(--blue); border-radius: 4px; transition: width .3s; }}
  .question-meta {{ font-size: 13px; color: var(--gray); margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }}
  .card {{ background: var(--card); border-radius: 14px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,.08); margin-bottom: 16px; }}
  .question-id {{ font-size: 13px; color: var(--gray); margin-bottom: 6px; }}
  .question-text {{ font-size: 18px; font-weight: 700; line-height: 1.7; margin-bottom: 20px; }}
  .options {{ display: flex; flex-direction: column; gap: 12px; }}
  .option-btn {{ width: 100%; text-align: left; padding: 14px 18px; border-radius: 10px; border: 2px solid var(--border); background: #fff; cursor: pointer; font-size: 15px; font-family: inherit; line-height: 1.5; color: var(--text); transition: border-color .15s, background .15s; display: flex; align-items: flex-start; gap: 10px; }}
  .option-btn:hover:not(:disabled) {{ border-color: var(--blue); background: #eff6ff; }}
  .option-btn .opt-label {{ font-weight: 700; min-width: 26px; color: var(--blue); font-size: 16px; }}
  .option-btn.correct {{ border-color: var(--green); background: #f0fdf4; }}
  .option-btn.correct .opt-label {{ color: var(--green); }}
  .option-btn.wrong {{ border-color: var(--red); background: #fef2f2; }}
  .option-btn.wrong .opt-label {{ color: var(--red); }}
  .option-btn:disabled {{ cursor: default; }}
  .result-bar {{ display: none; padding: 12px 18px; border-radius: 10px; font-size: 15px; font-weight: 600; margin-top: 14px; line-height: 1.5; }}
  .result-bar.show {{ display: block; }}
  .result-bar.correct {{ background: #f0fdf4; color: var(--green); }}
  .result-bar.wrong   {{ background: #fef2f2; color: var(--red); }}
  .nav {{ display: flex; gap: 10px; align-items: center; justify-content: center; flex-wrap: wrap; }}
  .jump-wrap {{ display: flex; align-items: center; gap: 6px; font-size: 14px; color: var(--gray); }}
  input[type=number] {{ width: 80px; text-align: center; }}
  .stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }}
  .stat-card {{ flex: 1; min-width: 70px; background: var(--card); border-radius: 10px; padding: 12px 16px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
  .stat-card .num {{ font-size: 22px; font-weight: 700; }}
  .stat-card .lbl {{ font-size: 12px; color: var(--gray); margin-top: 2px; }}
  .stat-card.green .num {{ color: var(--green); }}
  .stat-card.red .num {{ color: var(--red); }}
  .stat-card.blue .num {{ color: var(--blue); }}
  .mode-banner {{ background: #fef3c7; color: #92400e; border-radius: 8px; padding: 8px 16px; font-size: 13px; font-weight: 600; margin-bottom: 12px; display: none; }}
  .mode-banner.show {{ display: block; }}
  .hint {{ font-size: 12px; color: var(--gray); text-align: center; margin-top: 12px; }}
  @media (max-width: 480px) {{
    .question-text {{ font-size: 16px; }}
    .option-btn {{ font-size: 14px; padding: 12px 14px; }}
    .card {{ padding: 18px; }}
  }}
</style>
</head>
<body>
<header>
  <h1>&#x1F3CD; 機車駕照筆試練習</h1>
  <div class="score-badge" id="headerScore">得分 0 / 0</div>
</header>
<div class="main">
  <div class="stats">
    <div class="stat-card blue"><div class="num" id="statTotal">0</div><div class="lbl">已作答</div></div>
    <div class="stat-card green"><div class="num" id="statCorrect">0</div><div class="lbl">答對</div></div>
    <div class="stat-card red"><div class="num" id="statWrong">0</div><div class="lbl">答錯</div></div>
    <div class="stat-card"><div class="num" id="statRate">—</div><div class="lbl">正確率</div></div>
  </div>
  <div class="controls">
    <button class="btn btn-blue btn-sm" id="btnOrder">&#x1F4CB; 順序作答</button>
    <button class="btn btn-blue btn-sm" id="btnRandom">&#x1F500; 隨機出題</button>
    <button class="btn btn-red btn-sm" id="btnWrong">&#x274C; 複習錯題</button>
    <button class="btn btn-gray btn-sm" id="btnReset">&#x1F504; 重置紀錄</button>
  </div>
  <div class="mode-banner" id="modeBanner">&#x26A0; 錯題複習模式</div>
  <div class="progress-wrap"><div class="progress-bar" id="progressBar" style="width:0%"></div></div>
  <div class="question-meta">
    <span id="qMeta">第 1 / __TOTAL__ 題</span>
    <span style="font-size:12px;color:var(--gray)">鍵盤：← → 換題 | 1 2 3 選答</span>
  </div>
  <div class="card">
    <div class="question-id" id="qId"></div>
    <div class="question-text" id="qText"></div>
    <div class="options" id="optWrap"></div>
    <div class="result-bar" id="resultBar"></div>
  </div>
  <div class="nav">
    <button class="btn btn-gray" id="btnPrev">&#x25C4; 上一題</button>
    <div class="jump-wrap">
      跳至題號 <input type="number" id="jumpInput" min="1" max="804" placeholder="1~804">
      <button class="btn btn-gray btn-sm" id="btnJump">GO</button>
    </div>
    <button class="btn btn-blue" id="btnNext">下一題 &#x25BA;</button>
  </div>
  <div class="hint">共 __TOTAL__ 題（含 122 道圖示題需對照原題庫）</div>
</div>
<script>
const ALL_Q = QUESTIONS_JSON_PLACEHOLDER;
let queue=[], cursor=0, answered={}, wrongSet=new Set(), mode='order';

function shuffle(a){{for(let i=a.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}}return a;}}

function buildQueue(m){{
  mode=m;
  if(m==='order') queue=ALL_Q.map((_,i)=>i);
  else if(m==='random') queue=shuffle(ALL_Q.map((_,i)=>i));
  else if(m==='wrong'){{
    queue=shuffle(ALL_Q.map((_,i)=>i).filter(i=>wrongSet.has(ALL_Q[i].id)));
    if(!queue.length){{alert('目前沒有錯題！');return false;}}
  }}
  cursor=0;
  document.getElementById('modeBanner').classList.toggle('show',m==='wrong');
  return true;
}}

function render(){{
  const q=ALL_Q[queue[cursor]], tot=queue.length;
  document.getElementById('progressBar').style.width=((cursor+1)/tot*100)+'%';
  document.getElementById('qMeta').textContent='第 '+(cursor+1)+' / '+tot+' 題';
  document.getElementById('qId').textContent='題號 #'+q.id;
  document.getElementById('qText').textContent=q.question;
  const wrap=document.getElementById('optWrap');
  wrap.innerHTML='';
  ['①','②','③'].forEach((lbl,idx)=>{{
    const opt=q.options[idx];
    if(!opt) return;
    const btn=document.createElement('button');
    btn.className='option-btn';
    btn.innerHTML='<span class="opt-label">'+lbl+'</span><span>'+opt+'</span>';
    btn.dataset.idx=idx+1;
    btn.addEventListener('click',()=>selectAnswer(btn,q));
    wrap.appendChild(btn);
  }});
  const res=document.getElementById('resultBar');
  res.className='result-bar'; res.textContent='';
  if(answered.hasOwnProperty(q.id)){{
    const was=answered[q.id];
    highlightAnswer(q, was?q.answer:null);
    showResult(was, q.answer, q.options[q.answer-1]);
  }}
  updateStats();
}}

function selectAnswer(btn,q){{
  if(answered.hasOwnProperty(q.id)) return;
  const chosen=parseInt(btn.dataset.idx), correct=chosen===q.answer;
  answered[q.id]=correct;
  if(!correct) wrongSet.add(q.id);
  highlightAnswer(q, chosen);
  showResult(correct, q.answer, q.options[q.answer-1]);
  updateStats();
}}

function highlightAnswer(q, chosen){{
  document.querySelectorAll('.option-btn').forEach(b=>{{
    b.disabled=true;
    const idx=parseInt(b.dataset.idx);
    if(idx===q.answer) b.classList.add('correct');
    else if(chosen&&idx===chosen) b.classList.add('wrong');
  }});
}}

function showResult(correct, ansIdx, ansText){{
  const res=document.getElementById('resultBar');
  if(correct){{res.textContent='✅ 答對了！'; res.className='result-bar show correct';}}
  else{{res.textContent='❌ 答錯！正確答案為 '+['①','②','③'][ansIdx-1]+'：'+(ansText||'請見原題庫'); res.className='result-bar show wrong';}}
}}

function updateStats(){{
  const vals=Object.values(answered), tot=vals.length, c=vals.filter(v=>v).length, w=tot-c;
  document.getElementById('statTotal').textContent=tot;
  document.getElementById('statCorrect').textContent=c;
  document.getElementById('statWrong').textContent=w;
  document.getElementById('statRate').textContent=tot?Math.round(c/tot*100)+'%':'—';
  document.getElementById('headerScore').textContent='得分 '+c+' / '+tot;
}}

document.getElementById('btnNext').addEventListener('click',()=>{{if(cursor<queue.length-1){{cursor++;render();}}else alert('已是最後一題！');}});
document.getElementById('btnPrev').addEventListener('click',()=>{{if(cursor>0){{cursor--;render();}}}});
document.getElementById('btnOrder').addEventListener('click',()=>{{buildQueue('order');render();}});
document.getElementById('btnRandom').addEventListener('click',()=>{{buildQueue('random');render();}});
document.getElementById('btnWrong').addEventListener('click',()=>{{if(buildQueue('wrong'))render();}});
document.getElementById('btnReset').addEventListener('click',()=>{{
  if(!confirm('確定要重置所有作答紀錄？'))return;
  answered={{}};wrongSet.clear();buildQueue(mode);render();
}});
document.getElementById('btnJump').addEventListener('click',()=>{{
  const val=parseInt(document.getElementById('jumpInput').value);
  const gi=ALL_Q.findIndex(q=>q.id===val);
  if(gi<0){{alert('找不到題號 '+val);return;}}
  const qi=queue.indexOf(gi);
  if(qi>=0)cursor=qi; else{{queue.splice(cursor+1,0,gi);cursor++;}}
  render();
}});
document.getElementById('jumpInput').addEventListener('keydown',e=>{{if(e.key==='Enter')document.getElementById('btnJump').click();}});
document.addEventListener('keydown',e=>{{
  if(e.target.tagName==='INPUT') return;
  if(e.key==='ArrowRight'||e.key==='d') document.getElementById('btnNext').click();
  if(e.key==='ArrowLeft'||e.key==='a') document.getElementById('btnPrev').click();
  const opts=document.querySelectorAll('.option-btn');
  if(e.key==='1'&&opts[0]) opts[0].click();
  if(e.key==='2'&&opts[1]) opts[1].click();
  if(e.key==='3'&&opts[2]) opts[2].click();
}});
buildQueue('order');
render();
</script>
</body>
</html>"""

# 把 JSON 資料嵌入
HTML = HTML.replace('__TOTAL__', str(total)).replace('QUESTIONS_JSON_PLACEHOLDER', qs_json)

out_path = r'C:\Users\北興\Desktop\機車筆試練習.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

size = os.path.getsize(out_path)
print(f'完成！{out_path}')
print(f'檔案大小：{size//1024} KB')
