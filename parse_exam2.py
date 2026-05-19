import re, json
from collections import Counter

with open('exam2_full.txt', encoding='utf-8') as f:
    raw = f.read()

# 切題
parts = re.split(r'(?=\(　　\))', raw)

# 偵測兩大節
def get_section(pos, text):
    before = text[:pos]
    if '二、課文文意理解' in before or '課文文意理解' in before:
        return '課文文意理解'
    return '基礎語文知識題'

questions = []
for part in parts:
    part = part.strip()
    if not part.startswith('(　　)'):
        continue
    body = part[4:].strip()

    ans_m = re.search(r'答案：\(([ＡＢＣＤABCDａｂｃｄ])\)', body)
    if not ans_m:
        continue
    answer = ans_m.group(1)
    answer = {'A':'Ａ','B':'Ｂ','C':'Ｃ','D':'Ｄ',
              'a':'Ａ','b':'Ｂ','c':'Ｃ','d':'Ｄ'}.get(answer, answer)

    exp_m = re.search(r'解析：(.+)$', body, re.S)
    explanation = exp_m.group(1).strip() if exp_m else ''

    q_m = re.match(r'^(.+?)(?=\s*[\(（][ＡAａ][\)）])', body, re.S)
    if not q_m:
        continue
    question = q_m.group(1).strip()

    opts_raw = body[q_m.end():]
    opts_raw = re.sub(r'答案：.*$', '', opts_raw, flags=re.S).strip()

    def get_opt(fw, hw):
        m = re.search(rf'[\(（][{fw}{hw}][\)）](.+?)(?=[\(（][ＡＢＣＤABCDａｂｃｄ][\)）]|$)', opts_raw, re.S)
        return m.group(1).strip() if m else ''

    options = {
        'Ａ': get_opt('Ａ','A'), 'Ｂ': get_opt('Ｂ','B'),
        'Ｃ': get_opt('Ｃ','C'), 'Ｄ': get_opt('Ｄ','D'),
    }

    questions.append({
        'question': question,
        'options': options,
        'answer': answer,
        'explanation': explanation,
    })

# 分類（以題幹+選項為主）
RULES = [
    ('木蘭詩／樂府詩', ['木蘭','樂府','可汗','朔氣','金柝','黃河','燕山','木蘭詩','花木蘭',
                        '爺孃','對鏡','明駝','尚書郎','策勳','賞賜','唧唧','機杼','軍帖',
                        '十二卷','朔氣傳','明月','願為','雄兔','雌兔','傍地走']),
    ('歲月跟著',       ['歲月跟著','犁耙','分針','時針','秒針','鐘面','生命的枷',
                        '十二月凋','種子正開始','天光雲影','老人眼角','永恆輪迴',
                        '青翠森林','兒童粲亮','馬蹄不停','貓爪偷偷','雍容的分針']),
    ('運動家的風度',   ['運動家','風度','威爾基','羅斯福','百米','賽跑','競選',
                        '勝固欣然','敗亦可喜','功敗垂成','功虧一簣','任重而道遠',
                        '君子無所爭','揖讓而升','言必信','超越勝敗','榮譽的失敗',
                        '光明正大的失敗','偷雞摸狗的成功','丹恆在考試','我輸了只怪',
                        '充實改進','抱怨過教材']),
    ('修辭',           ['修辭','比喻','排比','誇飾','摹寫','擬人','對偶','借代','層遞',
                        '映襯','設問','類疊','頂真','回文','轉化','視覺摹寫','聽覺摹寫',
                        '狀聲詞','狀聲','反問','疑問句','反面','問題的反面','懸問']),
    ('字音字形',       ['注音','字音','讀音','形似字','字形','音義','寫成國字','國字後',
                        '用字完全正確','用字有誤','部首','筆畫',
                        '何者音義','讀音相同','讀音不同','字義','「粲」','「抽」']),
    ('成語／詞語',     ['成語','詞語','缺空','填入','意思相近','語義','詞義','歇後語',
                        '「　」中的詞語','造詞','語詞','撲朔迷離','老驥伏櫪']),
    ('詞性文法',       ['詞性','名詞','動詞','副詞','形容詞','代詞','主語','述語','補語',
                        '賓語','虛詞','實詞','詞類','當副詞','當名詞','當形容詞',
                        '句型','複句','文法','語法','「之」字','作代詞']),
    ('為學',           ['為學','蜀之鄙','僧','貧富','學問之道','人之為學']),
]

def categorize(q):
    text = q['question'] + ''.join(q['options'].values())
    for cat, kws in RULES:
        if any(k in text for k in kws):
            return cat
    # 二次：含解析
    full = text + q['explanation']
    for cat, kws in RULES:
        if any(k in full for k in kws):
            return cat
    return '其他語文知識'

# 偵測大節（依題目在原文中的位置）
raw_pos = 0
for i, q in enumerate(questions, 1):
    q['id'] = i
    pos = raw.find(q['question'][:15], raw_pos)
    if pos != -1:
        q['section'] = get_section(pos, raw)
        raw_pos = pos
    else:
        q['section'] = '基礎語文知識題'
    q['category'] = categorize(q)

stats = Counter(q['category'] for q in questions)
print(f'共 {len(questions)} 題')
for k, v in stats.most_common():
    print(f'  {k}: {v} 題')

with open('exam2_data.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print('→ exam2_data.json')
