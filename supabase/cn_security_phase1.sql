-- Phase 1: add secure RPCs and quiz_scores validation without removing
-- the legacy cn_users/cn_scores access needed by the currently deployed site.

begin;

create schema if not exists extensions;
create extension if not exists pgcrypto with schema extensions;

create table if not exists public.cn_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.cn_admins enable row level security;
revoke all on table public.cn_admins from anon, authenticated;

create or replace function public.cn_account_exists(p_nickname text)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nickname text := btrim(coalesce(p_nickname, ''));
begin
  if char_length(v_nickname) < 1 or char_length(v_nickname) > 30 then
    return false;
  end if;

  return exists (
    select 1
    from public.cn_users u
    where u.nickname = v_nickname
  );
end;
$$;

create or replace function public.cn_register(p_nickname text, p_password text)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nickname text := btrim(coalesce(p_nickname, ''));
begin
  if char_length(v_nickname) < 1 or char_length(v_nickname) > 30 then
    return jsonb_build_object('ok', false, 'code', 'invalid_nickname');
  end if;

  if char_length(coalesce(p_password, '')) < 6 or char_length(p_password) > 128 then
    return jsonb_build_object('ok', false, 'code', 'invalid_password');
  end if;

  if exists (select 1 from public.cn_users u where u.nickname = v_nickname) then
    return jsonb_build_object('ok', false, 'code', 'nickname_taken');
  end if;

  insert into public.cn_users (nickname, password_hash)
  values (
    v_nickname,
    extensions.crypt(p_password, extensions.gen_salt('bf', 10))
  );

  return jsonb_build_object('ok', true);
exception
  when unique_violation then
    return jsonb_build_object('ok', false, 'code', 'nickname_taken');
end;
$$;

create or replace function public.cn_login(p_nickname text, p_password text)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.cn_users u
    where u.nickname = btrim(coalesce(p_nickname, ''))
      and char_length(coalesce(p_password, '')) between 6 and 128
      and u.password_hash = extensions.crypt(p_password, u.password_hash)
  );
$$;

create or replace function public.cn_save_score(
  p_nickname text,
  p_password text,
  p_total_answered integer,
  p_correct_count integer,
  p_score numeric
)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nickname text := btrim(coalesce(p_nickname, ''));
  v_valid_login boolean;
begin
  select public.cn_login(v_nickname, p_password) into v_valid_login;

  if not coalesce(v_valid_login, false) then
    raise exception 'invalid_credentials' using errcode = '28000';
  end if;

  if p_total_answered is null or p_total_answered < 0 or p_total_answered > 100000 then
    raise exception 'invalid_total_answered' using errcode = '22023';
  end if;

  if p_correct_count is null or p_correct_count < 0 or p_correct_count > p_total_answered then
    raise exception 'invalid_correct_count' using errcode = '22023';
  end if;

  if p_score is null or p_score < 0 or p_score > p_correct_count then
    raise exception 'invalid_score' using errcode = '22023';
  end if;

  insert into public.cn_scores (
    nickname, total_answered, correct_count, score, updated_at
  ) values (
    v_nickname, p_total_answered, p_correct_count, p_score, now()
  )
  on conflict (nickname) do update
  set total_answered = excluded.total_answered,
      correct_count = excluded.correct_count,
      score = excluded.score,
      updated_at = excluded.updated_at;
end;
$$;

create or replace function public.cn_leaderboard(p_limit integer default 100)
returns table (
  nickname text,
  total_answered integer,
  correct_count integer,
  score numeric,
  updated_at timestamptz
)
language sql
security definer
set search_path = ''
as $$
  select s.nickname, s.total_answered, s.correct_count, s.score, s.updated_at
  from public.cn_scores s
  order by s.score desc, s.correct_count desc, s.updated_at asc
  limit greatest(1, least(coalesce(p_limit, 100), 500));
$$;

create or replace function public.cn_is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.cn_admins a
    where a.user_id = auth.uid()
  );
$$;

create or replace function public.cn_admin_list_scores()
returns table (
  nickname text,
  total_answered integer,
  correct_count integer,
  score numeric,
  updated_at timestamptz
)
language plpgsql
security definer
set search_path = ''
as $$
begin
  if not public.cn_is_admin() then
    raise exception 'admin_required' using errcode = '42501';
  end if;

  return query
  select u.nickname,
         coalesce(s.total_answered, 0),
         coalesce(s.correct_count, 0),
         coalesce(s.score, 0),
         s.updated_at
  from public.cn_users u
  left join public.cn_scores s on s.nickname = u.nickname
  order by coalesce(s.score, 0) desc, u.nickname asc;
