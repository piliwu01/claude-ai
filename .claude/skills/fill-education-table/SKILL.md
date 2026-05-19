---
name: fill-education-table
description: |
  法定教育議題融入課程規劃表填寫助手：
  讀取七、八、九年級領域科目總體課程教學進度總表 PDF，
  自動分析並填入「法定教育議題融入課程規劃」DOC/DOCX 表格，
  輸出完成版 DOCX。

  當使用者說「幫我填法定議題表」「填教育議題」「填課程計畫」
  「fill-education-table」「議題融入」時，使用此技能。
---

# 法定教育議題融入課程規劃表填寫流程

## Step 0 — 確認輸入檔案

詢問使用者提供以下路徑（若尚未提供）：
1. **七年級 PDF**：七年級領域科目總體課程教學進度總表
2. **八年級 PDF**：八年級領域科目總體課程教學進度總表
3. **九年級 PDF**：九年級領域科目總體課程教學進度總表
4. **目標 DOC/DOCX**：法定教育議題融入課程規劃表（可為 `.doc` 或 `.docx`）

---

## Step 1 — 轉換 DOC（如有需要）

如果目標檔案是 `.doc`，先轉為 `.docx`（PowerShell Word COM）：

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$inputPath = "C:\path\to\file.doc"
$outputPath = $inputPath -replace '\.doc$', '.docx'
$doc = $word.Documents.Open($inputPath)
$doc.SaveAs([ref]$outputPath, [ref]16)
$doc.Close($false)
$word.Quit()
```

---

## Step 2 — 讀取三份 PDF，分析課程資料

使用 Read tool 讀取三份 PDF 全文，針對以下 **8 大法定教育議題** 逐一找出：

### 需要填入的欄位（每個年段各一列）

| 欄 | 說明 |
|---|---|
| col 3 | 實施週次（例：第9-13週） |
| col 4 | 彈性學習課程節數（整數） |
| col 5 | 融入領域實施節數（整數） |
| col 6 | 規劃總節數（col4 + col5） |
| col 7 | 單元/主題名稱（領域-單元名稱，多項用；分隔） |

### 8 大議題對應關鍵字

分析 PDF 時，針對以下關鍵字在各學科欄位中搜尋：

| 議題 | 搜尋關鍵字 |
|---|---|
| 性別平等教育 | 性別、性平、青春、兩性、多元性別、輔導課「人際」「群我」 |
| 性侵害防治教育 | 性侵害、防治、身體自主、健康與體育「青春」「生命」 |
| 家庭教育 | 家庭、家政、孝親、親子、家人、料理、綜合「家」 |
| 家庭暴力防治教育 | 家庭暴力、家暴、公民「家庭生活」、綜合家政「料理」 |
| 環境教育 | 環境、生態、防災、能源、海洋、溼地、低碳、食物里程 |
| 安全教育 | 交通安全、水域安全、防墜、防災、食藥安全、校園安全 |
| 戶外教育 | 戶外、踏查、露營、登山、童軍、自然探索 |
| 生命教育 | 生命教育、國文（含生命主題課文）、感恩、珍愛生命 |

### 分析方式

對每個年級（一上/一下、二上/二下、三上/三下）：
1. 逐週掃描 PDF，記錄每週各學科的單元名稱
2. 對照上表找出相關週次與單元
3. 判斷節數類型：
   - **彈性學習課程**：課表中標示「彈性」「彈性學習」的節數
   - **融入領域實施**：在正式學科（健體、公民、國文、自然等）中融入的節數
4. 單元名稱格式：`學科簡稱-單元名稱`，例如：`健體-我的青春檔案`

### 法定最低節數參考

| 議題 | 法定最低 |
|---|---|
| 性別平等教育 | 每學期 6 節 |
| 性侵害防治教育 | 每學期 3 節 |
| 家庭教育 | 每學年 6 節 |
| 家庭暴力防治教育 | 每學年 6 節 |
| 環境教育 | 每學期 3 節 |
| 安全教育 | 每學期 2 節以上 |
| 戶外教育 | 無法定下限 |
| 生命教育 | 無法定下限 |

---

## Step 3 — 確認表格結構

使用 PowerShell 快速確認 DOCX 的列數，確保符合預期結構：

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("C:\path\to\file.docx")
$tbl = $doc.Tables.Item(1)
"Total rows: $($tbl.Rows.Count), cols: $($tbl.Columns.Count)" | Write-Host
# 確認幾個代表性 cell
"Row4 col2: $($tbl.Cell(4,2).Range.Text)" | Write-Host  # 應為「一上」
"Row16 col2: $($tbl.Cell(16,2).Range.Text)" | Write-Host # 應為「一上」
$doc.Close($false)
$word.Quit()
```

