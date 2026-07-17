# Supabase 教學網站安全改造與防暫停設計

日期：2026-07-17（Asia/Taipei）

## 1. 目標

在保留學生「暱稱＋密碼」操作方式的前提下，移除瀏覽器對 `cn_users`、`cn_scores` 的直接資料表存取，改以受控 RPC 完成註冊、登入、成績同步與排行榜查詢；管理後台改用 Supabase Auth；同時收斂 `quiz_scores` 的公開權限並建立 Windows 防暫停排程。

## 2. 現況與風險

- `國文練習網站.html` 與 `build_quiz_site.py` 目前使用 anon key 直接讀取 `cn_users.password_hash`。
- `cn_users`、`cn_scores` 的 `ALL ... USING (true) WITH CHECK (true)` 政策使任何人都能讀寫、竄改或刪除資料。
- 網站管理後台直接以 anon key 讀取全部成績與刪除帳號，沒有可信的管理員身分驗證。
- `quiz_scores` 允許公開讀取與新增，符合公開排行榜需求，但缺乏資料範圍限制。
- Supabase Free Plan 可能因 7 天低活動而暫停；官方表示通常每天數次使用者資料庫請求可形成足夠活動，但不保證 keepalive 永久有效。

## 3. 範圍

### 3.1 納入

- `public.cn_users`
- `public.cn_scores`
- `public.quiz_scores`
- Supabase RPC 與管理員 allowlist
- `國文練習網站.html`
- `build_quiz_site.py`
- Windows 工作排程與 keepalive 腳本

### 3.2 不納入

- 題庫內容、版面視覺與計分公式重構
- 與本功能無關的 repository 整理
- 自動 push 或部署 GitHub Pages
- service role key 的前端或排程使用

## 4. 架構

### 4.1 學生帳號

學生仍輸入暱稱與密碼。密碼至少 6 個字元，透過 HTTPS 傳給 RPC。資料庫使用 `pgcrypto` 的 bcrypt 能力產生與驗證雜湊。前端不再執行 SHA-256，也不能讀取 `password_hash`。

登入成功後，密碼只存在目前頁面的 JavaScript 記憶體，不寫入 `localStorage`、檔案或 URL；重新整理或關閉頁面即清除。成績同步 RPC 每次重新驗證暱稱與密碼，避免以他人暱稱竄改成績。

### 4.2 學生 RPC

RPC 分為單一責任介面：

- `cn_account_exists(nickname)`：只回傳帳號是否存在。
- `cn_register(nickname, password)`：驗證格式、bcrypt 雜湊並建立帳號。
- `cn_login(nickname, password)`：只回傳驗證成功或失敗。
- `cn_save_score(nickname, password, total_answered, correct_count, score)`：驗證密碼與數值後 upsert 成績。
- `cn_leaderboard(limit)`：只回傳公開排行榜所需欄位。

所有 `SECURITY DEFINER` 函式固定 `search_path`，完整限定物件 schema，撤銷 `PUBLIC` 預設執行權，僅對必要角色授權。

### 4.3 管理員

管理員使用 Supabase Auth 的 Email＋密碼登入。另建後台專用 `cn_admins(user_id uuid primary key)` allowlist。管理 RPC 同時驗證 JWT 的 `sub` 與 allowlist：

- `cn_admin_list_scores()`：回傳管理表格需要的帳號與成績。
- `cn_admin_delete_account(nickname)`：在同一交易中刪除指定帳號與成績。

`cn_admins`、`cn_users`、`cn_scores` 均啟用 RLS，不提供 anon／authenticated 直接資料表政策，並撤銷直接 table／sequence 權限。Dashboard、postgres 與 service role 維持後台管理能力。

### 4.4 quiz_scores

保留公開 `SELECT` 與 `INSERT`，不允許公開 `UPDATE`、`DELETE`。新增資料須符合：

- `player_name` 長度 1～30。
- `topic` 長度 1～100。
- `total` 介於 1～1000。
- `score` 介於 0～`total`。

限制同時存在於資料庫 CHECK constraints 與 INSERT policy，避免只靠前端驗證。

