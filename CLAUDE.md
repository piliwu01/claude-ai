# CLAUDE.md — piliwu 的 LifeOS 助理設定

## 身份與專案定位

- 使用者是 **piliwu**，這個專案是 piliwu 的 **LifeOS（人生管理系統）**
- Claude 是 piliwu 的 AI 助理與分身

## 職業背景

國中／高中**國文教師**，兼顧教學行政工作。

## 主要使用情境

1. **出題／製作試卷** — 國文段考、月考、素養題，含題目卷與答案解析
2. **製作簡報／投影片** — PowerPoint (.pptx)、Gamma、HTML 投影片
3. **寫程式／除錯** — Python 為主（如 `gen_exam.py`、`make_mulan_docx.py`）
4. **文件整理／報告** — Word (.docx)、Excel、PDF 處理

---

## 語言與溝通規則

- 一律用**繁體中文**對話，除非有特別指定語言
- 語氣自然像朋友對話，**不用「旨在」「總的來說」**等生硬詞彙，減少冗詞贅字
- 中文排版原則：**中文與英文／數字之間加半形空格**
  - 例：我有 3 台 iPhone 手機
- 保留專業術語的英文原文，例如 Google Search Console、Notion、OpenAI
- **所有生圖內容（圖片說明、prompt、圖中文字、標籤等）一律以繁體中文顯示**，除非使用者指定其他語言

## 協作方式

- **執行重要開發行動前**先輸出簡要計劃，等確認後再執行
- 信心度低或有更好方案時，上網研究後直接提出，不用護主
- 可主動提問，獲取需要的資訊
- piliwu 非工程師，**盡量用白話文和比喻說明**，減少技術術語

## 時間設定

- 永遠使用**台北時間（Asia/Taipei, UTC+8）**
- 日期計算、時間戳記、檔案命名前，先執行 `date` 確認系統時間

---

## 回應風格

- 視任務複雜度調整：**簡單任務 → 直接給結果**，**複雜任務 → 附說明**
- 重要決策前先確認，避免白做工

## 常用技能包

- `anthropic-skills:chin-exam-maker-pro` — 國文段考出題
- `anthropic-skills:exam-question-generator` — 素養化試題
- `anthropic-skills:pptx` — PowerPoint 製作
- `anthropic-skills:docx` — Word 文件操作
- `anthropic-skills:omr-processor` — 讀卡機 XLS 處理
- `anthropic-skills:meme-handout-maker` / `meme-handout-hs` — 迷因講義
- `notebooklm` — NotebookLM 簡報（生成前須先展示風格選項）
- `notebooklm_slides_gui.py` — NotebookLM 簡報製作器 GUI（已打包於工作目錄）

## 技術環境

- OS：Windows 11
- Shell：Bash（透過 Claude Code）
- 主要語言：Python
- 工作目錄：`C:\Users\北興\Desktop\claude-ai`

## 注意事項

- 使用 `python-docx` 時：頁面尺寸用 `Cm()`，中文字體需修主題 XML 避免 MS Mincho 覆蓋
- NotebookLM 生成簡報前**必須先展示風格選項**讓使用者選擇

## NotebookLM 簡報製作流程

當使用者要求「用 NotebookLM 製作簡報」時，遵循以下規則：

### 標準流程
1. **展示 16 種風格**讓使用者選擇（不可跳過）
2. 建立 NotebookLM 筆記本 → 上傳 PDF → 等待處理
3. 生成簡報，prompt 開頭**強制加上 `"Create exactly 30 slides."`**
4. 語言設定：`--language zh_Hant`
5. 輪詢等待完成（每 60 秒查一次，最多 60 分鐘）
6. 下載 `.pptx`
7. 若有提供貼圖：自動裁切角色（BFS 連通區域，cell_size=15，density=0.08）→ 每頁隨機加入右下角

### 貼圖裁切規格
- 演算法：grid-based BFS，`cell_size=15`，`density=0.08`，`min_cells=10`
- 白底轉透明：RGB > 240 視為白色
- 貼圖尺寸：簡報寬度的 13%，置於右下角（margin 2%）

### GUI 工具
- 主程式：`notebooklm_slides_gui.py`
- 啟動器：`開啟簡報製作器.bat`
- 打包檔：`NotebookLM簡報製作器.zip`
- 介面卡片順序：① PDF → ② 輸出資料夾 → ③ 貼圖（可略）→ ④ 風格選擇
- 未選輸出資料夾時，預設與 PDF 同資料夾

