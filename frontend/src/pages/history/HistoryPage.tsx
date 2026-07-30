import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  History, Brain, Code2, Filter, Clock, CheckCircle,
  XCircle, ArrowRight, AlertCircle, Trophy
} from 'lucide-react'
import { useMyInterviews } from '@/hooks'
import { useCodingHistory } from '@/hooks/useCoding'
import { Card, Badge, Button, Spinner, EmptyState } from '@/components/ui'
import { formatDate, scoreColor, difficultyColor } from '@/utils'
import { cn } from '@/utils'

const TYPE_FILTERS = ['All', 'Technical', 'Coding'] as const
const STATUS_FILTERS = ['All', 'Completed', 'In Progress', 'Failed'] as const

type TypeFilter = typeof TYPE_FILTERS[number]
type StatusFilter = typeof STATUS_FILTERS[number]

const StatusIcon = ({ status }: { status: string }) => {
  const s = status?.toLowerCase()
  if (s === 'completed') return <CheckCircle size={14} className="text-emerald-400" />
  if (s === 'failed') return <XCircle size={14} className="text-rose-400" />
  return <AlertCircle size={14} className="text-amber-400" />
}

// Unified interview row shape
interface UnifiedInterview {
  id: number
  type: 'technical' | 'coding'
  title: string
  status: string
  difficulty: string | null
  score: number | null
  created_at: string
  reportUrl: string
}

