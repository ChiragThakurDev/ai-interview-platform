import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Users, Shield, BarChart3, Activity, Search,
  Trash2, RefreshCw, Brain, TrendingUp,
  UserCheck, UserX, Crown, FileText, Star,
  AlertTriangle, MessageSquare,
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  ResponsiveContainer, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend,
} from 'recharts'
import {
  useAdminDashboard, useAdminUsers, useAdminActivity,
  useAdminAnalytics, useActivateUser, useDeactivateUser, useDeleteUser,
} from '@/hooks'
import { Card, Badge, Spinner, EmptyState, Button } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'

// ── palette ───────────────────────────────────────────────────────────────────
const C = { brand: '#6366f1', green: '#10b981', amber: '#f59e0b', red: '#ef4444', purple: '#8b5cf6', cyan: '#06b6d4' }
const DIFF_PIE = [{ name: 'Easy', fill: C.green }, { name: 'Medium', fill: C.amber }, { name: 'Hard', fill: C.red }]
const TIP = {
  contentStyle: { background: '#141523', border: '1px solid #2a2d3e', borderRadius: '10px', fontSize: '11px', color: '#e2e8f0' },
  cursor: { fill: 'rgba(99,102,241,0.08)' },
}

const fadeUp = { hidden: { opacity: 0, y: 14 }, show: { opacity: 1, y: 0 } }
const stagger = { show: { transition: { staggerChildren: 0.07 } } }

type Tab = 'overview' | 'users' | 'analytics' | 'activity'

// ── Stat card ─────────────────────────────────────────────────────────────────
const StatCard = ({ icon: Icon, label, value, color, sub }: {
  icon: React.ElementType; label: string; value: string | number; color: string; sub?: string
}) => (
  <motion.div variants={fadeUp}>
    <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card h-full">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider">{label}</p>
          <p className="text-3xl font-black dark:text-neutral-50 text-neutral-900 mt-1 tabular-nums">{value ?? '—'}</p>
          {sub && <p className="text-xs dark:text-neutral-500 text-neutral-400 mt-0.5">{sub}</p>}
        </div>
        <div className={cn('p-3 rounded-xl shrink-0', color)}>
          <Icon size={18} className="text-white" />
        </div>
      </div>
    </Card>
  </motion.div>
)

// ── Section heading ───────────────────────────────────────────────────────────
const SH = ({ icon: Icon, title, c = 'text-brand-500' }: { icon: React.ElementType; title: string; c?: string }) => (
  <div className="flex items-center gap-2 mb-4">
    <Icon size={14} className={c} />
    <h3 className="text-xs font-bold dark:text-neutral-200 text-neutral-700 uppercase tracking-widest">{title}</h3>
  </div>
)

