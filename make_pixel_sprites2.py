"""
對所有 sprite_*.png 做去背 + 點陣圖化，輸出 px_{key}.png
"""
import os, glob
from PIL import Image
from io import BytesIO
import rembg

SRC_DIR = r"C:\Users\北興\Desktop\claude-ai"

# key → 來源 sprite 檔名前綴
KEY_MAP = {
    "zhuge":    "sprite_zhuge",
    "simayi":   "sprite_simayi",
    "simashi":  "sprite_simashi",
    "simazhao": "sprite_simazhao",
    "tongziA":  "sprite_tongziA",
    "tongziB":  "sprite_tongziB",
    "zhaoYun":  "sprite_zhaoYun",
    "jiangWei": "sprite_jiangWei",
    "maDai":    "sprite_maDai",
    "zhangHe":  "sprite_zhangHe",
    "dengAi":   "sprite_dengAi",
}

PIXEL_W, PIXEL_H = 32, 40
OUT_W,   OUT_H   = 96, 120

def find_latest(prefix):
    """找最新的 sprite_{key}_*.png"""
    pattern = os.path.join(SRC_DIR, f"{prefix}_*.png")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def process(key, prefix):
    src = find_latest(prefix)
    if not src:
        print(f"  ⚠ 找不到 {prefix}_*.png，跳過")
        return
    out = os.path.join(SRC_DIR, f"px_{key}.png")
    print(f"  {key} ({os.path.basename(src)}) ...", end=" ")

    with open(src, "rb") as f:
        img_bytes = f.read()

    # 去背
    removed = rembg.remove(img_bytes)
    img = Image.open(BytesIO(removed)).convert("RGBA")

    # 裁切有效區域
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # 點陣化：縮小 → NEAREST 放大
    small = img.resize((PIXEL_W, PIXEL_H), Image.LANCZOS)
    big   = small.resize((OUT_W, OUT_H), Image.NEAREST)

    big.save(out, "PNG")
    print(f"OK")

print("=== 去背 + 點陣化 ===")
for key, prefix in KEY_MAP.items():
    try:
        process(key, prefix)
    except Exception as e:
        print(f"  ✗ {key}: {e}")
print("=== 完成 ===")