export const HistoryPage = () => {
  const navigate = useNavigate()
  const { data: technicalData, isLoading: loadingTechnical } = useMyInterviews()
  const { data: codingData, isLoading: loadingCoding } = useCodingHistory()

  const [typeFilter, setTypeFilter] = useState<TypeFilter>('All')
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('All')

  const isLoading = loadingTechnical || loadingCoding

  // Build unified list
  const allInterviews: UnifiedInterview[] = [
    ...(technicalData ?? []).map((iv) => ({
      id: iv.id,
      type: 'technical' as const,
      title: iv.title ?? iv.role ?? 'Technical Interview',
      status: iv.status ?? 'pending',
      difficulty: iv.difficulty ?? null,
      score: iv.score ?? null,
      created_at: iv.created_at,
      reportUrl: `/interview/${iv.id}/report`,
    })),
    ...(codingData?.history ?? []).map((iv) => ({
      id: iv.id,
      type: 'coding' as const,
      title: iv.company ? `${iv.role} @ ${iv.company}` : iv.role,
      status: iv.status ?? 'pending',
      difficulty: iv.difficulty ?? null,
      score: iv.score ?? null,
      created_at: iv.created_at,
      reportUrl: `/coding/${iv.id}/report`,
    })),
  ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

  const filtered = allInterviews.filter((iv) => {
    const matchType =
      typeFilter === 'All' ||
      (typeFilter === 'Technical' && iv.type === 'technical') ||
      (typeFilter === 'Coding' && iv.type === 'coding')

    const matchStatus =
      statusFilter === 'All' ||
      iv.status?.toLowerCase().replace('_', ' ') === statusFilter.toLowerCase()

    return matchType && matchStatus
  })

  const totalTechnical = (technicalData ?? []).length
  const totalCoding = codingData?.history?.length ?? 0

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shadow-sm">
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-500 text-xs font-semibold">
              <History size={13} className="text-brand-500" />
              <span>Session Archive &amp; Scorecards</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
              Interview History
            </h1>
            <p className="dark:text-neutral-400 text-neutral-600 text-sm">
              Full session archive with performance metrics. Click any row to view the full report.
            </p>
          </div>
          <div className="flex items-center gap-6 shrink-0">
            <div className="text-center">
              <p className="text-2xl font-bold text-brand-500">{totalTechnical}</p>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold">Technical</p>
            </div>
            <div className="w-px h-8 dark:bg-surface-border bg-lsurface-border" />
            <div className="text-center">
              <p className="text-2xl font-bold text-amber-400">{totalCoding}</p>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold">Coding</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <div className="flex items-center gap-2">
          <Filter size={13} className="dark:text-neutral-400 text-neutral-500" />
          <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider">Type:</span>
          <div className="flex gap-1.5">
            {TYPE_FILTERS.map((f) => (
              <button
                key={f}
                onClick={() => setTypeFilter(f)}
                className={cn(
                  'px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border',
                  typeFilter === f
                    ? 'dark:bg-brand-500/10 bg-brand-500/10 text-brand-500 dark:border-brand-500/30 border-brand-500/30'
                    : 'dark:text-neutral-400 text-neutral-600 dark:border-surface-border border-lsurface-border dark:hover:bg-surface-hover hover:bg-lsurface-hover'
                )}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider">Status:</span>
          <div className="flex gap-1.5 flex-wrap">
            {STATUS_FILTERS.map((f) => (
              <button
                key={f}
                onClick={() => setStatusFilter(f)}
                className={cn(
                  'px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border',
                  statusFilter === f
                    ? 'dark:bg-brand-500/10 bg-brand-500/10 text-brand-500 dark:border-brand-500/30 border-brand-500/30'
                    : 'dark:text-neutral-400 text-neutral-600 dark:border-surface-border border-lsurface-border dark:hover:bg-surface-hover hover:bg-lsurface-hover'
                )}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </div>

      {isLoading && (
        <div className="flex justify-center py-24"><Spinner size="lg" /></div>
      )}

      {!isLoading && (
        <>
          {filtered.length === 0 ? (
            <EmptyState
              icon={<History size={40} />}
              title="No session history"
              description="Start your first interview or coding challenge to populate your history."
              action={
                <div className="flex gap-3">
                  <Link to="/interview"><Button size="sm" variant="primary" icon={<Brain size={14} />}>Technical Interview</Button></Link>
                  <Link to="/coding"><Button size="sm" variant="secondary" icon={<Code2 size={14} />}>Coding Arena</Button></Link>
                </div>
              }
              className="py-20"
            />
          ) : (
            <div className="space-y-3">
              {filtered.map((iv, i) => {
                const isCoding = iv.type === 'coding'
                const isCompleted = iv.status?.toLowerCase() === 'completed'

                return (
                  <motion.div
                    key={`${iv.type}-${iv.id}`}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.03 }}
                    onClick={() => isCompleted && navigate(iv.reportUrl)}
                    className={isCompleted ? 'cursor-pointer' : ''}
                  >
                    <Card className={cn(
                      'border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-4 sm:p-5 transition-all duration-200',
                      isCompleted && 'hover-lift hover:dark:border-brand-500/40 hover:border-brand-500/30 group'
                    )}>
                      <div className="flex items-center gap-4">
                        {/* Type Icon */}
                        <div className={cn(
                          'p-3 rounded-xl shrink-0 transition-transform',
                          isCompleted && 'group-hover:scale-105',
                          isCoding
                            ? 'dark:bg-amber-500/10 bg-amber-500/10 text-amber-400'
                            : 'dark:bg-brand-500/10 bg-brand-500/10 text-brand-500'
                        )}>
                          {isCoding ? <Code2 size={18} /> : <Brain size={18} />}
                        </div>

                        {/* Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1 flex-wrap">
                            <p className="text-sm font-semibold dark:text-neutral-100 text-neutral-900 truncate">
                              {iv.title}
                            </p>
                            <Badge variant={isCoding ? 'warning' : 'purple'} size="xs">
                              {isCoding ? 'Coding' : 'Technical'}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-3 flex-wrap">
                            <span className="flex items-center gap-1 text-[11px] font-semibold dark:text-neutral-400 text-neutral-500">
                              <Clock size={11} /> {formatDate(iv.created_at)}
                            </span>
                            {iv.difficulty && (
                              <span className={cn('text-[11px] px-2 py-0.5 rounded-full font-semibold', difficultyColor(iv.difficulty))}>
                                {iv.difficulty}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Status & Score */}
                        <div className="flex items-center gap-4 shrink-0">
                          <div className="flex items-center gap-1.5 text-xs font-semibold dark:text-neutral-300 text-neutral-600">
                            <StatusIcon status={iv.status} />
                            <span className="hidden sm:block capitalize">{iv.status?.replace('_', ' ')}</span>
                          </div>

                          {iv.score != null && (
                            <div className="flex items-center gap-1">
                              <Trophy size={12} className={scoreColor(iv.score)} />
                              <span className={cn('text-sm font-bold', scoreColor(iv.score))}>
                                {iv.score}
                              </span>
                            </div>
                          )}

                          {isCompleted ? (
                            <div className={cn(
                              'flex items-center gap-1 text-xs font-semibold text-brand-500 opacity-0 transition-opacity',
                              'group-hover:opacity-100'
                            )}>
                              <span className="hidden sm:block">View Report</span>
                              <ArrowRight size={13} />
                            </div>
                          ) : (
                            <span className="text-[11px] dark:text-neutral-500 text-neutral-400 font-medium">
                              {iv.status === 'running' ? 'In progress…' : 'Pending'}
                            </span>
                          )}
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                )
              })}
            </div>
          )}
        </>
      )}
    </div>
  )
}
