import { supabase } from './supabase';
import type { User } from '@supabase/supabase-js';

export async function currentUser(): Promise<User | null> {
  if (!supabase) return null;
  const { data } = await supabase.auth.getUser();
  return data.user;
}

export async function ensureProfile(user: User) {
  if (!supabase) return;
  await supabase.from('profiles').upsert({ id: user.id, email: user.email ?? null }, { onConflict: 'id', ignoreDuplicates: true });
}
