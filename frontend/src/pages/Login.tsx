import { FormEvent, useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Activity, LoaderCircle, MailCheck } from 'lucide-react';
import { authEnabled, supabase } from '../lib/supabase';
import { ensureProfile } from '../lib/session';

type Mode = 'login' | 'register' | 'reset';
export default function Login() {
  const [mode, setMode] = useState<Mode>('login');
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('');
  const [name, setName] = useState(''); const [loading, setLoading] = useState(false); const [msg, setMsg] = useState('');
  const navigate = useNavigate(); const location = useLocation();
  useEffect(() => { if (!authEnabled) return; supabase!.auth.getSession().then(({ data }) => { if (data.session && mode !== 'reset') navigate('/dashboard', { replace: true }); }); }, [navigate, mode]);
  async function submit(e: FormEvent) {
    e.preventDefault(); setLoading(true); setMsg('');
    if (!supabase) { setMsg('Supabase is not configured. Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to enable authentication.'); setLoading(false); return; }
    if (mode === 'reset') { const r = await supabase.auth.resetPasswordForEmail(email, { redirectTo: `${window.location.origin}/login` }); setMsg(r.error ? r.error.message : 'Password-reset instructions have been sent if the account exists.'); setLoading(false); return; }
    const r = mode === 'login' ? await supabase.auth.signInWithPassword({ email, password }) : await supabase.auth.signUp({ email, password, options: { data: { full_name: name } } });
    if (r.error) setMsg(r.error.message);
    else if (r.data.user) { await ensureProfile(r.data.user); if (mode === 'register' && !r.data.session) setMsg('Account created. Check your email to confirm the account, then sign in.'); else navigate((location.state as { from?: string } | null)?.from || '/dashboard', { replace: true }); }
    setLoading(false);
  }
  return <main className="mx-auto grid min-h-[calc(100vh-72px)] max-w-6xl place-items-center px-5 py-12"><div className="grid w-full overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-soft md:grid-cols-2 dark:border-slate-800 dark:bg-slate-900"><div className="hidden bg-slate-950 p-10 text-white md:block"><div className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-600"><Activity /></div><h2 className="display mt-16 text-4xl font-extrabold">Healthcare access, routed intelligently.</h2><p className="mt-5 leading-7 text-slate-400">SehatSetu connects natural-language healthcare questions with transparent service pathways while keeping the decision-support boundary clear.</p></div><div className="p-7 sm:p-10"><p className="text-xs font-bold uppercase tracking-[.18em] text-brand-600">SehatSetu</p><h1 className="display mt-2 text-3xl font-extrabold">{mode === 'login' ? 'Welcome back' : mode === 'register' ? 'Create your account' : 'Reset your password'}</h1>
  <form onSubmit={submit} className="mt-8 space-y-4">{mode === 'register' && <input value={name} onChange={e=>setName(e.target.value)} required placeholder="Full name" className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500"/>}<input value={email} onChange={e=>setEmail(e.target.value)} type="email" required placeholder="Email address" className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500"/>{mode !== 'reset' && <input value={password} onChange={e=>setPassword(e.target.value)} type="password" required minLength={6} placeholder="Password" className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500"/>}<button className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-3 font-bold text-white" disabled={loading}>{loading?<LoaderCircle size={18} className="animate-spin"/>:mode==='reset'?<MailCheck size={18}/>:null}{mode==='login'?'Sign in':mode==='register'?'Register':'Send reset link'}</button></form>
  {msg&&<p className="mt-4 rounded-xl bg-slate-100 p-3 text-sm text-slate-600 dark:bg-slate-800 dark:text-slate-300">{msg}</p>}
  <div className="mt-5 flex flex-wrap gap-4 text-sm font-bold text-brand-700">{mode !== 'reset' && <button onClick={()=>setMode(mode==='login'?'register':'login')}>{mode==='login'?'Create an account':'Already have an account?'}</button>}{mode==='login'&&authEnabled&&<button onClick={()=>setMode('reset')}>Forgot password?</button>}{mode==='reset'&&<button onClick={()=>setMode('login')}>Back to sign in</button>}</div><Link to="/" className="mt-8 block text-center text-sm text-slate-400">Back to SehatSetu</Link></div></div></main>;
}
