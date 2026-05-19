"""為第二份考卷（木蘭詩等）生成互動 HTML"""
import json, os
from collections import defaultdict

CATEGORY_ORDER = [
    ('木蘭詩／樂府詩', '📜'),
    ('歲月跟著',       '⏳'),
    ('運動家的風度',   '🏅'),
    ('修辭',           '✏️'),
    ('字音字形',       '🔤'),
    ('成語／詞語',     '📖'),
    ('詞性文法',       '🔍'),
    ('其他語文知識',   '📌'),
]

HALF = {'Ａ':'A','Ｂ':'B','Ｃ':'C','Ｄ':'D'}
DISP = {'A':'Ａ','B':'Ｂ','C':'Ｃ','D':'Ｄ'}

def opt_d(l): return DISP.get(l, l)
def sid(c): return c.replace('／','_').replace('/','_')

def card(q):
    qid = f'q{q["id"]}'
    ans_half = HALF.get(q['answer'], q['answer'])
    ans_text = q['options'].get(q['answer']) or q['options'].get(ans_half,'')
    opts = ''
    for fw in ['Ａ','Ｂ','Ｃ','Ｄ']:
        hw = HALF.get(fw, fw)
        v = q['options'].get(fw) or q['options'].get(hw,'')
        if v:
            opts += f'<div class="option" data-letter="{hw}">（{fw}）{v}</div>\n'
    return f'''\
<div class="card" id="{qid}" onclick="toggleCard('{qid}')">
  <div class="card-header">
    <span class="q-num">第&nbsp;{q["id"]}&nbsp;題</span>
    <span class="section-tag">{q["section"]}</span>
    <span class="expand-icon">＋</span>
  </div>
  <div class="q-text">{q["question"]}</div>
  <div class="card-body">
    <div class="options" id="opts-{qid}">{opts}</div>
    <button class="show-ans-btn" onclick="showAnswer(event,'{qid}','{ans_half}')">顯示答案</button>
    <div class="answer-block" id="ans-{qid}" style="display:none">
      <div class="answer-line">正確答案：<strong>（{opt_d(q["answer"])}）</strong>&nbsp;{ans_text}</div>
      <div class="explanation">💡&nbsp;{q["explanation"] or "（無解析）"}</div>
    </div>
  </div>
</div>'''

with open('exam2_data.json', encoding='utf-8') as f:
    questions = json.load(f)

groups = defaultdict(list)
for q in questions:
    groups[q['category']].append(q)

nav = ''.join(
    f'<button class="nav-btn" onclick="scrollTo_(\'{sid(c)}\')">{e} {c}</button>\n'
    for c, e in CATEGORY_ORDER if groups.get(c)
)
secs = ''
for c, e in CATEGORY_ORDER:
    qs = groups.get(c, [])
    if not qs: continue
    secs += f'''<section class="category-section" id="cat-{sid(c)}">
  <h2 class="cat-title">{e} {c} <span class="count">({len(qs)} 題)</span></h2>
  <div class="cards-row">{"".join(card(q) for q in qs)}</div>
</section>'''

total_cat = sum(1 for c,_ in CATEGORY_ORDER if groups.get(c))

