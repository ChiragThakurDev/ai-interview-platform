import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Trophy, Crown, Medal, Star, Search,
  TrendingUp, Users, Zap, Target,
} from 'lucide-react'
import { useLeaderboard } from '@/hooks'
import { Card, Spinner, EmptyState } from '@/components/ui'
import { cn } from '@/utils'
import type { LeaderboardEntry } from '@/types'

const scoreColor = (s: number) =>
  s >= 8 ? 'text-emerald-400' : s >= 6 ? 'text-amber-400' : 'text-red-400'

const RankBadge = ({ rank }: { rank: number }) => {
  if (rank === 1) return <Crown size={18} className="text-amber-400" />
  if (rank === 2) return <Medal size={18} className="text-slate-300" />
  if (rank === 3) return <Medal size={18} className="text-orange-400" />
  return <span className="text-xs font-bold dark:text-neutral-500 text-neutral-400">#{rank}</span>
}

const avatarGradient = (rank: number) => {
  if (rank === 1) return 'from-amber-500 to-orange-500'
  if (rank === 2) return 'from-slate-500 to-slate-400'
  if (rank === 3) return 'from-orange-600 to-amber-600'
  return 'from-brand-500 to-purple-600'
}

export const LeaderboardPage = () => {
  const { data: leaderboard, isLoading } = useLeaderboard()
  const [search, setSearch] = useState('')

  const allEntries: LeaderboardEntry[] = leaderboard?.leaderboard ?? []

  const filtered = allEntries.filter(e =>
    !search || e.user_name?.toLowerCase().includes(search.toLowerCase())
  )

  const top3 = filtered.slice(0, 3)
  const rest = filtered.slice(3)

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">

      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl p-6 sm:p-8 border dark:border-amber-500/20 border-amber-200/60 dark:bg-surface-card bg-lsurface-card">
        <div className="absolute -top-12 -right-12 w-40 h-40 rounded-full bg-amber-500/5 blur-2xl pointer-events-none" />
        <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/25 text-amber-400 text-xs font-bold">
              <Trophy size={12} /> Global Rankings
            </div>
            <h1 className="text-2xl sm:text-3xl font-black dark:text-neutral-50 text-neutral-900 tracking-tight">
              Leaderboard
            </h1>
            <p className="dark:text-neutral-400 text-neutral-500 text-sm">
              Real-time rankings across all coding interview candidates.
            </p>
          </div>
          <div className="flex gap-5 shrink-0">
            <div className="text-center">
              <p className="text-2xl font-black text-amber-400 tabular-nums">{allEntries.length}</p>
              <p className="text-xs dark:text-neutral-500 text-neutral-400 font-semibold">Ranked</p>
            </div>
          </div>
        </div>
      </div>

      {isLoading && (
        <div className="flex justify-center py-24"><Spinner size="lg" /></div>
      )}

      {!isLoading && allEntries.length === 0 && (
        <EmptyState
          icon={<Trophy size={40} />}
          title="No rankings yet"
          description="Complete coding interviews to appear on the leaderboard."
          className="py-20"
        />
      )}

      {!isLoading && allEntries.length > 0 && (
        <>
          {/* Podium — top 3 */}
          {top3.length >= 3 && (
            <div>
              <p className="text-xs font-bold dark:text-neutral-500 text-neutral-400 uppercase tracking-widest flex items-center gap-2 mb-5">
                <Star size={12} className="text-amber-400" /> Top 3 Performers
              </p>
              <div className="grid grid-cols-3 gap-3 items-end">
                {/* 2nd */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
                  className="flex flex-col items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-slate-500 to-slate-400 flex items-center justify-center text-sm font-black text-white shadow">
                    {top3[1]?.user_name?.slice(0, 2).toUpperCase()}
                  </div>
                  <div className="text-center">
                    <p className="text-xs font-bold dark:text-neutral-100 text-neutral-900 truncate max-w-[100px]">{top3[1]?.user_name}</p>
                    <p className={cn('text-xs font-black', scoreColor(top3[1]?.best_score))}>{top3[1]?.best_score} pts</p>
                  </div>
                  <div className="w-full h-16 rounded-t-xl dark:bg-slate-700/30 bg-slate-100 border dark:border-slate-600/30 border-slate-200 flex items-start justify-center pt-2">
                    <Medal size={18} className="text-slate-400" />
                  </div>
                </motion.div>
                {/* 1st */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
                  className="flex flex-col items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center text-lg font-black text-white shadow-lg ring-4 ring-amber-500/25">
                    {top3[0]?.user_name?.slice(0, 2).toUpperCase()}
                  </div>
                  <div className="text-center">
                    <p className="text-xs font-bold dark:text-neutral-100 text-neutral-900 truncate max-w-[100px]">{top3[0]?.user_name}</p>
                    <p className={cn('text-base font-black', scoreColor(top3[0]?.best_score))}>{top3[0]?.best_score} pts</p>
                  </div>
                  <div className="w-full h-28 rounded-t-xl dark:bg-amber-500/10 bg-amber-50 border dark:border-amber-500/25 border-amber-200 flex items-start justify-center pt-2">
                    <Crown size={22} className="text-amber-400" />
                  </div>
                </motion.div>
                {/* 3rd */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
                  className="flex flex-col items-center gap-3">
                  <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-orange-600 to-amber-600 flex items-center justify-center text-xs font-black text-white shadow">
                    {top3[2]?.user_name?.slice(0, 2).toUpperCase()}
                  </div>
                  <div className="text-center">
                    <p className="text-xs font-bold dark:text-neutral-100 text-neutral-900 truncate max-w-[100px]">{top3[2]?.user_name}</p>
                    <p className={cn('text-xs font-black', scoreColor(top3[2]?.best_score))}>{top3[2]?.best_score} pts</p>
                  </div>
                  <div className="w-full h-12 rounded-t-xl dark:bg-orange-500/10 bg-orange-50 border dark:border-orange-500/25 border-orange-200 flex items-start justify-center pt-2">
                    <Medal size={16} className="text-orange-400" />
                  </div>
                </motion.div>
              </div>
            </div>
          )}

          {/* Search */}
          <div className="relative max-w-sm">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 dark:text-neutral-400 text-neutral-500" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search candidates…"
              className="w-full pl-9 pr-4 py-2.5 text-xs font-medium dark:bg-surface-card bg-lsurface-card border dark:border-surface-border border-lsurface-border rounded-xl dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            />
          </div>

          {/* Full table */}
          <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
            {/* Header */}
            <div className="px-5 py-3 border-b dark:border-surface-border border-lsurface-border flex items-center gap-2">
              <Users size={14} className="text-brand-500" />
              <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider">Full Rankings</h2>
              <span className="ml-auto text-xs dark:text-neutral-500 text-neutral-400 font-semibold">{filtered.length} candidates</span>
            </div>

            {/* Column labels */}
            <div className="hidden sm:grid grid-cols-[3rem_1fr_auto_auto_auto] gap-3 px-5 py-2.5 border-b dark:border-surface-border border-lsurface-border text-xs font-semibold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider">
              <span>Rank</span><span>Candidate</span>
              <span className="text-right">Interviews</span>
              <span className="text-right">Avg</span>
              <span className="text-right">Best</span>
            </div>

            {filtered.length === 0 ? (
              <div className="py-10">
                <EmptyState title="No results" description="Try a different search term." className="py-6" />
              </div>
            ) : (
              <div className="divide-y dark:divide-surface-border divide-lsurface-border">
                {filtered.map((entry, i) => {
                  const rank = i + 1
                  return (
                    <motion.div key={entry.user_id}
                      initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.02 }}
                      className={cn(
                        'grid grid-cols-[3rem_1fr] sm:grid-cols-[3rem_1fr_auto_auto_auto] gap-3 items-center px-5 py-3.5 transition-colors',
                        rank <= 3
                          ? 'dark:bg-amber-500/5 bg-amber-50/40'
                          : 'dark:hover:bg-surface-hover hover:bg-lsurface-hover'
                      )}
                    >
                      {/* Rank */}
                      <div className="flex items-center justify-center">
                        <RankBadge rank={rank} />
                      </div>

                      {/* Name */}
                      <div className="flex items-center gap-3 min-w-0">
                        <div className={cn(
                          'w-8 h-8 rounded-lg bg-gradient-to-br flex items-center justify-center text-xs font-bold text-white shrink-0',
                          avatarGradient(rank)
                        )}>
                          {entry.user_name?.slice(0, 2).toUpperCase()}
                        </div>
                        <span className="text-sm font-semibold dark:text-neutral-100 text-neutral-900 truncate">
                          {entry.user_name}
                        </span>
                      </div>

                      {/* Interviews */}
                      <div className="hidden sm:flex items-center justify-end gap-1">
                        <Target size={11} className="dark:text-neutral-500 text-neutral-400" />
                        <span className="text-xs font-semibold dark:text-neutral-300 text-neutral-600 tabular-nums">
                          {entry.total_interviews}
                        </span>
                      </div>

                      {/* Avg score */}
                      <div className="hidden sm:flex items-center justify-end gap-1">
                        <TrendingUp size={11} className="dark:text-neutral-500 text-neutral-400" />
                        <span className={cn('text-xs font-semibold tabular-nums', scoreColor(entry.average_score))}>
                          {entry.average_score?.toFixed(1)}
                        </span>
                      </div>

                      {/* Best score */}
                      <div className="flex items-center justify-end gap-1">
                        <Zap size={11} className="text-amber-400" />
                        <span className={cn('text-sm font-black tabular-nums', scoreColor(entry.best_score))}>
                          {entry.best_score}
                        </span>
                      </div>
                    </motion.div>
                  )
                })}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  )
}
