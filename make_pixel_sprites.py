"""
角色圖片處理：去背 + 像素化（點陣圖風格）
輸出：px_{key}.png  ← 去背後縮成 32x40 再放大到 96x120（NEAREST）
"""
import os
from PIL import Image
import rembg

SRC = r"C:\Users\北興\Desktop\claude-ai"
OUT = SRC   # 輸出到同一資料夾

# key → 來源檔名
CHARS = {
    "zhuge":   "kongchengji_zhugeliang_20260429_093800.png",
    "simayi":  "kongchengji_simayi_20260429_093745.png",
    "zhaoYun": "char_zhaoYun_20260429_095346.png",
    "jiangWei":"char_jiangWei_20260429_095346.png",
    "maDai":   "char_maDai_20260429_095351.png",
    "zhangHe": "char_zhangHe_20260429_095455.png",
    "dengAi":  "char_dengAi_20260429_095604.png",
    "tongziA": "char_tongziA_20260429_143625.png",
    "tongziB": "char_tongziB_20260429_143626.png",
    "weiA":    "char_weiA_20260429_143632.png",
    "weiB":    "char_weiB_20260429_143632.png",
}

# 點陣風格參數
PIXEL_W, PIXEL_H = 32, 40   # 先縮到這個低解析度（FC 精靈尺寸感）
OUT_W,   OUT_H   = 96, 120  # 再放大到此（NEAREST = 保留方塊感）

def process(key, filename):
    src_path = os.path.join(SRC, filename)
    out_path = os.path.join(OUT, f"px_{key}.png")

    print(f"  處理 {key} ...", end=" ")

    # 1. 讀檔
    with open(src_path, "rb") as f:
        img_bytes = f.read()

    # 2. rembg 去背
    removed = rembg.remove(img_bytes)

    # 3. 轉 PIL，確保 RGBA
    from io import BytesIO
    img = Image.open(BytesIO(removed)).convert("RGBA")

    # 4. 裁切：取有效像素的 bounding box，去除多餘透明邊
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # 5. 縮到低解析（LANCZOS 保細節），創造點陣底圖
    small = img.resize((PIXEL_W, PIXEL_H), Image.LANCZOS)

    # 6. 放大到輸出尺寸（NEAREST = 方塊像素感）
    big = small.resize((OUT_W, OUT_H), Image.NEAREST)

    # 7. 存檔
    big.save(out_path, "PNG")
    print(f"OK → px_{key}.png ({OUT_W}x{OUT_H})")

print("=== 開始處理 ===")
for key, fname in CHARS.items():
    src = os.path.join(SRC, fname)
    if not os.path.exists(src):
        print(f"  ⚠ 找不到 {fname}，跳過")
        continue
    try:
        process(key, fname)
    except Exception as e:
        print(f"  ✗ {key} 錯誤：{e}")

print("=== 全部完成 ===")
