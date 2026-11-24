-- SehatSetu 2.0 security hardening. Apply after 202611250001_init.sql.
create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path=public
as $$ select exists (select 1 from public.profiles where id=auth.uid() and role='admin'); $$;
revoke all on function public.is_admin() from public;
grant execute on function public.is_admin() to authenticated;

-- Users can edit profile details, but cannot promote themselves to admin.
drop policy if exists "profile owner update" on public.profiles;
create policy "profile owner update" on public.profiles for update using (auth.uid()=id) with check (auth.uid()=id and role = (select p.role from public.profiles p where p.id=auth.uid()));

create policy "admin read profiles" on public.profiles for select using (public.is_admin());
create policy "admin read queries" on public.healthcare_queries for select using (public.is_admin());
create policy "admin read appointments" on public.appointments for select using (public.is_admin());
create policy "admin update queries" on public.healthcare_queries for update using (public.is_admin());
create policy "admin update appointments" on public.appointments for update using (public.is_admin());

alter table public.profiles add constraint profiles_full_name_length check (full_name is null or char_length(full_name) <= 120);