export const AdminDashboardPage = () => {
  const [tab, setTab] = useState<Tab>('overview')
  const [search, setSearch] = useState('')
  const [confirmDelete, setConfirmDelete] = useState<number | null>(null)

  const { data: stats, isLoading: loadingStats, refetch } = useAdminDashboard()
  const { data: users,    isLoading: loadingUsers    } = useAdminUsers()
  const { data: activity, isLoading: loadingActivity } = useAdminActivity()
  const { data: analytics,isLoading: loadingAnalytics} = useAdminAnalytics()

  const { mutate: doActivate,   isPending: activating  } = useActivateUser()
  const { mutate: doDeactivate, isPending: deactivating} = useDeactivateUser()
  const { mutate: doDelete,     isPending: deleting    } = useDeleteUser()

  const filtered = (users ?? []).filter(u =>
    !search || u.name?.toLowerCase().includes(search.toLowerCase()) || u.email?.toLowerCase().includes(search.toLowerCase())
  )

  // ── chart data — built from actual backend shapes ─────────────────────────
  // registrations: Record<string,number>  e.g. { "Jan": 5, "Feb": 3 }
  const regData = analytics?.registrations
    ? Object.entries(analytics.registrations).map(([date, count]) => ({ date, count }))
    : []

  // interviews: { completed: number, pending: number } — not a time series
  const interviewSummary = analytics?.interviews ?? { completed: 0, pending: 0 }

  // popular_roles: already an array
  const roleData = (analytics?.popular_roles ?? [])
    .slice(0, 7)
    .map(d => ({ role: d.role.length > 16 ? d.role.slice(0, 16) + '…' : d.role, count: d.count }))

  // difficulty_distribution: Record { easy, medium, hard }
  const diffData = analytics?.difficulty_distribution
    ? [
        { difficulty: 'Easy',   count: analytics.difficulty_distribution.easy,   fill: C.green  },
        { difficulty: 'Medium', count: analytics.difficulty_distribution.medium, fill: C.amber  },
        { difficulty: 'Hard',   count: analytics.difficulty_distribution.hard,   fill: C.red    },
      ].filter(d => d.count > 0)
    : []

  // score_distribution: Record<string,number>
  const scoreDist = analytics?.score_distribution
    ? Object.entries(analytics.score_distribution).map(([range, count]) => ({ range, count }))
    : []
  const axisC = '#4b5563'
  const textC = '#9ca3af'

  const TABS: { id: Tab; label: string; icon: React.ElementType }[] = [
    { id: 'overview',  label: 'Overview',  icon: BarChart3  },
    { id: 'users',     label: 'Users',     icon: Users      },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'activity',  label: 'Activity',  icon: Activity   },
  ]

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-fade-in pb-8">

      {/* header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold mb-2">
            <Shield size={11} /> Admin Control Panel
          </div>
          <h1 className="text-2xl font-black dark:text-neutral-50 text-neutral-900">Admin Dashboard</h1>
          <p className="text-sm dark:text-neutral-400 text-neutral-500 mt-1">Manage users, monitor platform activity and analytics.</p>
        </div>
        <Button variant="ghost" size="sm" icon={<RefreshCw size={14} />} onClick={() => refetch()}>Refresh</Button>
      </div>

      {/* tabs */}
      <div className="flex gap-1 p-1 rounded-xl dark:bg-surface-card bg-lsurface-card border dark:border-surface-border border-lsurface-border w-fit">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={cn('flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all',
              tab === t.id ? 'bg-brand-500 text-white shadow-sm' : 'dark:text-neutral-400 text-neutral-500 hover:dark:text-neutral-200 hover:text-neutral-700')}>
            <t.icon size={13} />{t.label}
          </button>
        ))}
      </div>

      {/* ══ OVERVIEW ══════════════════════════════════════════════════════════ */}
      {tab === 'overview' && (
        <div className="space-y-6">
          {loadingStats ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
          : stats ? (
            <>
              <motion.div variants={stagger} initial="hidden" animate="show" className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard icon={Users}     label="Total Users"      value={stats.total_users}         color="bg-brand-500"   sub={`${stats.active_users} active`} />
                <StatCard icon={Brain}     label="Interviews"       value={stats.total_interviews}    color="bg-purple-600"  sub={`${stats.completed_interviews} completed`} />
                <StatCard icon={FileText}  label="Reports"          value={stats.total_reports}       color="bg-emerald-600" sub="AI generated" />
                <StatCard icon={TrendingUp} label="Avg Score"       value={stats.average_score}       color="bg-amber-500"   sub="platform wide" />
              </motion.div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {[
                  { label: 'Active Users',   value: stats.active_users,         c: 'text-emerald-400' },
                  { label: 'Inactive Users', value: stats.inactive_users,       c: 'text-red-400'     },
                  { label: 'In Progress',    value: stats.pending_interviews,   c: 'text-amber-400'   },
                  { label: 'Completed',      value: stats.completed_interviews, c: 'text-brand-400'   },
                ].map(s => (
                  <Card key={s.label} className="p-4 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card text-center">
                    <p className={cn('text-2xl font-black tabular-nums', s.c)}>{s.value ?? 0}</p>
                    <p className="text-xs dark:text-neutral-500 text-neutral-400 font-semibold mt-0.5">{s.label}</p>
                  </Card>
                ))}
              </div>

              {/* mini charts in overview */}
              {(regData.length > 0 || roleData.length > 0) && (
                <div className="grid sm:grid-cols-2 gap-5">
                  {regData.length > 0 && (
                    <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                      <SH icon={Users} title="Daily Registrations (14d)" />
                      <ResponsiveContainer width="100%" height={160}>
                        <AreaChart data={regData} margin={{ top: 4, right: 8, bottom: 0, left: -14 }}>
                          <defs>
                            <linearGradient id="regGrad" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%"  stopColor={C.brand} stopOpacity={0.3} />
                              <stop offset="95%" stopColor={C.brand} stopOpacity={0}   />
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke={axisC} />
                          <XAxis dataKey="date" tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                          <YAxis allowDecimals={false} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                          <Tooltip {...TIP} formatter={(v: number) => [v, 'Signups']} />
                          <Area type="monotone" dataKey="count" stroke={C.brand} strokeWidth={2} fill="url(#regGrad)" dot={false} />
                        </AreaChart>
                      </ResponsiveContainer>
                    </Card>
                  )}
                  {roleData.length > 0 && (
                    <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                      <SH icon={Brain} title="Top Roles" c="text-purple-400" />
                      <ResponsiveContainer width="100%" height={160}>
                        <BarChart data={roleData} layout="vertical" margin={{ top: 0, right: 8, bottom: 0, left: 4 }} barSize={10}>
                          <CartesianGrid strokeDasharray="3 3" stroke={axisC} horizontal={false} />
                          <XAxis type="number" allowDecimals={false} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                          <YAxis dataKey="role" type="category" width={80} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                          <Tooltip {...TIP} formatter={(v: number) => [v, 'Interviews']} />
                          <Bar dataKey="count" fill={C.purple} radius={[0, 4, 4, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </Card>
                  )}
                </div>
              )}
            </>
          ) : (
            <Card className="p-10 border dark:border-surface-border border-lsurface-border">
              <EmptyState icon={<AlertTriangle size={32} className="text-amber-400" />} title="No data" description="Admin dashboard returned no data." />
            </Card>
          )}
        </div>
      )}

      {/* ══ USERS ═════════════════════════════════════════════════════════════ */}
      {tab === 'users' && (
        <div className="space-y-4">
          <div className="relative max-w-sm">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 dark:text-neutral-400 text-neutral-500" />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search by name or email…"
              className="w-full pl-9 pr-4 py-2.5 text-xs font-medium dark:bg-surface-card bg-lsurface-card border dark:border-surface-border border-lsurface-border rounded-xl dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30" />
          </div>
          {loadingUsers ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
          : filtered.length === 0 ? <EmptyState icon={<Users size={32} />} title="No users found" description="Try a different search term." className="py-16" />
          : (
            <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
              <div className="hidden sm:grid grid-cols-[1fr_1fr_auto_auto_auto] gap-3 px-5 py-3 border-b dark:border-surface-border border-lsurface-border text-xs font-bold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider">
                <span>User</span><span>Email</span><span>Role</span><span>Status</span><span>Actions</span>
              </div>
              <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                {filtered.map(u => (
                  <motion.div key={u.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="grid grid-cols-[1fr_auto] sm:grid-cols-[1fr_1fr_auto_auto_auto] gap-3 items-center px-5 py-3.5 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors">
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center text-xs font-black text-white shrink-0">
                        {u.name?.slice(0, 2).toUpperCase() ?? '??'}
                      </div>
                      <span className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 truncate">{u.name}</span>
                    </div>
                    <span className="hidden sm:block text-xs dark:text-neutral-400 text-neutral-500 truncate">{u.email}</span>
                    <Badge variant={u.role === 'admin' ? 'danger' : 'default'} size="xs" className="w-fit hidden sm:flex">
                      {u.role === 'admin' ? <><Crown size={9} className="mr-1" />Admin</> : 'User'}
                    </Badge>
                    <Badge variant={u.is_active ? 'success' : 'danger'} size="xs" className="w-fit hidden sm:flex">
                      {u.is_active ? 'Active' : 'Inactive'}
                    </Badge>
                    <div className="flex items-center gap-1">
                      {u.is_active
                        ? <button onClick={() => doDeactivate(u.id, { onSuccess: () => showToast('success','User deactivated'), onError: () => showToast('error','Failed') })} disabled={deactivating}
                            className="p-1.5 rounded-lg hover:bg-amber-500/10 text-amber-400 transition-colors"><UserX size={13} /></button>
                        : <button onClick={() => doActivate(u.id,   { onSuccess: () => showToast('success','User activated'),   onError: () => showToast('error','Failed') })} disabled={activating}
                            className="p-1.5 rounded-lg hover:bg-emerald-500/10 text-emerald-400 transition-colors"><UserCheck size={13} /></button>
                      }
                      {confirmDelete === u.id
                        ? <div className="flex items-center gap-1">
                            <button onClick={() => doDelete(u.id, { onSuccess: () => { showToast('info','Deleted'); setConfirmDelete(null) }, onError: () => { showToast('error','Failed'); setConfirmDelete(null) } })} disabled={deleting}
                              className="px-2 py-1 rounded-lg bg-red-500/10 text-red-400 text-xs font-bold hover:bg-red-500/20">{deleting ? '…' : 'Confirm'}</button>
                            <button onClick={() => setConfirmDelete(null)} className="px-2 py-1 rounded-lg dark:text-neutral-400 text-neutral-500 text-xs hover:dark:bg-surface-hover hover:bg-lsurface-hover">Cancel</button>
                          </div>
                        : <button onClick={() => setConfirmDelete(u.id)} className="p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors"><Trash2 size={13} /></button>
                      }
                    </div>
                  </motion.div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}

      {/* ══ ANALYTICS (full charts) ═══════════════════════════════════════════ */}
      {tab === 'analytics' && (
        <div className="space-y-5">
          {loadingAnalytics ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
          : analytics ? (
            <>
              {/* row 1 — registrations area + interviews area */}
              <div className="grid sm:grid-cols-2 gap-5">
                <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <SH icon={Users} title="Daily Registrations" />
                  {regData.length === 0 ? <p className="text-xs dark:text-neutral-500 text-neutral-400">No data yet.</p> : (
                    <ResponsiveContainer width="100%" height={180}>
                      <AreaChart data={regData} margin={{ top: 4, right: 8, bottom: 0, left: -14 }}>
                        <defs>
                          <linearGradient id="rg2" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%"  stopColor={C.green} stopOpacity={0.35} />
                            <stop offset="95%" stopColor={C.green} stopOpacity={0}    />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke={axisC} />
                        <XAxis dataKey="date" tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                        <YAxis allowDecimals={false} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                        <Tooltip {...TIP} formatter={(v: number) => [v, 'New Users']} />
                        <Area type="monotone" dataKey="count" stroke={C.green} strokeWidth={2} fill="url(#rg2)" dot={false} />
                      </AreaChart>
                    </ResponsiveContainer>
                  )}
                </Card>

                <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <SH icon={Brain} title="Interview Summary" c="text-purple-400" />
                  <div className="flex flex-col gap-4 mt-2">
                    {[
                      { label: 'Completed', value: interviewSummary.completed, color: C.green  },
                      { label: 'Pending',   value: interviewSummary.pending,   color: C.amber  },
                    ].map(row => {
                      const total = interviewSummary.completed + interviewSummary.pending || 1
                      const pct = Math.round((row.value / total) * 100)
                      return (
                        <div key={row.label}>
                          <div className="flex justify-between text-xs mb-1.5">
                            <span className="font-semibold dark:text-neutral-200 text-neutral-700">{row.label}</span>
                            <span className="font-black tabular-nums" style={{ color: row.color }}>{row.value} ({pct}%)</span>
                          </div>
                          <div className="h-2.5 rounded-full dark:bg-surface-border bg-neutral-200 overflow-hidden">
                            <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }}
                              transition={{ duration: 0.7, ease: 'easeOut' }}
                              className="h-full rounded-full" style={{ background: row.color }} />
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </Card>
              </div>

              {/* row 2 — difficulty pie + score distribution bar */}
              <div className="grid sm:grid-cols-2 gap-5">
                <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <SH icon={Star} title="Difficulty Distribution" c="text-amber-400" />
                  {diffData.length === 0 ? <p className="text-xs dark:text-neutral-500 text-neutral-400">No data yet.</p> : (
                    <div className="flex items-center gap-5">
                      <ResponsiveContainer width="55%" height={160}>
                        <PieChart>
                          <Pie data={diffData} cx="50%" cy="50%" innerRadius={42} outerRadius={65} paddingAngle={4} dataKey="count">
                            {diffData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                          </Pie>
                          <Tooltip {...TIP} formatter={(v: number) => [v, 'Sessions']} />
                        </PieChart>
                      </ResponsiveContainer>
                      <div className="space-y-2.5 flex-1">
                        {diffData.map(d => (
                          <div key={d.difficulty} className="flex items-center gap-2">
                            <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: d.fill }} />
                            <span className="flex-1 text-xs dark:text-neutral-300 text-neutral-700 capitalize">{d.difficulty}</span>
                            <span className="text-xs font-black tabular-nums dark:text-neutral-200 text-neutral-700">{d.count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </Card>

                <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <SH icon={BarChart3} title="Score Distribution" c="text-cyan-400" />
                  {scoreDist.length === 0 ? <p className="text-xs dark:text-neutral-500 text-neutral-400">No data yet.</p> : (
                    <ResponsiveContainer width="100%" height={160}>
                      <BarChart data={scoreDist} margin={{ top: 4, right: 8, bottom: 0, left: -14 }} barSize={16}>
                        <CartesianGrid strokeDasharray="3 3" stroke={axisC} vertical={false} />
                        <XAxis dataKey="range" tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                        <YAxis allowDecimals={false} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                        <Tooltip {...TIP} formatter={(v: number) => [v, 'Interviews']} />
                        <Bar dataKey="count" fill={C.cyan} radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  )}
                </Card>
              </div>

              {/* row 3 — popular roles horizontal bar */}
              {roleData.length > 0 && (
                <Card className="p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <SH icon={Brain} title="Top Interview Roles" c="text-emerald-400" />
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={roleData} layout="vertical" margin={{ top: 0, right: 16, bottom: 0, left: 8 }} barSize={14}>
                      <CartesianGrid strokeDasharray="3 3" stroke={axisC} horizontal={false} />
                      <XAxis type="number" allowDecimals={false} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                      <YAxis dataKey="role" type="category" width={100} tick={{ fontSize: 9, fill: textC }} axisLine={false} tickLine={false} />
                      <Tooltip {...TIP} formatter={(v: number) => [v, 'Interviews']} />
                      <Bar dataKey="count" fill={C.green} radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Card>
              )}
            </>
          ) : <EmptyState icon={<BarChart3 size={32} />} title="No analytics" description="Analytics appear once users are active." className="py-16" />}
        </div>
      )}

      {/* ══ ACTIVITY ══════════════════════════════════════════════════════════ */}
      {tab === 'activity' && (
        <div className="space-y-5">
          {loadingActivity ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
          : !activity ? <EmptyState icon={<Activity size={32} />} title="No activity" description="Recent activity will appear here." className="py-16" />
          : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

              {/* new users */}
              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
                <div className="px-4 py-3 border-b dark:border-surface-border border-lsurface-border flex items-center gap-2">
                  <Users size={13} className="text-brand-500" />
                  <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider">New Users</span>
                  <Badge variant="default" size="xs" className="ml-auto">{(activity.recent_users ?? []).length}</Badge>
                </div>
                {(activity.recent_users ?? []).length === 0
                  ? <p className="text-xs dark:text-neutral-500 text-neutral-400 p-4">No recent users.</p>
                  : <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                      {(activity.recent_users ?? []).map(u => (
                        <div key={u.id} className="flex items-center gap-3 px-4 py-3 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors">
                          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center text-xs font-black text-white shrink-0">
                            {u.name?.slice(0, 2).toUpperCase()}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 truncate">{u.name}</p>
                            <p className="text-xs dark:text-neutral-500 text-neutral-400 truncate">{u.email}</p>
                          </div>
                          <span className="text-2xs dark:text-neutral-500 text-neutral-400 shrink-0">{new Date(u.created_at).toLocaleDateString()}</span>
                        </div>
                      ))}
                    </div>
                }
              </Card>

              {/* recent interviews */}
              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
                <div className="px-4 py-3 border-b dark:border-surface-border border-lsurface-border flex items-center gap-2">
                  <Brain size={13} className="text-purple-500" />
                  <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider">Interviews</span>
                  <Badge variant="default" size="xs" className="ml-auto">{(activity.recent_interviews ?? []).length}</Badge>
                </div>
                {(activity.recent_interviews ?? []).length === 0
                  ? <p className="text-xs dark:text-neutral-500 text-neutral-400 p-4">No recent interviews.</p>
                  : <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                      {(activity.recent_interviews ?? []).map(iv => (
                        <div key={iv.id} className="px-4 py-3 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors">
                          <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900">{iv.role}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant={iv.difficulty === 'hard' ? 'danger' : iv.difficulty === 'medium' ? 'warning' : 'success'} size="xs">{iv.difficulty}</Badge>
                            <Badge variant={iv.status === 'completed' ? 'success' : 'default'} size="xs">{iv.status}</Badge>
                            <span className="text-2xs dark:text-neutral-500 text-neutral-400 ml-auto">{new Date(iv.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                }
              </Card>

              {/* recent reports */}
              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
                <div className="px-4 py-3 border-b dark:border-surface-border border-lsurface-border flex items-center gap-2">
                  <FileText size={13} className="text-emerald-500" />
                  <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider">Reports</span>
                  <Badge variant="default" size="xs" className="ml-auto">{(activity.recent_reports ?? []).length}</Badge>
                </div>
                {(activity.recent_reports ?? []).length === 0
                  ? <p className="text-xs dark:text-neutral-500 text-neutral-400 p-4">No recent reports.</p>
                  : <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                      {(activity.recent_reports ?? []).map(r => {
                        const col = r.overall_score >= 80 ? C.green : r.overall_score >= 60 ? C.amber : C.red
                        return (
                          <div key={r.id} className="flex items-center gap-3 px-4 py-3 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors">
                            <div className="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-black text-white shrink-0" style={{ background: col }}>
                              {r.overall_score}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900">Interview #{r.interview_id}</p>
                              <p className="text-2xs dark:text-neutral-500 text-neutral-400">{new Date(r.created_at).toLocaleDateString()}</p>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                }
              </Card>
            </div>
          )}
        </div>
      )}

    </div>
  )
}
