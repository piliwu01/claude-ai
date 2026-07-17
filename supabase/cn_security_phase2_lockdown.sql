-- Phase 2: remove legacy direct table access after the RPC-based site is live.
-- Safe to run more than once. The transaction rolls back if verification fails.

begin;

alter table public.cn_users enable row level security;
alter table public.cn_scores enable row level security;

-- These two tables are RPC-only. Remove every direct RLS policy, including
-- legacy policies whose names may differ from the original deployment.
do $policy_cleanup$
declare
  v_policy record;
begin
  for v_policy in
    select schemaname, tablename, policyname
    from pg_policies
    where schemaname = 'public'
      and tablename in ('cn_users', 'cn_scores')
  loop
    execute format(
      'drop policy if exists %I on %I.%I',
      v_policy.policyname,
      v_policy.schemaname,
      v_policy.tablename
    );
  end loop;
end;
$policy_cleanup$;

revoke all on table public.cn_users from anon, authenticated;
revoke all on table public.cn_scores from anon, authenticated;

-- Supabase may auto-grant newly created public-schema functions to API roles.
-- Reset every RPC grant, then add only the intended allowlist.
revoke all on function public.cn_account_exists(text) from public, anon, authenticated;
revoke all on function public.cn_register(text, text) from public, anon, authenticated;
revoke all on function public.cn_login(text, text) from public, anon, authenticated;
revoke all on function public.cn_save_score(text, text, integer, integer, numeric) from public, anon, authenticated;
revoke all on function public.cn_leaderboard(integer) from public, anon, authenticated;
revoke all on function public.cn_is_admin() from public, anon, authenticated;
revoke all on function public.cn_admin_list_scores() from public, anon, authenticated;
revoke all on function public.cn_admin_delete_account(text) from public, anon, authenticated;

grant execute on function public.cn_account_exists(text) to anon, authenticated;
grant execute on function public.cn_register(text, text) to anon, authenticated;
grant execute on function public.cn_login(text, text) to anon, authenticated;
grant execute on function public.cn_save_score(text, text, integer, integer, numeric) to anon, authenticated;
grant execute on function public.cn_leaderboard(integer) to anon, authenticated;

grant execute on function public.cn_is_admin() to authenticated;
grant execute on function public.cn_admin_list_scores() to authenticated;
grant execute on function public.cn_admin_delete_account(text) to authenticated;

-- Abort the transaction if direct table access or an admin RPC grant is wrong.
do $verify_lockdown$
begin
  if exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename in ('cn_users', 'cn_scores')
  ) then
    raise exception 'lockdown_failed: direct table policy remains';
  end if;

  if has_table_privilege('anon', 'public.cn_users', 'SELECT')
     or has_table_privilege('anon', 'public.cn_users', 'INSERT')
     or has_table_privilege('anon', 'public.cn_users', 'UPDATE')
     or has_table_privilege('anon', 'public.cn_users', 'DELETE')
     or has_table_privilege('authenticated', 'public.cn_users', 'SELECT')
     or has_table_privilege('authenticated', 'public.cn_users', 'INSERT')
     or has_table_privilege('authenticated', 'public.cn_users', 'UPDATE')
     or has_table_privilege('authenticated', 'public.cn_users', 'DELETE')
     or has_table_privilege('anon', 'public.cn_scores', 'SELECT')
     or has_table_privilege('anon', 'public.cn_scores', 'INSERT')
     or has_table_privilege('anon', 'public.cn_scores', 'UPDATE')
     or has_table_privilege('anon', 'public.cn_scores', 'DELETE')
     or has_table_privilege('authenticated', 'public.cn_scores', 'SELECT')
     or has_table_privilege('authenticated', 'public.cn_scores', 'INSERT')
     or has_table_privilege('authenticated', 'public.cn_scores', 'UPDATE')
     or has_table_privilege('authenticated', 'public.cn_scores', 'DELETE') then
    raise exception 'lockdown_failed: direct table privilege remains';
  end if;

  if has_function_privilege('anon', 'public.cn_is_admin()', 'EXECUTE')
     or has_function_privilege('anon', 'public.cn_admin_list_scores()', 'EXECUTE')
     or has_function_privilege('anon', 'public.cn_admin_delete_account(text)', 'EXECUTE') then
    raise exception 'lockdown_failed: anon can execute an admin RPC';
  end if;

  if not has_function_privilege('authenticated', 'public.cn_is_admin()', 'EXECUTE')
     or not has_function_privilege('authenticated', 'public.cn_admin_list_scores()', 'EXECUTE')
     or not has_function_privilege('authenticated', 'public.cn_admin_delete_account(text)', 'EXECUTE') then
    raise exception 'lockdown_failed: authenticated admin RPC grant is missing';
  end if;

  if not has_function_privilege('anon', 'public.cn_account_exists(text)', 'EXECUTE')
     or not has_function_privilege('anon', 'public.cn_register(text,text)', 'EXECUTE')
     or not has_function_privilege('anon', 'public.cn_login(text,text)', 'EXECUTE')
     or not has_function_privilege('anon', 'public.cn_save_score(text,text,integer,integer,numeric)', 'EXECUTE')
     or not has_function_privilege('anon', 'public.cn_leaderboard(integer)', 'EXECUTE') then
    raise exception 'lockdown_failed: student RPC grant is missing';
  end if;
end;
$verify_lockdown$;

commit;

-- Expected verification result:
--   cn_users/cn_scores: no anon/authenticated direct privileges or policies
--   student RPCs: anon + authenticated
--   admin RPCs: authenticated only
select
  has_table_privilege('anon', 'public.cn_users', 'SELECT') as anon_reads_users,
  has_table_privilege('anon', 'public.cn_scores', 'SELECT') as anon_reads_scores,
  has_function_privilege('anon', 'public.cn_login(text,text)', 'EXECUTE') as anon_uses_student_login,
  has_function_privilege('anon', 'public.cn_admin_list_scores()', 'EXECUTE') as anon_uses_admin_list,
  has_function_privilege('authenticated', 'public.cn_admin_list_scores()', 'EXECUTE') as authenticated_uses_admin_list;

