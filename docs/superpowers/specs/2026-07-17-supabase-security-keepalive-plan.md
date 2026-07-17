# Supabase 教學網站安全改造與防暫停實作計畫

日期：2026-07-17（Asia/Taipei）
依據：`docs/superpowers/specs/2026-07-17-supabase-security-keepalive-design.md`

## 實作原則

- 使用兩階段資料庫遷移，先新增安全 RPC 並驗證，再撤銷舊的公開資料表權限，避免網站中斷。
- 每次遠端 SQL 執行前展示完整 SQL，取得使用者確認後才執行。
- MCP 維持 project-scoped、read-only；DDL 由 Supabase SQL Editor 執行。
- 只修改明列檔案，保留 repository 內其他未提交內容。
- 不自動 push 或部署；發布前另行確認。

## Phase 0：建立安全基線與回復資訊

### 0.1 匯出唯讀基線

透過 Supabase MCP 記錄：

- `cn_users`、`cn_scores`、`quiz_scores` schema、row count、RLS、policies、grants。
- 既有 functions 與同名 RPC，避免名稱碰撞。
- security advisors。

驗收：基線結果足以判斷遷移前後差異。

### 0.2 建立本機檔案備份

備份但不提交：

- `國文練習網站.html`
- `build_quiz_site.py`

驗收：備份檔含時間戳，可在不碰其他 working tree 內容的情況下回復。

## Phase 1：資料庫新增安全能力（不撤銷舊權限）

新增 `supabase/cn_security_phase1.sql`，內容包含：

1. 啟用 `pgcrypto` extension。
2. 建立 `public.cn_admins(user_id uuid primary key references auth.users(id) on delete cascade, created_at timestamptz default now())`。
3. 對 `cn_admins` 啟用 RLS；撤銷 anon／authenticated 直接 table 權限。
4. 建立並鎖定學生 RPC：
   - `cn_account_exists(text) returns boolean`
   - `cn_register(text,text) returns jsonb`
   - `cn_login(text,text) returns boolean`
   - `cn_save_score(text,text,integer,integer,numeric) returns void`
   - `cn_leaderboard(integer) returns table(...)`
5. 建立並鎖定管理 RPC：
   - `cn_admin_list_scores() returns table(...)`
   - `cn_admin_delete_account(text) returns void`
6. 所有 `SECURITY DEFINER` 函式：
   - 固定安全 `search_path`。
   - 完整限定 schema。
   - `REVOKE ALL ... FROM PUBLIC`。
   - 僅將學生 RPC grant 給 anon／authenticated；管理 RPC 僅 grant 給 authenticated。
7. 新註冊密碼使用 `crypt(password, gen_salt('bf'))`；驗證使用 `password_hash = crypt(password, password_hash)`。
8. 暱稱 trim 後長度 1～30；密碼最少 6；成績須符合 `total >= 0`、`correct between 0 and total`、`score between 0 and correct`。
9. `quiz_scores` 加入具名 CHECK constraints，限制姓名、主題、總題數與得分。
10. 收斂 `quiz_scores` grants 為 SELECT、INSERT，重新建立具名 SELECT／INSERT policies；不允許 UPDATE／DELETE。

執行前檢查：查詢是否已有同名函式、constraint 或 admin table。

驗收：

- RPC 可透過 anon key 呼叫。
- 舊網站尚未切換前仍可運作。
- 不在 Phase 1 撤銷 `cn_users`、`cn_scores` 舊權限。

回復：Phase 1 SQL 同時提供只移除新 RPC、admin table 與新 constraints 的 rollback 區段；不影響舊資料表資料。

## Phase 2：管理員 Supabase Auth 設定

1. 使用者在 Supabase Dashboard 建立管理員 Email＋密碼，不在對話中提供密碼。
2. 從 Dashboard 取得該 Auth user UUID。
3. 在 SQL Editor 將 UUID 加入 `public.cn_admins`。
4. 使用管理 RPC 驗證 allowlist；未列入的 authenticated 使用者必須被拒絕。

驗收：只有 allowlist 管理員能列出全部成績與刪除測試帳號。

## Phase 3：網站切換至 RPC

### 3.1 修改產生器

檔案：`build_quiz_site.py`