## 5. 網站資料流

### 5.1 註冊與登入

1. 網站呼叫 `cn_account_exists` 決定顯示註冊或登入介面。
2. 註冊呼叫 `cn_register`；登入呼叫 `cn_login`。
3. 成功後把暱稱與密碼保存於頁面記憶體，載入本機作答統計。
4. 不把密碼或雜湊寫入 localStorage。

### 5.2 成績同步與排行榜

1. `syncScore` 呼叫 `cn_save_score`。
2. 網路錯誤時保留本機資料，後續操作再次觸發同步。
3. 排行榜呼叫 `cn_leaderboard`，不直接查詢 `cn_scores`。

### 5.3 管理後台

1. 管理員以 Supabase Auth Email＋密碼取得 session。
2. `cn_admin_list_scores` 依 JWT 與 allowlist 驗證身分。
3. 刪除帳號使用 `cn_admin_delete_account`。
4. 未登入或不在 allowlist 時顯示「沒有管理權限」，不回傳資料。

## 6. 錯誤處理

- 暱稱重複：顯示「這個暱稱已被使用」。
- 密碼錯誤：使用一般訊息，不透露雜湊或內部錯誤。
- 密碼少於 6 個字元：前端與 RPC 同時拒絕。
- 暱稱或數值格式錯誤：RPC 回傳可辨識但不含敏感細節的錯誤。
- 網路中斷：保留本機作答資料，不宣稱同步成功。
- 非管理員：拒絕執行管理 RPC。
- keepalive 失敗：記錄台北時間、HTTP 狀態與簡短錯誤，不記錄 API key。

## 7. 防暫停排程

- 腳本使用 project URL 與 Supabase publishable key。
- 每 8 小時對 `quiz_scores?select=id&limit=1` 發出唯讀 GET。
- 工作排程設定為錯過排程後儘快補跑。
- 腳本只覆寫單一狀態檔，包含最近執行時間與成功／失敗，避免日誌無限增長。
- 不使用 service role key，不寫入資料庫。
- keepalive 僅增加正常活動，不能視為 Supabase 永久不暫停保證；需要保證可用性時應升級付費方案。

## 8. 測試與驗收

1. 建立測試學生，驗證密碼使用 bcrypt 儲存而非前端 SHA-256。
2. 驗證正確密碼可登入、錯誤密碼不可登入、少於 6 字元不可註冊。
3. 驗證合法成績可同步，負數、答對數超過作答數等異常資料被拒絕。
4. 驗證 anon key 無法直接讀寫 `cn_users`、`cn_scores`。
5. 驗證學生排行榜仍可讀取且不含敏感欄位。
6. 建立 Supabase Auth 管理員並加入 allowlist，驗證查看與刪除測試帳號。
7. 驗證非 allowlist 使用者無法執行管理 RPC。
8. 驗證 `quiz_scores` 合法資料可新增、異常資料被 constraint／policy 拒絕、公開使用者無法更新或刪除。
9. 手動執行 keepalive 工作排程，確認 HTTP 成功與狀態檔更新。
10. 重新執行 Supabase security advisor，記錄所有剩餘警告及其是否屬預期設計。

## 9. 變更與發布控制

- 只修改本規格列出的網站檔案與新增必要 SQL／排程檔案。
- 保留 repository 中所有既有未提交修改，不進行 reset、checkout 或清理。
- 設計文件單獨提交；實作變更不自動 push 或部署。
- 資料庫 SQL 在遠端執行前再次展示並由使用者確認。

## 10. 成功條件

- 學生仍能使用暱稱＋至少 6 字元密碼完成註冊與登入。
- 前端無法讀取任何密碼雜湊，也無法直接讀寫帳號與成績表。
- 成績同步與排行榜功能正常。
- 只有 Supabase Auth allowlist 管理員能查看全體資料與刪除帳號。
- `quiz_scores` 只開放受限制的公開讀取與新增。
- Windows 排程每 8 小時執行唯讀 keepalive，且不保存高權限密鑰。
