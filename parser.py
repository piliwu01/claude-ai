import warnings
warnings.filterwarnings("ignore")

import os
import re
import json
import pdfplumber
import openpyxl

DAYS = ['一', '二', '三', '四', '五']

# 不計入科別推算的雜項科目
_SKIP = {'班會', '本土語言', '選手培訓', '選培', '本土讀者', '導師', ''}


# 課表科目名稱 → 正式科別名稱
_SUBJ_TO_DEPT = {
    '國文': '國文', '英語': '英語', '英文': '英語',
    '數學': '數學', '生物': '生物', '理化': '理化',
    '地科': '地科', '地球科學': '地科',
    '歷史': '歷史', '地理': '地理', '公民': '公民',
    '健康': '健康', '體育': '體育', '美術': '美術',
    '音樂': '音樂', '輔導': '輔導', '電腦': '電腦',
    '資訊': '電腦', '家政': '家政', '工藝': '工藝',
    '生活科技': '生活科技', '科技': '生活科技',
    '寫作魔法師': '國文',
}


def _strip_fu(subject):
    """去掉科目名稱中的 .輔 / ．輔 / 輔 後綴"""
    return re.sub(r'[.．]?輔$', '', subject).strip()


def _derive_dept(schedule):
    """從實際課表推算科別：取出現最多次的核心科目"""
    counter = {}
    for entries in schedule.values():
        for e in entries:
            subj = _strip_fu(e['科目'])
            if subj in _SKIP or '導師' in subj:
                continue
            counter[subj] = counter.get(subj, 0) + 1
    if not counter:
        return ''
    top = max(counter, key=counter.get)
    return _SUBJ_TO_DEPT.get(top, top)


def parse_subject_map(excel_path):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['工作表1']
    subject_map = {}
    for row in ws.iter_rows(values_only=True):
        if row[0] and str(row[0]).startswith('_'):
            subj = str(row[0])[3:]  # 去掉 _01 等前綴，保留 "國文"
            for name in row[1:]:
                if name:
                    subject_map[str(name).strip()] = subj
    return subject_map


def parse_teacher_name(text):
    for line in text.strip().split('\n')[:5]:
        m = re.match(r'^\d{3}\s+(\S+)', line)
        if m:
            return m.group(1)
    return None


def parse_cell(cell_text):
    """解析單格內容，例如 '國文\n202 兼' → (科目, 班級, 兼課)"""
    if not cell_text or not cell_text.strip():
        return None
    parts = cell_text.strip().split('\n')
    subject = parts[0].strip()
    if not subject:
        return None

    class_num = ''
    is_jian = False

    week_type = ''  # '', '單週', '雙週'

    if len(parts) >= 2:
        class_part = parts[1].strip()
        is_jian = '兼' in class_part
        if '單週' in class_part:
            week_type = '單週'
        elif '雙週' in class_part:
            week_type = '雙週'
        class_clean = (class_part
                       .replace('兼', '')
                       .replace('單週', '')
                       .replace('雙週', '')
                       .strip())
        # 班級號碼為 2-3 位數字
        if re.match(r'^\d{2,3}$', class_clean):
            class_num = class_clean

    return {
        'subject': subject,
        'class': class_num,
        'is_jian': is_jian,
        'week_type': week_type,
    }


def parse_pdf(pdf_path, excel_path, progress_callback=None):
    subject_map = parse_subject_map(excel_path)
    result = {}

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            if progress_callback:
                progress_callback(i + 1, total)

            text = page.extract_text() or ''
            teacher = parse_teacher_name(text)
            if not teacher:
                continue

            tables = page.extract_tables()
            if not tables:
                continue

            table = tables[0]
            # table[0] = ['', '', '星期一', '星期二', '星期三', '星期四', '星期五']
            # table[1:] = 各節資料

            schedule = {day: [] for day in DAYS}

            for row in table[1:]:
                period_str = (row[0] or '').strip()
                if not period_str.isdigit():
                    continue
                period = int(period_str)

                for day_idx, day in enumerate(DAYS):
                    col_idx = day_idx + 2
                    if col_idx >= len(row):
                        continue
                    parsed = parse_cell(row[col_idx])
                    if parsed:
                        schedule[day].append({
                            '節次': period,
                            '科目': _strip_fu(parsed['subject']),  # 去掉 .輔
                            '班級': parsed['class'],
                            '兼課': parsed['is_jian'],
                            '週別': parsed['week_type'],
                        })

            # 科別：PDF 推算 > 工作表1（覆蓋在載入快取後用 apply_overrides 套用）
            dept = _derive_dept(schedule) or subject_map.get(teacher, '')
            result[teacher] = {
                '科別': dept,
                'schedule': schedule,
            }

    return result


def load_overrides(overrides_path):
    if os.path.exists(overrides_path):
        with open(overrides_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_overrides(overrides, overrides_path):
    with open(overrides_path, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, ensure_ascii=False, indent=2)


def apply_overrides(schedule_data, overrides):
    """將覆蓋設定套用到已載入的課表資料（直接修改）"""
    for teacher, dept in overrides.items():
        if teacher in schedule_data:
            schedule_data[teacher]['科別'] = dept


def save_cache(data, cache_path):
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_cache(cache_path):
    with open(cache_path, 'r', encoding='utf-8') as f:
        return json.load(f)