end;
$$;

create or replace function public.cn_admin_delete_account(p_nickname text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nickname text := btrim(coalesce(p_nickname, ''));
begin
  if not public.cn_is_admin() then
    raise exception 'admin_required' using errcode = '42501';
  end if;

  delete from public.cn_scores where nickname = v_nickname;
  delete from public.cn_users where nickname = v_nickname;
end;
$$;

revoke all on function public.cn_account_exists(text) from public;
revoke all on function public.cn_register(text, text) from public;
revoke all on function public.cn_login(text, text) from public;
revoke all on function public.cn_save_score(text, text, integer, integer, numeric) from public;
revoke all on function public.cn_leaderboard(integer) from public;
revoke all on function public.cn_is_admin() from public;
revoke all on function public.cn_admin_list_scores() from public;
revoke all on function public.cn_admin_delete_account(text) from public;

grant execute on function public.cn_account_exists(text) to anon, authenticated;
grant execute on function public.cn_register(text, text) to anon, authenticated;
grant execute on function public.cn_login(text, text) to anon, authenticated;
grant execute on function public.cn_save_score(text, text, integer, integer, numeric) to anon, authenticated;
grant execute on function public.cn_leaderboard(integer) to anon, authenticated;
grant execute on function public.cn_is_admin() to authenticated;
grant execute on function public.cn_admin_list_scores() to authenticated;
grant execute on function public.cn_admin_delete_account(text) to authenticated;

alter table public.quiz_scores
  drop constraint if exists quiz_scores_player_name_length,
  drop constraint if exists quiz_scores_topic_length,
  drop constraint if exists quiz_scores_total_range,
  drop constraint if exists quiz_scores_score_range;

alter table public.quiz_scores
  add constraint quiz_scores_player_name_length
    check (char_length(btrim(player_name)) between 1 and 30),
  add constraint quiz_scores_topic_length
    check (char_length(btrim(topic)) between 1 and 100),
  add constraint quiz_scores_total_range
    check (total between 1 and 1000),
  add constraint quiz_scores_score_range
    check (score between 0 and total);

drop policy if exists "anyone can read" on public.quiz_scores;
drop policy if exists "anyone can insert" on public.quiz_scores;
drop policy if exists quiz_scores_public_read on public.quiz_scores;
drop policy if exists quiz_scores_public_insert_valid on public.quiz_scores;

create policy quiz_scores_public_read
on public.quiz_scores
for select
to anon, authenticated
using (true);

create policy quiz_scores_public_insert_valid
on public.quiz_scores
for insert
to anon, authenticated
with check (
  char_length(btrim(player_name)) between 1 and 30
  and char_length(btrim(topic)) between 1 and 100
  and total between 1 and 1000
  and score between 0 and total
);

revoke all on table public.quiz_scores from anon, authenticated;
grant select, insert on table public.quiz_scores to anon, authenticated;
grant usage, select on sequence public.quiz_scores_id_seq to anon, authenticated;

commit;

-- Rollback for Phase 1 (review and run separately only if needed):
-- begin;
-- drop function if exists public.cn_admin_delete_account(text);
-- drop function if exists public.cn_admin_list_scores();
-- drop function if exists public.cn_is_admin();
-- drop function if exists public.cn_leaderboard(integer);
-- drop function if exists public.cn_save_score(text, text, integer, integer, numeric);
-- drop function if exists public.cn_login(text, text);
-- drop function if exists public.cn_register(text, text);
-- drop function if exists public.cn_account_exists(text);
-- drop table if exists public.cn_admins;
-- alter table public.quiz_scores
--   drop constraint if exists quiz_scores_player_name_length,
--   drop constraint if exists quiz_scores_topic_length,
--   drop constraint if exists quiz_scores_total_range,
--   drop constraint if exists quiz_scores_score_range;
-- drop policy if exists quiz_scores_public_read on public.quiz_scores;
-- drop policy if exists quiz_scores_public_insert_valid on public.quiz_scores;
-- create policy "anyone can read" on public.quiz_scores for select to public using (true);
-- create policy "anyone can insert" on public.quiz_scores for insert to public with check (true);
-- grant all on table public.quiz_scores to anon, authenticated;
-- grant all on sequence public.quiz_scores_id_seq to anon, authenticated;
-- commit;
