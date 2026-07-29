import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Brain, Code2, Trophy, ArrowRight, CheckCircle, Star,
  Target, Flame, Clock, TrendingUp, BarChart3, PieChart as PieIcon,
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, RadarChart,
  Radar, PolarGrid, PolarAngleAxis, Tooltip, ResponsiveContainer,
  XAxis, YAxis, CartesianGrid,
} from 'recharts'
import {
  useDashboard, useLeaderboard, usePerformanceHistory,
  useAnalytics, useTopicAnalysis, useProgress,
} from '@/hooks'
import { useAuthStore } from '@/store'
import { useThemeStore } from '@/store'
import { Card, Button, Spinner, EmptyState, Badge } from '@/components/ui'
import { formatDate, scoreColor, difficultyColor } from '@/utils'

const fadeUp = { hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } }
const stagger = { show: { transition: { staggerChildren: 0.06 } } }

// ── Palette ──────────────────────────────────────────────────────────────────
const BRAND   = '#6366f1'
const GREEN   = '#10b981'
const AMBER   = '#f59e0b'
const RED     = '#ef4444'
const PURPLE  = '#8b5cf6'
const CYAN    = '#06b6d4'
const DIFF_COLORS: Record<string, string> = { easy: GREEN, medium: AMBER, hard: RED }

// ── Tooltip styles ────────────────────────────────────────────────────────────
const TooltipStyle = {
  contentStyle: {
    background: '#141523', border: '1px solid #2a2d3e',
    borderRadius: '10px', fontSize: '11px', color: '#e2e8f0',
  },
  cursor: { fill: 'rgba(99,102,241,0.08)' },
}

// ── Stat card ─────────────────────────────────────────────────────────────────
const StatCard = ({
  label, value, icon: Icon, color, sub,
}: { label: string; value: string | number; icon: React.ElementType; color: string; sub?: string }) => (
  <motion.div variants={fadeUp}>
    <Card className="flex items-center gap-4 p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
      <div className={`p-3 rounded-xl ${color} shrink-0`}>
        <Icon size={18} className="text-white" />
      </div>
      <div>
        <p className="text-2xl font-black dark:text-neutral-100 text-neutral-900 leading-none tabular-nums">{value}</p>
        <p className="text-xs dark:text-neutral-500 text-neutral-400 mt-0.5 font-medium">{label}</p>
        {sub && <p className="text-xs text-brand-400 font-semibold mt-0.5">{sub}</p>}
      </div>
    </Card>
  </motion.div>
)

// ── Section header ────────────────────────────────────────────────────────────
const SectionTitle = ({ icon: Icon, title, color = 'text-brand-500' }: { icon: React.ElementType; title: string; color?: string }) => (
  <div className="flex items-center gap-2 mb-4">
    <Icon size={15} className={color} />
    <h2 className="text-xs font-bold dark:text-neutral-200 text-neutral-700 uppercase tracking-widest">{title}</h2>
  </div>
)

// ── Custom dot for area chart ─────────────────────────────────────────────────
const CustomDot = (props: any) => {
  const { cx, cy, value } = props
  if (!value) return null
  return <circle cx={cx} cy={cy} r={4} fill={BRAND} stroke="#141523" strokeWidth={2} />
}