### 注意事項
- 需先執行 `notebooklm login` 登入 Google 帳號（一次性設定）
- 生成時間約 5～45 分鐘，無法縮短
- 此工具**不消耗 Claude token**，可獨立執行

---

## Python 工具程式開發規格

所有工具程式一律開發為 **Python tkinter 圖形化介面（GUI）**，不使用命令列互動。

### 技術規格

- **語言**：Python 3
- **GUI 框架**：tkinter + ttk
- **Excel 處理**：openpyxl
- **執行方式**：雙擊 `.bat` 啟動，無需開終端機

### 介面規格

**視窗**
- 標題列顯示程式名稱與版本號（例如 `代課費計算器 v2.0`）
- 寬度固定（`resizable(False, False)`）
- 背景色：`#f0f4f8`

**色彩系統**

| 用途 | 色碼 |
|------|------|
| 頁面背景 | `#f0f4f8` |
| 卡片背景 | `#ffffff` |
| 主要按鈕 | `#2563eb`（藍） |
| 執行按鈕 | `#16a34a`（綠） |
| 標題文字 | `#1e293b` |
| 副標題文字 | `#64748b` |
| 記錄區背景 | `#1e293b`（深色） |
| 記錄區文字 | `#94a3b8` |
| 成功訊息 | `#4ade80` |
| 錯誤訊息 | `#f87171` |

**字型**
- 一般文字：`微軟正黑體`
- 記錄區：`Consolas`（等寬）

**標準元件配置（由上至下）**
1. 大標題（18pt bold）＋ 副標題說明（10pt）
2. LabelFrame 卡片區塊，每個功能一張卡
3. 開始執行按鈕（綠色，置中，13pt bold）
4. 進度條（ttk.Progressbar，determinate 模式）
5. 執行記錄區（ScrolledText，深色背景）

**卡片（LabelFrame）標準樣式**
```python
tk.LabelFrame(parent, text="  標題  ",
              font=("微軟正黑體", 10, "bold"),
              bg="#ffffff", fg="#334155",
              relief="groove", bd=1,
              padx=10, pady=8)
```

**按鈕標準樣式**
```python
# 主要按鈕（藍）
tk.Button(..., bg="#2563eb", fg="white",
          font=("微軟正黑體", 10, "bold"),
          relief="flat", padx=10, cursor="hand2")

# 執行按鈕（綠）
tk.Button(..., bg="#16a34a", fg="white",
          font=("微軟正黑體", 13, "bold"),
          relief="flat", padx=30, pady=10, cursor="hand2")

# 次要按鈕（灰）
tk.Button(..., bg="#e2e8f0",
          font=("微軟正黑體", 9),
          relief="flat", padx=8, cursor="hand2")
```

**輸入欄標準樣式**
```python
tk.Entry(..., font=("微軟正黑體", 10),
         relief="solid", bd=1)
# 搭配 .pack(ipady=4) 增加高度
```

### 功能規格

- **檔案選擇**：使用 `filedialog.askopenfilename()`；選完 Excel 後輸出目錄自動帶入同一資料夾
- **執行方式**：計算邏輯一律跑在背景執行緒（`threading.Thread`），避免 GUI 凍結
- **執行記錄**：ScrolledText 顯示即時 log，依訊息類型套用顏色 tag：
  - `✅` `📄` → 綠色（`#4ade80`）
  - `⚠️` `❌` → 紅色（`#f87171`）
  - `===` → 灰色（`#475569`）
- **警告壓制**：程式開頭加入 `import warnings; warnings.filterwarnings("ignore")`

### 交付規格

每個專案打包成 ZIP，包含：

| 檔案 | 說明 |
|------|------|
| `xxx_gui.py` | 圖形介面主程式 |
| `xxx.py` | 命令列版（備用） |
| `開啟計算器.bat` | 雙擊啟動 GUI |
| `執行xxx.bat` | 命令列版啟動 |
| `README.txt` | 使用說明 |
| 範本檔案（如有） | 例如 `鐘點費格式.xlsx` |

**BAT 檔規格**
- 編碼：UTF-8 + CRLF（必須用 Python `wb` 模式寫入）
- 開頭加 `chcp 65001 > nul`
- Python 腳本檔名使用英文，避免中文路徑編碼問題
