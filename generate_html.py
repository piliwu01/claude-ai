import json

with open('exam_data.json', encoding='utf-8') as f:
    questions = json.load(f)

# 類別順序與 emoji
CATEGORIES = [
    ('婚嫁題辭',   '💍'),
    ('壽誕題辭',   '🎂'),
    ('哀輓題辭',   '🕯️'),
    ('生育題辭',   '👶'),
    ('比賽題辭',   '🏆'),
    ('開業題辭',   '🏪'),
    ('搬遷題辭',   '🏠'),
    ('師生／畢業題辭', '🎓'),
    ('柬帖知識',   '📜'),
    ('題辭概念',   '📖'),
]

# 按類別分組
from collections import defaultdict
groups = defaultdict(list)
for i, q in enumerate(questions, 1):
    q['id'] = i
    groups[q['category']].append(q)

# 生成題目卡片 HTML
def opt_label(letter):
    return {'A':'Ａ','B':'Ｂ','C':'Ｃ','D':'Ｄ'}.get(letter, letter)

def render_card(q, cat_idx, q_idx):
    qid = f'q{q["id"]}'
    correct = q['answer']
    opts_html = ''
    for letter in ['A','B','C','D']:
        val = q['options'].get(letter, '')
        if not val:
            continue
        opts_html += f'<div class="option" data-letter="{letter}">（{opt_label(letter)}）{val}</div>\n'

    section_tag = f'<span class="section-tag">{q["section"]}</span>'

    return f'''<div class="card" id="{qid}" onclick="toggleCard('{qid}')">
  <div class="card-header">
    <span class="q-num">第 {q["id"]} 題</span>
    {section_tag}
    <span class="expand-icon">＋</span>
  </div>
  <div class="q-text">{q["question"]}</div>
  <div class="card-body" id="body-{qid}">
    <div class="options" id="opts-{qid}">
{opts_html}    </div>
    <button class="show-ans-btn" onclick="showAnswer(event, '{qid}', '{correct}')">顯示答案</button>
    <div class="answer-block" id="ans-{qid}" style="display:none">
      <div class="answer-line">正確答案：<strong>（{opt_label(correct)}）</strong> {q["options"].get(correct, '')}</div>
      <div class="explanation">💡 {q["explanation"]}</div>
    </div>
  </div>
</div>'''

# 生成各類別 section
sections_html = ''
for cat_name, emoji in CATEGORIES:
    qs = groups.get(cat_name, [])
    if not qs:
        continue
    cards_html = '\n'.join(render_card(q, 0, i) for i, q in enumerate(qs))
    safe_id = cat_name.replace('／','_').replace('/','_')
    sections_html += f'''
<section class="category-section" id="cat-{safe_id}">
  <h2 class="cat-title">{emoji} {cat_name} <span class="count">({len(qs)} 題)</span></h2>
  <div class="cards-row">
{cards_html}
  </div>
</section>
'''

# 生成導覽按鈕
nav_html = ''
for cat_name, emoji in CATEGORIES:
    qs = groups.get(cat_name, [])
    if not qs:
        continue
    safe_id = cat_name.replace('／','_').replace('/','_')
    nav_html += f'<button class="nav-btn" onclick="scrollTo_(\'{safe_id}\')">{emoji} {cat_name}</button>\n'

html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>114學年度國中國文測驗－題辭與柬帖互動練習</title>
<style>
:root {{
  --bg: #f0f4f8;
  --card-bg: #fff;
  --primary: #2563eb;
  --primary-light: #dbeafe;
  --green: #16a34a;
  --green-light: #dcfce7;
  --text: #1e293b;
  --sub: #64748b;
  --border: #e2e8f0;
  --shadow: 0 2px 8px rgba(0,0,0,.08);
  --radius: 12px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: '微軟正黑體', 'Microsoft JhengHei', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
}}

/* 頁首 */
.hero {{
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: #fff;
  padding: 2.5rem 1.5rem 2rem;
  text-align: center;
}}
.hero h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: .05em; }}
.hero p {{ margin-top: .5rem; font-size: .95rem; opacity: .85; }}
.hero .stats {{
  margin-top: 1rem;
  display: flex; justify-content: center; gap: 2rem;
  font-size: .9rem;
}}
.hero .stat {{ background: rgba(255,255,255,.15); border-radius: 8px; padding: .4rem 1rem; }}

/* 導覽列 */
.nav-bar {{
  position: sticky; top: 0; z-index: 100;
  background: #fff;
  border-bottom: 1px solid var(--border);
  padding: .6rem 1rem;
  display: flex; flex-wrap: wrap; gap: .5rem;
  box-shadow: 0 2px 6px rgba(0,0,0,.06);
}}
.nav-btn {{
  background: var(--primary-light);
  color: var(--primary);
  border: none;
  border-radius: 20px;
  padding: .35rem .85rem;
  font-size: .85rem;
  font-family: inherit;
  cursor: pointer;
  transition: .15s;
  white-space: nowrap;
}}
.nav-btn:hover {{ background: var(--primary); color: #fff; }}

/* 主體 */
main {{ padding: 1.5rem 1rem 3rem; max-width: 1400px; margin: 0 auto; }}

/* 類別標題 */
.category-section {{ margin-bottom: 2.5rem; }}
.cat-title {{
  font-size: 1.2rem; font-weight: 700;
  color: var(--primary);
  margin-bottom: 1rem;
  padding-left: .75rem;
  border-left: 4px solid var(--primary);
}}
.cat-title .count {{ font-size: .85rem; color: var(--sub); font-weight: 400; }}

/* 橫向捲動行 */
.cards-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}}