- 移除前端 `sha256`。
- 新增統一 `sbRpc(functionName, body, accessToken?)` helper。
- `step1Next` 改呼叫 `cn_account_exists`。
- `step2Submit` 改呼叫 `cn_register`／`cn_login`。
- 將學生密碼只保存於 JavaScript 記憶體變數；不寫入 localStorage。
- `syncScore` 改呼叫 `cn_save_score`。
- `loadLeaderboard` 改呼叫 `cn_leaderboard`。
- 管理頁新增 Supabase Auth Email＋密碼登入區塊。
- 管理列表與刪除改呼叫 `cn_admin_list_scores`／`cn_admin_delete_account`，Authorization 使用 Auth access token。
- 登出時清除 Auth session 與頁面記憶體中的學生密碼。
- 保留原 UI 風格、題庫、計分公式與 localStorage 作答資料。

### 3.2 重新產生網站

執行：`python build_quiz_site.py`

產物：`國文練習網站.html`

驗收：

- 產生器可成功執行。
- 產物不含 `sha256`、`select=password_hash` 或對 `cn_users`／`cn_scores` 的直接 REST table 存取。
- 產物仍含題庫與既有主要 UI 元素。

## Phase 4：RPC 與網站相容性測試

1. 建立測試學生帳號。
2. 驗證帳號存在查詢、正確登入、錯誤密碼、短密碼拒絕。
3. 驗證成績新增與更新；驗證非法數值拒絕。
4. 驗證排行榜欄位與排序。
5. 驗證管理員登入、列表與刪除測試帳號。
6. 驗證非管理員無法呼叫管理 RPC。
7. 驗證 `quiz_scores` 合法 INSERT／SELECT 成功，UPDATE／DELETE 與非法 INSERT 失敗。
8. 使用瀏覽器進行基本 smoke test：登入、答題、同步、排行榜、管理頁。

驗收：所有流程通過後才能進入 Phase 5。

## Phase 5：發布 Gate

1. 顯示 `git diff -- build_quiz_site.py 國文練習網站.html supabase/cn_security_phase1.sql`。
2. 使用者確認是否 commit、push 與部署。
3. 若網站由 GitHub Pages 發布，確認實際 URL 已載入 RPC 版本。

未取得發布確認前，不進入舊權限撤銷。

## Phase 6：撤銷舊資料表存取

新增 `supabase/cn_security_phase2_lockdown.sql`：

- Drop `allow_all_cn_users`、`allow_all_cn_scores`。
- 啟用／維持兩表 RLS。
- Revoke anon／authenticated 對 `cn_users`、`cn_scores` 的所有 table／sequence 權限。
- 確認 table 上沒有 anon／authenticated 直接 policies。
- 保留受控 RPC execute grants。

驗收：

- anon 直接 REST 讀寫兩表皆失敗。
- RPC 功能仍全部成功。
- security advisor 不再回報兩表的 always-true policy 或 GraphQL exposure。

回復：只有在新網站無法修復且使用者明確確認時，才暫時恢復最小必要舊權限；不恢復 password_hash 公開 SELECT。

## Phase 7：Windows 防暫停排程

### 7.1 建立腳本

檔案：`tools/supabase_keepalive.ps1`

- 使用 project URL 與 publishable key。
- GET `/rest/v1/quiz_scores?select=id&limit=1`。
- 設定逾時與非 2xx 失敗處理。
- 將最近一次結果覆寫到使用者本機狀態檔；不記錄 API key。

### 7.2 建立工作排程

工作名稱：`Supabase-piliwu01-Keepalive`

- 每 8 小時執行 PowerShell 腳本。
- 錯過排程後儘快執行。
- 使用目前 Windows 使用者，不要求 service role 或管理員資料庫權限。

### 7.3 驗證

- 手動觸發工作。
- 查詢 Task Scheduler Last Run Result 為成功。
- 狀態檔包含台北時間與 HTTP 成功結果。
- Supabase logs 可看到唯讀 REST 請求。

## Phase 8：最終安全驗證與交付

1. 執行 Supabase security advisor。
2. 列出剩餘 INFO／WARN，逐項標註預期或待處理。
3. 確認 MCP 仍為 project-scoped、read-only OAuth。
4. 確認 repository 只包含本任務預期變更；不清理其他使用者檔案。
5. 提供：
   - 資料庫變更摘要。
   - 網站測試結果。
   - 排程名稱、頻率與最後執行結果。
   - 回復方式。

## 提交策略

建議分開提交：

1. `feat: add secure Supabase RPC layer`
2. `refactor: route quiz accounts through secure RPCs`
3. `security: lock down direct quiz table access`
4. `chore: add Supabase keepalive task script`

每次 commit 只加入本任務檔案；push 與部署需另外確認。
