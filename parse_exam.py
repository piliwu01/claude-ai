import re, json

with open("exam_full.txt", encoding="utf-8") as f:
    raw = f.read()

# 擷取兩大節
section1_match = re.search(r'一、基礎語文知識題.*?(?=二、課文文意理解)', raw, re.S)
section2_match = re.search(r'二、課文文意理解.*$', raw, re.S)

def parse_questions(text, section_name):
    # 切分每一題：以 (　　) 開頭
    parts = re.split(r'(?=\(　　\))', text)
    questions = []
    for part in parts:
        part = part.strip()
        if not part.startswith('(　　)'):
            continue
        # 移除 (　　) 開頭
        part = part[4:].strip()

        # 擷取答案
        ans_match = re.search(r'答案：\(([ＡＢＣＤ])\)', part)
        if not ans_match:
            continue
        answer = ans_match.group(1)

        # 擷取解析
        exp_match = re.search(r'解析：(.+)$', part, re.S)
        explanation = exp_match.group(1).strip() if exp_match else ''

        # 取題目本體（到 (Ａ) 之前）
        q_match = re.match(r'^(.+?)(?=\(Ａ\))', part, re.S)
        if not q_match:
            continue
        question = q_match.group(1).strip()

        # 取選項
        opts_text = part[q_match.end():]
        opts_text = re.sub(r'答案：.*$', '', opts_text, flags=re.S).strip()

        opt_a = re.search(r'\(Ａ\)(.+?)(?=\(Ｂ\)|$)', opts_text, re.S)
        opt_b = re.search(r'\(Ｂ\)(.+?)(?=\(Ｃ\)|$)', opts_text, re.S)
        opt_c = re.search(r'\(Ｃ\)(.+?)(?=\(Ｄ\)|$)', opts_text, re.S)
        opt_d = re.search(r'\(Ｄ\)(.+?)$', opts_text, re.S)

        options = {
            'A': opt_a.group(1).strip() if opt_a else '',
            'B': opt_b.group(1).strip() if opt_b else '',
            'C': opt_c.group(1).strip() if opt_c else '',
            'D': opt_d.group(1).strip() if opt_d else '',
        }

        questions.append({
            'section': section_name,
            'question': question,
            'options': options,
            'answer': answer,
            'explanation': explanation,
        })
    return questions

q1 = parse_questions(section1_match.group(), '基礎語文知識題')
q2 = parse_questions(section2_match.group(), '課文文意理解')
all_q = q1 + q2

# 分類函式（只用題目文字＋選項，不用解析，避免反例污染）
def categorize(q):
    q_text = q['question'] + ''.join(q['options'].values())

    # 柬帖知識（優先，因為常在題目出現）
    if any(k in q_text for k in ['柬帖','請柬','喜帖','邀請卡','必要項目','發帖','收帖','餞行','洗塵']):
        return '柬帖知識'

    # 題辭概念定義
    if any(k in q_text for k in ['題辭的分類','撰寫要領','題辭的功能','題辭的載體','春聯','日月潭','大成殿']):
        return '題辭概念'

    # 哀輓類
    if any(k in q_text for k in ['告別式','輓聯','喪幛','喪禮','過世','逝世','罹難','哀悼','花圈','驟背','祭孔','往生']):
        return '哀輓題辭'

    # 壽誕類（在哀輓前判斷）
    if any(k in q_text for k in ['壽宴','祝壽','生日','壽誕','七十歲','壽辭','七十大壽','長壽','祝賀父親','友藏爺爺']):
        return '壽誕題辭'
    if any(k in q_text for k in ['南極騰輝','樹茂椿庭','松鶴延齡','蟠桃獻壽','椿萱並茂','萬壽無疆','南極星輝']):
        return '壽誕題辭'

    # 比賽類
    if any(k in q_text for k in ['比賽','演說比賽','演講比賽','書法比賽','作文比賽','歌唱比賽','音樂比賽','優勝','冠軍','奪冠','游泳','田徑','射箭','網球','運動']):
        return '比賽題辭'

    # 開業類
    if any(k in q_text for k in ['開業','開張','診所','餐館','餐廳','書局','銀行','旅館','民宿','醫院開業','店舖','新店','開幕','書店','學術論文發表','簽名會']):
        return '開業題辭'

    # 婚嫁類
    if any(k in q_text for k in ['結婚','婚禮','婚宴','喜宴','訂婚','嫁女兒','嫁','文定','喜帖','歸寧','喜酒']):
        return '婚嫁題辭'

    # 生育類
    if any(k in q_text for k in ['生男','生女','生育','弄璋','弄瓦','麟兒','喜獲麟兒','千金','嬰','誕','瓜瓞綿綿','子孫']):
        return '生育題辭'

    # 搬遷類
    if any(k in q_text for k in ['搬家','新居','搬新家','遷居','孟母','大觀園']):
        return '搬遷題辭'

    # 師生/畢業類
    if any(k in q_text for k in ['老師','師長','教師節','畢業','謝師','學長','畢業紀念冊']):
        return '師生／畢業題辭'

    # 看解析補分類（二次機會）
    exp = q['explanation']
    if any(k in exp for k in ['壽誕','賀壽','祝壽','男壽','女壽','雙壽']):
        return '壽誕題辭'
    if any(k in exp for k in ['賀結婚','婚嫁']):
        return '婚嫁題辭'
    if any(k in exp for k in ['搬家','遷居','新居']):
        return '搬遷題辭'
    if any(k in exp for k in ['師長','師生']):
        return '師生／畢業題辭'

    return '題辭概念'

for q in all_q:
    q['category'] = categorize(q)

# 統計
from collections import Counter
cats = Counter(q['category'] for q in all_q)
for k, v in cats.most_common():
    print(f'{k}: {v}題')

print(f'\n共 {len(all_q)} 題')

with open('exam_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_q, f, ensure_ascii=False, indent=2)
print('已輸出 exam_data.json')