CSS = """:root{--bg:#f0f4f8;--card-bg:#fff;--primary:#2563eb;--primary-light:#dbeafe;
  --green:#16a34a;--green-light:#dcfce7;--text:#1e293b;--sub:#64748b;
  --border:#e2e8f0;--shadow:0 2px 8px rgba(0,0,0,.08);--radius:12px;--nav-h:54px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-padding-top:var(--nav-h)}
body{font-family:'微軟正黑體','Microsoft JhengHei','Noto Sans TC',sans-serif;
     background:var(--bg);color:var(--text);line-height:1.75;
     overflow-wrap:break-word;word-break:break-word}
.hero{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;
      padding:clamp(1.5rem,5vw,3rem) clamp(1rem,4vw,2rem);text-align:center}
.hero h1{font-size:clamp(1.1rem,4vw,1.8rem);font-weight:700;letter-spacing:.04em}
.hero p{margin-top:.5rem;font-size:clamp(.8rem,2.5vw,1rem);opacity:.85}
.hero .stats{margin-top:1rem;display:flex;justify-content:center;flex-wrap:wrap;
             gap:.6rem;font-size:clamp(.75rem,2vw,.9rem)}
.hero .stat{background:rgba(255,255,255,.18);border-radius:8px;padding:.35rem .9rem;white-space:nowrap}
.nav-bar{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--border);
         padding:.55rem 1rem;display:flex;flex-wrap:nowrap;gap:.45rem;overflow-x:auto;
         -webkit-overflow-scrolling:touch;scrollbar-width:none;box-shadow:0 2px 6px rgba(0,0,0,.06)}
.nav-bar::-webkit-scrollbar{display:none}
.nav-btn{flex-shrink:0;background:var(--primary-light);color:var(--primary);border:none;
         border-radius:20px;padding:.4rem .9rem;font-size:clamp(.75rem,2vw,.85rem);
         font-family:inherit;cursor:pointer;transition:.15s;white-space:nowrap;min-height:36px}
.nav-btn:hover{background:var(--primary);color:#fff}
main{padding:clamp(1rem,3vw,1.5rem) clamp(.75rem,3vw,1.5rem) 4rem;max-width:1440px;margin:0 auto}
.category-section{margin-bottom:clamp(1.5rem,4vw,2.5rem)}
.cat-title{font-size:clamp(1rem,2.5vw,1.25rem);font-weight:700;color:var(--primary);
           margin-bottom:1rem;padding-left:.75rem;border-left:4px solid var(--primary)}
.cat-title .count{font-size:.82rem;color:var(--sub);font-weight:400;margin-left:.25rem}
.cards-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,280px),1fr));
           gap:clamp(.75rem,2vw,1.1rem);align-items:start}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);
      box-shadow:var(--shadow);cursor:pointer;transition:box-shadow .2s,border-color .2s,transform .15s;overflow:hidden}
.card:hover{box-shadow:0 4px 18px rgba(37,99,235,.14);border-color:#93c5fd;transform:translateY(-1px)}
.card.active{border-color:var(--primary);transform:none}
.card-header{display:flex;align-items:center;gap:.45rem;padding:.7rem 1rem .45rem}
.q-num{flex-shrink:0;font-size:.72rem;font-weight:700;background:var(--primary);color:#fff;
       border-radius:20px;padding:.12rem .55rem;white-space:nowrap}
.section-tag{font-size:.68rem;background:#f1f5f9;color:var(--sub);border-radius:20px;
             padding:.08rem .45rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.expand-icon{margin-left:auto;flex-shrink:0;font-size:1.2rem;color:var(--sub);
             transition:transform .2s;line-height:1;user-select:none}
.card.active .expand-icon{transform:rotate(45deg);color:var(--primary)}
.q-text{font-size:clamp(.82rem,2vw,.92rem);padding:0 1rem .75rem;color:var(--text);
        display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card.active .q-text{-webkit-line-clamp:unset;overflow:visible}
.card-body{display:none;padding:.75rem 1rem 1rem;border-top:1px dashed var(--border)}
.card.active .card-body{display:block}
.options{margin-bottom:.75rem}
.option{font-size:clamp(.78rem,2vw,.86rem);padding:.35rem .6rem;border-radius:6px;
        margin-bottom:.3rem;background:#f8fafc;line-height:1.5}
.option.correct{background:var(--green-light);color:var(--green);font-weight:600}
.option.wrong{background:#fef2f2;color:#dc2626;text-decoration:line-through;opacity:.65}
.show-ans-btn{width:100%;background:var(--green);color:#fff;border:none;border-radius:8px;
              padding:.55rem;font-size:clamp(.82rem,2vw,.92rem);font-family:inherit;
              cursor:pointer;transition:.15s;min-height:40px}
.show-ans-btn:hover{background:#15803d}
.show-ans-btn:disabled{background:#94a3b8;cursor:default}
.answer-block{margin-top:.75rem}
.answer-line{font-size:clamp(.82rem,2vw,.92rem);background:var(--green-light);color:var(--green);
             border-radius:8px;padding:.5rem .75rem;margin-bottom:.5rem;line-height:1.6}
.explanation{font-size:clamp(.76rem,1.8vw,.82rem);background:#fffbeb;border-left:3px solid #f59e0b;
             color:#92400e;padding:.5rem .75rem;border-radius:0 6px 6px 0;line-height:1.65}
footer{text-align:center;padding:1.5rem 1rem;font-size:.8rem;color:var(--sub);border-top:1px solid var(--border)}
@media(min-width:480px){.cards-row{grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr))}}
@media(min-width:768px){.nav-bar{flex-wrap:wrap;overflow-x:visible}
  .cards-row{grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr))}}
@media(min-width:1024px){.cards-row{grid-template-columns:repeat(auto-fill,minmax(min(100%,310px),1fr))}}
@media(prefers-color-scheme:dark){
  :root{--bg:#0f172a;--card-bg:#1e293b;--text:#e2e8f0;--sub:#94a3b8;
        --border:#334155;--shadow:0 2px 8px rgba(0,0,0,.3);--primary-light:#1e3a8a}
  .nav-bar{background:#1e293b;border-bottom-color:#334155}
  .section-tag{background:#334155}.option{background:#0f172a}
  .explanation{background:#2d1e00;color:#fbbf24}}
@media(prefers-reduced-motion:reduce){.card,.card:hover,.show-ans-btn{transition:none}}"""

JS = """function toggleCard(qid){document.getElementById(qid).classList.toggle('active')}
function showAnswer(e,qid,correct){
  e.stopPropagation();
  document.getElementById('ans-'+qid).style.display='block';
  e.target.disabled=true;e.target.textContent='已顯示答案';
  document.querySelectorAll('#opts-'+qid+' .option').forEach(function(o){
    o.classList.add(o.dataset.letter===correct?'correct':'wrong');});
}
function scrollTo_(id){var el=document.getElementById('cat-'+id);
  if(el)el.scrollIntoView({behavior:'smooth',block:'start'});}"""

html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>114 學年度國中國文測驗</title>
<style>{CSS}</style>
</head>
<body>
<div class="hero">
  <h1>114 學年度國中國文測驗</h1>
  <p>互動練習卷（含解析）</p>
  <div class="stats">
    <div class="stat">📝 共 {len(questions)} 題</div>
    <div class="stat">🗂️ 共 {total_cat} 大類</div>
    <div class="stat">💡 含詳細解析</div>
  </div>
</div>
<nav class="nav-bar">{nav}</nav>
<main>{secs}</main>
<footer>點擊題目展開 · 點擊「顯示答案」查看解析</footer>
<script>{JS}</script>
</body>
</html>"""

out = os.path.join('exam-ticiu2', 'index.html')
os.makedirs('exam-ticiu2', exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(out)
print(f'✅ {out}  {sz:,} bytes ({sz/1024:.1f} KB)')
print(f'   共 {len(questions)} 題，{total_cat} 類')
card_n = html.count('class="card"')
sec_n  = html.count('category-section')
print(f'   card 數: {card_n}，section 數: {sec_n}')
