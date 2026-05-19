"""
從 插圖 資料夾處理：
1. char_*.png → intrude_*.png (400x600，亂入大圖)
2. sprite_*.png → spr_*.png (200x250，去背高品質戰鬥精靈)
"""
import os, glob, shutil
from PIL import Image
from io import BytesIO
import rembg

SRC = r'C:\Users\北興\Desktop\claude-ai\插圖'
DST = r'C:\Users\北興\Desktop\claude-ai'

# ── 1. 複製故事背景圖（直接用原檔）──────────────────
STORY_FILES = [
    'bg_jieting_20260429_095427.png',
    'kongchengji_defeat_20260429_093837.png',
    'kongchengji_empty_20260429_093835.png',
    'kongchengji_simayi_20260429_093745.png',
    'kongchengji_title_20260429_093759.png',
    'kongchengji_victory_20260429_093840.png',
    'kongchengji_zhugeliang_20260429_093800.png',
]
for f in STORY_FILES:
    src = os.path.join(SRC, f)
    dst = os.path.join(DST, f)
    if not os.path.exists(dst) and os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'  copied: {f}')

# ── 2. char_*.png → intrude_*.png (400x600，亂入大圖)──
CHAR_MAP = {
    'char_zhaoYun_20260429_095346.png':  'intrude_zhaoYun.png',
    'char_jiangWei_20260429_095346.png': 'intrude_jiangWei.png',
    'char_maDai_20260429_095351.png':    'intrude_maDai.png',
    'char_zhangHe_20260429_095455.png':  'intrude_zhangHe.png',
    'char_dengAi_20260429_095604.png':   'intrude_dengAi.png',
}
print('\n=== 武將亂入大圖（400x600）===')
for src_f, dst_f in CHAR_MAP.items():
    src = os.path.join(SRC, src_f)
    dst = os.path.join(DST, dst_f)
    if not os.path.exists(src):
        print(f'  ⚠ 找不到 {src_f}')
        continue
    print(f'  {dst_f}...', end=' ')
    img = Image.open(src).convert('RGBA')
    img = img.resize((400, 600), Image.LANCZOS)
    img.save(dst, 'PNG')
    print('OK')

# ── 3. sprite_*.png → spr_*.png (rembg去背 + 200x250)──
SPRITE_MAP = {
    'sprite_zhuge_20260429_160949.png':    'spr_zhuge.png',
    'sprite_simayi_20260429_160941.png':   'spr_simayi.png',
    'sprite_simashi_20260429_160954.png':  'spr_simashi.png',
    'sprite_simazhao_20260429_160956.png': 'spr_simazhao.png',
    'sprite_tongziA_20260429_160959.png':  'spr_tongziA.png',
    'sprite_tongziB_20260429_161001.png':  'spr_tongziB.png',
    'sprite_zhaoYun_20260429_161150.png':  'spr_zhaoYun.png',
    'sprite_jiangWei_20260429_161222.png': 'spr_jiangWei.png',
    'sprite_maDai_20260429_161304.png':    'spr_maDai.png',
    'sprite_zhangHe_20260429_161355.png':  'spr_zhangHe.png',
    'sprite_dengAi_20260429_161016.png':   'spr_dengAi.png',
}
print('\n=== 戰鬥精靈（去背 200x250）===')
for src_f, dst_f in SPRITE_MAP.items():
    src = os.path.join(SRC, src_f)
    dst = os.path.join(DST, dst_f)
    if not os.path.exists(src):
        print(f'  ⚠ 找不到 {src_f}')
        continue
    print(f'  {dst_f}...', end=' ')
    with open(src, 'rb') as f:
        img_bytes = f.read()
    removed = rembg.remove(img_bytes)
    img = Image.open(BytesIO(removed)).convert('RGBA')
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img = img.resize((200, 250), Image.LANCZOS)
    img.save(dst, 'PNG')
    print('OK')

print('\n=== 完成 ===')
