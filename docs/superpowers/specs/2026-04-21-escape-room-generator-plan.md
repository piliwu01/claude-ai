# 密室逃脫題目發想器 — 實作計劃

**對應設計**：2026-04-21-escape-room-generator-design.md  
**日期**：2026-04-21

---

## 實作步驟

### Step 1：建立範本庫 `templates.py`
- 定義課文預設關鍵詞字典（木蘭詩、岳陽樓記、桃花源記、出師表、愛蓮說）
- 實作 5 種謎題類型各 5～10 個範本字串（含佔位符）
- 實作故事背景範本（5 個）
- 實作關卡串接提示語範本
- 提供 `generate_puzzle(theme, keywords, puzzle_type)` 函式：隨機選範本並填入

### Step 2：建立 Word 輸出模組（整合進 gui 或獨立函式）
- 使用 python-docx 建立文件
- 修主題 XML 避免 MS Mincho 中文字體覆蓋
- 支援封面、關卡區塊、提示、答案格式
- 提供 `export_to_docx(game_data, output_path, show_hints, show_answers)` 函式

### Step 3：建立主程式 `escape_room_gui.py`
- 依 CLAUDE.md tkinter 規格建立視窗（標題、背景色、字型）
- 實作四個卡片區塊：模式選擇、主題設定、謎題類型、執行按鈕
- 實作結果預覽區（深色 ScrolledText）
- 實作「重新發想」與「匯出 Word」按鈕
- 生成邏輯跑在背景執行緒（threading.Thread）

### Step 4：建立啟動檔
- `開啟密室題目發想器.bat`（UTF-8 + CRLF，用 Python wb 模式寫入）
- `README.txt`（使用說明）

### Step 5：打包
- 建立 `密室逃脫題目發想器.zip`，包含所有交付檔案

---

## 檔案清單

| 檔案 | 說明 |
|------|------|
| `escape_room_gui.py` | tkinter 主程式 |
| `templates.py` | 範本資料庫 + 生成邏輯 |
| `開啟密室題目發想器.bat` | 雙擊啟動 |
| `README.txt` | 使用說明 |
| `密室逃脫題目發想器.zip` | 完整打包 |

---

## 相依套件

- `tkinter`（Python 內建）
- `python-docx`（需安裝：`pip install python-docx`）