### 標準表格結構（共 99 列）

```
列 1-3：標題列（合併儲存格）
列 4-15：性別平等教育（一上=4, 一下=5, 二上=6, 二下=7, 三上=8, 三下=9, 四上-六下=10-15）
列 16-27：性侵害防治教育（一上=16 ... 三下=21）
列 28-39：家庭教育（一上=28 ... 三下=33）
列 40-51：家庭暴力防治教育（一上=40 ... 三下=45）
列 52-63：環境教育（一上=52 ... 三下=57）
列 64-75：安全教育（一上=64 ... 三下=69）
列 76-87：戶外教育（一上=76 ... 三下=81）
列 88-99：生命教育（一上=88 ... 三下=93）
```

> 只填國中年段（一上～三下，即第 4-9 列位置），四上～六下保持空白。

若列數不符（例如表格有異動），用以下方式重新偵測：
```powershell
for ($r = 1; $r -le $tbl.Rows.Count; $r++) {
    try {
        $c2 = $tbl.Cell($r, 2).Range.Text.Trim()
        if ($c2 -eq "一上") {
            $c1 = try { $tbl.Cell($r, 1).Range.Text.Trim() } catch { "MERGE" }
            "Row $r | col1: $c1 | col2: $c2" | Write-Host
        }
    } catch {}
}
```

---

## Step 4 — 填入表格

使用 PowerShell Word COM 填入所有資料，**所有操作在同一個 PowerShell 呼叫中完成**：

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("C:\path\to\file.docx")
$tbl = $doc.Tables.Item(1)

function FillCell($r, $c, $text) {
    try { $tbl.Cell($r, $c).Range.Text = $text } catch { Write-Host "Err r$r c$c" }
}

# 依 Step 2 分析結果填入 — 格式範例：
# 性別平等教育 一上
FillCell 4 3 "第X-Y週"
FillCell 4 4 "0"        # 彈性節數
FillCell 4 5 "6"        # 融入節數
FillCell 4 6 "6"        # 總節數
FillCell 4 7 "健體-XXX單元"

# ... 其餘各列依此類推 ...

$outputPath = ($doc.FullName -replace '\.docx$', '_完成版.docx')
$doc.SaveAs([ref]$outputPath, [ref]16)
$doc.Close($false)
$word.Quit()
Write-Host "完成：$outputPath"
```

### 注意事項

- **不可用 `SC` 作為函數名**：PowerShell 內建別名 `Set-Content`，會衝突
- **所有程式碼必須在同一個 PowerShell 呼叫中**：變數不跨呼叫保留
- 若節數欄填「0」而非空白，有助維持格式一致
- 週次格式統一用「第X週」或「第X-Y週」或「第X、Y週」

---

## Step 5 — 完成回報

告知使用者：
- 輸出檔案路徑（`_完成版.docx`）
- 各議題填入節數是否符合法定最低要求
- 如有任何週次/節數不足，提示需補充的項目

---

## 常見錯誤排除

| 問題 | 解法 |
|---|---|
| `.doc` 無法直接讀取 | 先用 Word COM 轉 `.docx`（Step 1） |
| `Cell()` 拋出錯誤 | 該格為合併儲存格，屬正常，catch 後略過 |
| 中文亂碼 | PowerShell 輸出用 `Out-File -Encoding UTF8` 再用 Read tool 讀取 |
| Word 未安裝 | 此技能依賴 Microsoft Word，需確認已安裝 |
| 列號不符預期 | 執行 Step 3 的偵測腳本重新定位 |