/* 題目卡片 */
.card {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  width: 320px;
  cursor: pointer;
  transition: box-shadow .2s, border-color .2s;
  overflow: hidden;
}}
.card:hover {{ box-shadow: 0 4px 16px rgba(37,99,235,.13); border-color: #93c5fd; }}
.card.active {{ border-color: var(--primary); }}

.card-header {{
  display: flex; align-items: center; gap: .5rem;
  padding: .75rem 1rem .5rem;
}}
.q-num {{
  font-size: .75rem; font-weight: 700;
  background: var(--primary); color: #fff;
  border-radius: 20px; padding: .15rem .6rem;
  white-space: nowrap;
}}
.section-tag {{
  font-size: .7rem;
  background: #f1f5f9; color: var(--sub);
  border-radius: 20px; padding: .1rem .5rem;
  white-space: nowrap;
}}
.expand-icon {{
  margin-left: auto;
  font-size: 1.2rem; color: var(--sub);
  transition: transform .2s;
  line-height: 1;
}}
.card.active .expand-icon {{ transform: rotate(45deg); color: var(--primary); }}

.q-text {{
  font-size: .9rem;
  padding: 0 1rem .75rem;
  color: var(--text);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: all .2s;
}}
.card.active .q-text {{
  -webkit-line-clamp: unset;
  overflow: visible;
}}

/* 展開內容 */
.card-body {{
  display: none;
  padding: 0 1rem 1rem;
  border-top: 1px dashed var(--border);
  margin-top: .25rem;
  padding-top: .75rem;
}}
.card.active .card-body {{ display: block; }}

.options {{ margin-bottom: .75rem; }}
.option {{
  font-size: .85rem;
  padding: .3rem .5rem;
  border-radius: 6px;
  margin-bottom: .25rem;
  background: #f8fafc;
}}
.option.correct {{ background: var(--green-light); color: var(--green); font-weight: 600; }}
.option.wrong {{ background: #fef2f2; color: #dc2626; text-decoration: line-through; opacity: .7; }}

.show-ans-btn {{
  width: 100%;
  background: var(--green);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: .5rem;
  font-size: .9rem;
  font-family: inherit;
  cursor: pointer;
  transition: .15s;
}}
.show-ans-btn:hover {{ background: #15803d; }}
.show-ans-btn:disabled {{ background: #94a3b8; cursor: default; }}

.answer-block {{ margin-top: .75rem; }}
.answer-line {{
  font-size: .9rem;
  background: var(--green-light);
  color: var(--green);
  border-radius: 8px;
  padding: .5rem .75rem;
  margin-bottom: .5rem;
}}
.explanation {{
  font-size: .82rem;
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
  color: #92400e;
  padding: .5rem .75rem;
  border-radius: 0 6px 6px 0;
  line-height: 1.6;
}}

/* 頁尾 */
footer {{
  text-align: center;
  padding: 1.5rem;
  font-size: .8rem;
  color: var(--sub);
  border-top: 1px solid var(--border);
}}

@media (max-width: 600px) {{
  .card {{ width: 100%; }}
  .hero h1 {{ font-size: 1.2rem; }}
  .hero .stats {{ gap: .75rem; }}
}}
</style>
</head>
<body>

<div class="hero">
  <h1>114 學年度國中國文測驗</h1>
  <p>題辭與柬帖互動練習卷（含解析）</p>
  <div class="stats">
    <div class="stat">📝 共 {len(questions)} 題</div>
    <div class="stat">🗂️ 共 {len([c for c,e in CATEGORIES if groups.get(c)])} 大類</div>
    <div class="stat">💡 含詳細解析</div>
  </div>
</div>

<nav class="nav-bar">
{nav_html}
</nav>

<main>
{sections_html}
</main>

<footer>114 學年度國中國文 · 點擊題目展開 · 點擊「顯示答案」查看解析</footer>

<script>
function toggleCard(qid) {{
  const card = document.getElementById(qid);
  card.classList.toggle('active');
}}

function showAnswer(e, qid, correct) {{
  e.stopPropagation();
  const ansBlock = document.getElementById('ans-' + qid);
  const btn = e.target;
  const optsDiv = document.getElementById('opts-' + qid);

  ansBlock.style.display = 'block';
  btn.disabled = true;
  btn.textContent = '已顯示答案';

  // 標記選項顏色
  optsDiv.querySelectorAll('.option').forEach(opt => {{
    const letter = opt.getAttribute('data-letter');
    if (letter === correct) {{
      opt.classList.add('correct');
    }} else {{
      opt.classList.add('wrong');
    }}
  }});
}}

function scrollTo_(safeid) {{
  const el = document.getElementById('cat-' + safeid);
  if (el) el.scrollIntoView({{behavior: 'smooth', block: 'start'}});
}}
</script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html 生成完成！')
