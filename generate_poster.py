#!/usr/bin/env python3
"""
Meridian Fields — Poster Generator (Refined)
Design Philosophy: Cartographic Resonance
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

random.seed(7)

# === CANVAS ===
W, H = 2400, 3360
img = Image.new('RGB', (W, H), (8, 9, 27))
draw = ImageDraw.Draw(img)

# === COLOR PALETTE ===
BG      = (8, 9, 27)
WARM_W  = (228, 222, 205)
DIM     = (52, 58, 92)
FAINT   = (20, 22, 40)
GOLD    = (194, 156, 68)
GOLD_D  = (88, 68, 26)
ALMOST  = (22, 24, 44)

# === FOCAL CENTER ===
cx = W // 2
cy = int(H * 0.468)

# ─────────────────────────────────────────────────────────
# 1. BACKGROUND: Refined dot field — denser, varies by zone
# ─────────────────────────────────────────────────────────
for gx in range(48, W, 62):
    for gy in range(48, H, 62):
        d = math.hypot(gx - cx, gy - cy)
        jx = gx + random.randint(-3, 3)
        jy = gy + random.randint(-3, 3)
        # Outside big ring: very faint; inside: slightly more visible
        if d < 820:
            v = max(18, int(52 - d * 0.028))
        else:
            v = max(12, int(22 - (d - 820) * 0.008))
        col = (v, v + 3, v + 16)
        draw.ellipse([jx - 1, jy - 1, jx + 1, jy + 1], fill=col)

# ─────────────────────────────────────────────────────────
# 2. VIGNETTE LAYER (darkens edges for depth)
# ─────────────────────────────────────────────────────────
vig = Image.new('RGB', (W, H), (0, 0, 0))
vdraw = ImageDraw.Draw(vig)
steps = 80
for i in range(steps):
    alpha = int(120 * (1 - i / steps) ** 2)
    col_v = (alpha, alpha, alpha)
    # Top/bottom bands
    vdraw.rectangle([0, 0, W, int(H * (i / steps) * 0.5)], fill=col_v)
from PIL import ImageChops
# Manual vignette by darkening corners with radial falloff
vg = Image.new('RGB', (W, H), (8, 9, 27))
vg_draw = ImageDraw.Draw(vg)
# Draw a large bright center circle on vignette layer
cx_v, cy_v = W // 2, H // 2
for r in range(min(W, H) // 2, 0, -8):
    brightness = min(255, int(255 * (1 - r / (min(W, H) / 2)) ** 0.5))
    col_vig = (brightness, brightness, brightness)
    vg_draw.ellipse([cx_v - r, cy_v - r, cx_v + r, cy_v + r], outline=col_vig, width=8)

vg = vg.filter(ImageFilter.GaussianBlur(radius=60))
# Blend: multiply img with vignette
img_arr = img.convert('RGB')
# Simple composite: darken corners
from PIL import ImageEnhance
# Skip complex vignette, just proceed with main render on our img

# ─────────────────────────────────────────────────────────
# 3. CONCENTRIC RINGS — precise, crisp
# ─────────────────────────────────────────────────────────
rings = [
    (820, WARM_W, 2),
    (640, DIM,    1),
    (462, DIM,    1),
    (282, (60, 66, 106), 1),
    (112, DIM,    1),
    (38,  (36, 40, 68),  1),
]
for r, col, w in rings:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)

# ─────────────────────────────────────────────────────────
# 4. RADIAL LINES
# ─────────────────────────────────────────────────────────
r0, r1 = 112, 820
for deg in range(0, 360, 10):
    a = math.radians(deg)
    x1 = cx + r0 * math.cos(a)
    y1 = cy + r0 * math.sin(a)
    x2 = cx + r1 * math.cos(a)
    y2 = cy + r1 * math.sin(a)
    if deg % 90 == 0:
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)
    elif deg % 30 == 0:
        draw.line([(x1, y1), (x2, y2)], fill=DIM, width=1)
    else:
        draw.line([(x1, y1), (x2, y2)], fill=FAINT, width=1)

# ─────────────────────────────────────────────────────────
# 5. CROSS HAIRS (full canvas — very soft)
# ─────────────────────────────────────────────────────────
draw.line([(0, cy), (W, cy)], fill=(18, 20, 38), width=1)
draw.line([(cx, 0), (cx, H)], fill=(18, 20, 38), width=1)

# ─────────────────────────────────────────────────────────
# 6. CENTER ANCHOR
# ─────────────────────────────────────────────────────────
draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=GOLD, width=1)
draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)

# ─────────────────────────────────────────────────────────
# 7. TICK MARKS around outer ring
# ─────────────────────────────────────────────────────────
for deg in range(0, 360, 5):
    a = math.radians(deg)
    if deg % 90 == 0:
        r_in, r_out, col, w = 820, 854, GOLD, 2
    elif deg % 45 == 0:
        r_in, r_out, col, w = 820, 844, DIM, 1
    elif deg % 10 == 0:
        r_in, r_out, col, w = 820, 836, DIM, 1
    else:
        r_in, r_out, col, w = 820, 830, FAINT, 1
    x1 = cx + int(r_in * math.cos(a))
    y1 = cy + int(r_in * math.sin(a))
    x2 = cx + int(r_out * math.cos(a))
    y2 = cy + int(r_out * math.sin(a))
    draw.line([(x1, y1), (x2, y2)], fill=col, width=w)

# ─────────────────────────────────────────────────────────
# 8. HORIZONTAL BAND RULES
# ─────────────────────────────────────────────────────────
for y_frac, gap in [(0.108, 10), (0.876, 10)]:
    y = int(H * y_frac)
    draw.line([(108, y),       (W - 108, y)],       fill=DIM,    width=1)
    draw.line([(108, y + gap), (W - 108, y + gap)], fill=ALMOST, width=1)

# ─────────────────────────────────────────────────────────
# 9. CORNER REGISTRATION MARKS
# ─────────────────────────────────────────────────────────
for rx, ry in [(115, 115), (W - 115, 115), (115, H - 115), (W - 115, H - 115)]:
    draw.line([(rx - 52, ry), (rx + 52, ry)], fill=GOLD_D, width=1)
    draw.line([(rx, ry - 52), (rx, ry + 52)], fill=GOLD_D, width=1)
    draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=GOLD_D)

# ─────────────────────────────────────────────────────────
# 10. TYPOGRAPHY
# ─────────────────────────────────────────────────────────
fdir = r'C:\Users\北興\.claude\skills\canvas-design\canvas-fonts'

def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(fdir, name), size)
    except Exception as e:
        print(f"Font warning: {e}")
        return ImageFont.load_default()

f_title  = load_font('Jura-Light.ttf',            185)
f_sub    = load_font('InstrumentSans-Regular.ttf', 52)
f_label  = load_font('GeistMono-Regular.ttf',      32)
f_degree = load_font('GeistMono-Regular.ttf',      27)
f_coord  = load_font('GeistMono-Regular.ttf',      24)

def ctext(text, y, font, color):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

def spaced_text(text, y, font, color, letter_spacing=18):
    """Draw text with manual letter spacing."""
    total_w = 0
    char_widths = []
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=font)
        cw = bb[2] - bb[0]
        char_widths.append(cw)
        total_w += cw + letter_spacing
    total_w -= letter_spacing
    x = (W - total_w) // 2
    for i, ch in enumerate(text):
        draw.text((x, y), ch, fill=color, font=font)
        x += char_widths[i] + letter_spacing

# — Title: MERIDIAN (letter-spaced)
title_y = int(H * 0.052)
spaced_text("MERIDIAN", title_y, f_title, WARM_W, letter_spacing=22)

title_h = draw.textbbox((0, 0), "M", font=f_title)[3]

# — Sub: F I E L D S
sub_y = title_y + title_h + 24
spaced_text("F I E L D S", sub_y, f_sub, GOLD, letter_spacing=14)

# — Bottom classification
ctext(
    "CARTOGRAPHIC  RESONANCE  ·  VOL. I",
    int(H * 0.893),
    f_label,
    (65, 72, 110)
)

# — Degree labels at 45° intervals around outer ring
for deg in range(0, 360, 45):
    a = math.radians(deg - 90)  # 0° at top
    r_lbl = 908
    lx = cx + int(r_lbl * math.cos(a))
    ly = cy + int(r_lbl * math.sin(a))
    label = f"{deg:03d}°"
    bb = draw.textbbox((0, 0), label, font=f_degree)
    lw = bb[2] - bb[0]
    lh = bb[3] - bb[1]
    draw.text((lx - lw // 2, ly - lh // 2), label, fill=GOLD_D, font=f_degree)

# — Compass labels (N/E/S/W) inside small inner ring
for txt, dx, dy in [("N", 0, -136), ("E", 140, 0), ("S", 0, 140), ("W", -148, 0)]:
    bb = draw.textbbox((0, 0), txt, font=f_coord)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text((cx + dx - tw // 2, cy + dy - th // 2), txt,
              fill=(52, 58, 88), font=f_coord)

# ─────────────────────────────────────────────────────────
# 11. SUBTLE ARC DASHES on mid ring (NE + SW)
# ─────────────────────────────────────────────────────────
def arc_dashes(center_x, center_y, radius, start_deg, end_deg, color, n=10):
    step = (end_deg - start_deg) / (n * 2)
    for i in range(n):
        a0 = math.radians(start_deg + i * 2 * step)
        a1 = math.radians(start_deg + i * 2 * step + step)
        pts = [
            (center_x + radius * math.cos(a0), center_y + radius * math.sin(a0)),
            (center_x + radius * math.cos((a0 + a1) / 2), center_y + radius * math.sin((a0 + a1) / 2)),
            (center_x + radius * math.cos(a1), center_y + radius * math.sin(a1)),
        ]
        draw.line(pts, fill=color, width=1)

arc_dashes(cx, cy, 640, -78, -12,  (58, 64, 98), 8)
arc_dashes(cx, cy, 640, 102, 168,  (58, 64, 98), 8)

# ─────────────────────────────────────────────────────────
# 12. SUBTLE CORNER VIGNETTE (only darkens the 4 corners)
# ─────────────────────────────────────────────────────────
import numpy as np
img_np = np.array(img, dtype=np.float32)
ys = np.linspace(0, 1, H)
xs = np.linspace(0, 1, W)
xg, yg = np.meshgrid(xs, ys)
# Distance from center (normalized)
dist = np.sqrt((xg - 0.5) ** 2 + (yg - 0.5) ** 2) / 0.707
# Vignette factor: 1.0 at center, ~0.82 at corners
vignette = np.clip(1.0 - dist ** 3 * 0.35, 0.75, 1.0)
vignette = vignette[:, :, np.newaxis]
out_np = np.clip(img_np * vignette, 0, 255).astype(np.uint8)
img = Image.fromarray(out_np)

# ─────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────
out_path = r'C:\Users\北興\Desktop\claude-ai\meridian_fields_poster.png'
img.save(out_path, 'PNG', dpi=(300, 300))
print(f"✅ 海報儲存：{out_path}")
print(f"   尺寸：{W} × {H} px")