export const DashboardPage = () => {
  const { user } = useAuthStore()
  const { theme } = useThemeStore()
  const isDark = theme === 'dark'

  const { data, isLoading, error } = useDashboard()
  const { data: leaderboardData } = useLeaderboard()
  const { data: perfHistory } = usePerformanceHistory()
  const { data: analytics } = useAnalytics()
  const { data: topics } = useTopicAnalysis()
  const { data: progress } = useProgress()

  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'

  // ── Chart data prep ──────────────────────────────────────────────────────
  const perfData = (perfHistory?.history ?? []).slice(-10).map(p => ({
    date: typeof p.date === 'string' ? p.date.slice(0, 10).slice(5) : '',
    score: p.score,
    role: p.role,
  }))

  const diffData = analytics?.difficulty_stats
    ? [
        { name: 'Easy',   value: analytics.difficulty_stats.easy,   fill: GREEN },
        { name: 'Medium', value: analytics.difficulty_stats.medium, fill: AMBER },
        { name: 'Hard',   value: analytics.difficulty_stats.hard,   fill: RED   },
      ]
    : []

  const scoreDistData = analytics?.score_distribution
    ? Object.entries(analytics.score_distribution).map(([range, count]) => ({ range, count }))
    : []

  const topicData = (topics?.topics ?? []).slice(0, 7).map(t => ({
    topic: t.topic.length > 14 ? t.topic.slice(0, 14) + '…' : t.topic,
    score: Math.round(t.average_score),
    questions: t.total_questions,
  }))

  const roleData = analytics?.role_stats
    ? Object.entries(analytics.role_stats).slice(0, 6).map(([role, count]) => ({
        role: role.length > 18 ? role.slice(0, 18) + '…' : role,
        count,
      }))
    : []

  // progress trend — backend uses: improving | declining | no_change | no_interviews | first_interview
  const trendLabel = progress
    ? progress.trend === 'improving'  ? `↑ +${progress.improvement} pts`
    : progress.trend === 'declining'  ? `↓ ${Math.abs(progress.improvement)} pts`
    : progress.trend === 'no_change'  ? 'No change'
    : undefined
    : undefined

  const axisColor = isDark ? '#4b5563' : '#d1d5db'
  const textColor = isDark ? '#9ca3af' : '#6b7280'

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in pb-8">

      {/* ── Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-black dark:text-neutral-100 text-neutral-900">
            {greeting}, {user?.name?.split(' ')[0] ?? 'there'} 👋
          </h1>
          <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-0.5">Here's your interview prep overview</p>
        </div>
        <div className="flex gap-2">
          <Link to="/interview"><Button variant="secondary" size="sm" icon={<Brain size={13} />}>Practice</Button></Link>
          <Link to="/coding"><Button variant="primary" size="sm" icon={<Code2 size={13} />}>Code</Button></Link>
        </div>
      </div>

      {isLoading && <div className="flex justify-center py-20"><Spinner size="lg" /></div>}
      {error && (
        <Card className="text-center py-10 border dark:border-surface-border border-lsurface-border">
          <p className="text-xs dark:text-neutral-500 text-neutral-400">Failed to load dashboard.</p>
          <Button variant="ghost" size="sm" className="mt-2" onClick={() => window.location.reload()}>Retry</Button>
        </Card>
      )}

      {data && (
        <>
          {/* ── Stats ── */}
          <motion.div variants={stagger} initial="hidden" animate="show"
            className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard label="Total Interviews" value={data.total_interviews ?? 0}   icon={Flame}       color="bg-brand-500" />
            <StatCard label="Questions Answered" value={data.total_questions_answered ?? 0} icon={CheckCircle} color="bg-emerald-600" />
            <StatCard label="Average Score"  value={data.average_score != null ? `${Math.round(data.average_score)}` : '—'} icon={Target} color="bg-blue-600"
              sub={trendLabel} />
            <StatCard label="Best Score"     value={data.highest_score ?? '—'}       icon={Star}        color="bg-amber-500" />
          </motion.div>

          {/* ── Performance history chart ── */}
          {perfData.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
                <SectionTitle icon={TrendingUp} title="Performance History" />
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={perfData} margin={{ top: 4, right: 8, bottom: 0, left: -10 }}>
                    <defs>
                      <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%"  stopColor={BRAND} stopOpacity={0.3} />
                        <stop offset="95%" stopColor={BRAND} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke={axisColor} />
                    <XAxis dataKey="date" tick={{ fontSize: 10, fill: textColor }} axisLine={false} tickLine={false} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: textColor }} axisLine={false} tickLine={false} />
                    <Tooltip {...TooltipStyle} formatter={(v: number) => [`${v}/100`, 'Score']} labelFormatter={l => `Date: ${l}`} />
                    <Area type="monotone" dataKey="score" stroke={BRAND} strokeWidth={2.5}
                      fill="url(#scoreGrad)" dot={<CustomDot />} activeDot={{ r: 5, fill: BRAND }} />
                  </AreaChart>
                </ResponsiveContainer>
              </Card>
            </motion.div>
          )}

          {/* ── Analytics row: difficulty pie + score bar ── */}
          {(diffData.length > 0 || scoreDistData.length > 0) && (
            <div className="grid sm:grid-cols-2 gap-5">

              {/* Difficulty avg score bars */}
              {diffData.length > 0 && (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                  <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
                    <SectionTitle icon={PieIcon} title="Avg Score by Difficulty" color="text-amber-400" />
                    <div className="space-y-4 mt-2">
                      {diffData.map(d => (
                        <div key={d.name}>
                          <div className="flex justify-between text-xs mb-1.5">
                            <span className="font-semibold dark:text-neutral-200 text-neutral-700">{d.name}</span>
                            <span className="font-black tabular-nums" style={{ color: d.fill }}>{d.value}/100</span>
                          </div>
                          <div className="h-2.5 rounded-full dark:bg-surface-border bg-neutral-200 overflow-hidden">
                            <motion.div initial={{ width: 0 }} animate={{ width: `${d.value}%` }}
                              transition={{ duration: 0.7, ease: 'easeOut' }}
                              className="h-full rounded-full" style={{ background: d.fill }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
                </motion.div>
              )}

              {/* Score distribution bar */}
              {scoreDistData.length > 0 && (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
                  <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
                    <SectionTitle icon={BarChart3} title="Score Distribution" color="text-purple-400" />
                    <ResponsiveContainer width="100%" height={160}>
                      <BarChart data={scoreDistData} margin={{ top: 4, right: 8, bottom: 0, left: -14 }} barSize={16}>
                        <CartesianGrid strokeDasharray="3 3" stroke={axisColor} vertical={false} />
                        <XAxis dataKey="range" tick={{ fontSize: 9, fill: textColor }} axisLine={false} tickLine={false} />
                        <YAxis tick={{ fontSize: 9, fill: textColor }} axisLine={false} tickLine={false} />
                        <Tooltip {...TooltipStyle} formatter={(v: number) => [v, 'Interviews']} />
                        <Bar dataKey="count" fill={PURPLE} radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>
                </motion.div>
              )}
            </div>
          )}

          {/* ── Topic radar + role bar ── */}
          {(topicData.length > 0 || roleData.length > 0) && (
            <div className="grid sm:grid-cols-2 gap-5">

              {/* Topic radar */}
              {topicData.length >= 3 && (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                  <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
                    <SectionTitle icon={Brain} title="Topic Mastery" color="text-cyan-400" />
                    <ResponsiveContainer width="100%" height={210}>
                      <RadarChart data={topicData} margin={{ top: 0, right: 20, bottom: 0, left: 20 }}>
                        <PolarGrid stroke={axisColor} />
                        <PolarAngleAxis dataKey="topic" tick={{ fontSize: 9, fill: textColor }} />
                        <Radar dataKey="score" stroke={CYAN} fill={CYAN} fillOpacity={0.18} strokeWidth={2} dot />
                        <Tooltip {...TooltipStyle} formatter={(v: number) => [`${v}/100`, 'Score']} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </Card>
                </motion.div>
              )}

              {/* Popular roles */}
              {roleData.length > 0 && (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.33 }}>
                  <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
                    <SectionTitle icon={Target} title="Interviews by Role" color="text-emerald-400" />
                    <ResponsiveContainer width="100%" height={210}>
                      <BarChart data={roleData} layout="vertical"
                        margin={{ top: 0, right: 8, bottom: 0, left: 4 }} barSize={12}>
                        <CartesianGrid strokeDasharray="3 3" stroke={axisColor} horizontal={false} />
                        <XAxis type="number" tick={{ fontSize: 9, fill: textColor }} axisLine={false} tickLine={false} />
                        <YAxis dataKey="role" type="category" width={90} tick={{ fontSize: 9, fill: textColor }} axisLine={false} tickLine={false} />
                        <Tooltip {...TooltipStyle} formatter={(v: number) => [v, 'Interviews']} />
                        <Bar dataKey="count" fill={GREEN} radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>
                </motion.div>
              )}
            </div>
          )}

          {/* ── Recent interviews + leaderboard ── */}
          <div className="grid lg:grid-cols-3 gap-5">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="lg:col-span-2">
              <Card noPad className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                <div className="flex items-center justify-between px-5 py-3.5 border-b dark:border-surface-border border-lsurface-border">
                  <span className="text-xs font-bold dark:text-neutral-200 text-neutral-700 flex items-center gap-1.5 uppercase tracking-wider">
                    <Clock size={13} className="text-brand-500" /> Recent Interviews
                  </span>
                  <Link to="/history"><Button variant="ghost" size="xs">View all <ArrowRight size={11} /></Button></Link>
                </div>
                {!data.recent_interviews?.length ? (
                  <EmptyState icon={<Brain size={28} />} title="No interviews yet"
                    description="Start a technical or coding interview to see results here."
                    action={<Link to="/interview"><Button size="sm" variant="primary" className="mt-1">Start interview</Button></Link>}
                    className="py-10" />
                ) : (
                  <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                    {data.recent_interviews.map((iv, i) => (
                      <motion.div key={iv.id}
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.04 }}
                        className="flex items-center justify-between px-5 py-3.5 dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-colors">
                        <div className="flex items-center gap-3 min-w-0">
                          <div className="w-8 h-8 rounded-lg bg-brand-500/10 flex items-center justify-center shrink-0">
                            <Brain size={14} className="text-brand-500" />
                          </div>
                          <div className="min-w-0">
                            <p className="text-xs font-semibold dark:text-neutral-200 text-neutral-800 truncate">{iv.role}</p>
                            <p className="text-2xs dark:text-neutral-500 text-neutral-400">{formatDate(iv.created_at)}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className={`text-2xs px-2 py-0.5 rounded-full font-semibold border ${difficultyColor(iv.difficulty)}`}>{iv.difficulty}</span>
                          {iv.score != null && (
                            <span className={`text-sm font-black tabular-nums ${scoreColor(iv.score)}`}>{iv.score}</span>
                          )}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </Card>
            </motion.div>

            {/* Leaderboard */}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}>
              <Card noPad className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                <div className="flex items-center justify-between px-5 py-3.5 border-b dark:border-surface-border border-lsurface-border">
                  <span className="text-xs font-bold dark:text-neutral-200 text-neutral-700 flex items-center gap-1.5 uppercase tracking-wider">
                    <Trophy size={13} className="text-amber-400" /> Leaderboard
                  </span>
                  <Link to="/leaderboard"><Button variant="ghost" size="xs">Full <ArrowRight size={11} /></Button></Link>
                </div>
                {!leaderboardData?.leaderboard?.length ? (
                  <EmptyState title="No rankings" description="Complete interviews to rank." className="py-8" />
                ) : (
                  <div className="p-2 space-y-0.5">
                    {leaderboardData.leaderboard.slice(0, 6).map((e, i) => (
                      <div key={e.user_id} className="flex items-center gap-2.5 px-3 py-2 rounded-lg dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-colors">
                        <span className={`w-5 h-5 flex items-center justify-center rounded text-2xs font-black shrink-0
                          ${i === 0 ? 'bg-amber-500/20 text-amber-400' : i === 1 ? 'bg-neutral-500/15 dark:text-neutral-300 text-neutral-500' : i === 2 ? 'bg-orange-500/15 text-orange-400' : 'dark:bg-surface-raised bg-neutral-100 dark:text-neutral-500 text-neutral-400'}`}>
                          {i + 1}
                        </span>
                        <span className="flex-1 text-xs dark:text-neutral-300 text-neutral-700 truncate font-medium">{e.user_name}</span>
                        <span className={`text-xs font-black tabular-nums ${scoreColor(e.best_score)}`}>{e.best_score}</span>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </motion.div>
          </div>

          {/* ── Quick start ── */}
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
            <p className="text-xs font-bold dark:text-neutral-500 text-neutral-400 uppercase tracking-widest mb-3">Quick Start</p>
            <div className="grid sm:grid-cols-3 gap-3">
              {[
                { to: '/resume',    icon: Brain,   title: 'Resume Analysis',     desc: 'Upload resume for AI skill assessment and tailored questions.', accent: 'text-brand-500',   bg: 'bg-brand-500/10'   },
                { to: '/interview', icon: Target,  title: 'Technical Interview', desc: 'Practice role-specific Q&A with instant AI feedback.',         accent: 'text-blue-400',   bg: 'bg-blue-500/10'    },
                { to: '/coding',    icon: Code2,   title: 'Coding Interview',    desc: 'Solve challenges in Monaco editor with live evaluation.',       accent: 'text-emerald-400',bg: 'bg-emerald-500/10' },
              ].map(({ to, icon: Icon, title, desc, accent, bg }) => (
                <Link key={to} to={to}>
                  <Card hover className="h-full p-5 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card group transition-all hover:border-brand-500/30">
                    <div className={`w-9 h-9 rounded-xl ${bg} flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                      <Icon size={17} className={accent} />
                    </div>
                    <p className="text-sm font-bold dark:text-neutral-200 text-neutral-800 mb-1">{title}</p>
                    <p className="text-xs dark:text-neutral-500 text-neutral-500 leading-relaxed">{desc}</p>
                  </Card>
                </Link>
              ))}
            </div>
          </motion.div>
        </>
      )}
    </div>
  )
}
