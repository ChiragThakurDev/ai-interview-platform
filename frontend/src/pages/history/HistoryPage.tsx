import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  History, Brain, Code2, Filter, Clock, CheckCircle,
  XCircle, AlertCircle, ArrowRight, Trophy, ChevronDown,
  ChevronUp, PlayCircle, BarChart2, Timer, Layers,
} from 'lucide-react'
import { useMyInterviews } from '@/hooks'
import { useCodingHistory } from '@/hooks/useCoding'
import { Card, Badge, Button, Spinner, EmptyState } from '@/components/ui'
import { formatDate, formatDuration, scoreColor, difficultyColor } from '@/utils'
import { cn } from '@/utils'

// ── Types ─────────────────────────────────────────────────────────────────────
const TYPE_FILTERS   = ['All', 'Technical', 'Coding'] as const
const STATUS_FILTERS = ['All', 'Completed', 'In Progress', 'Pending'] as const
type TypeFilter   = typeof TYPE_FILTERS[number]
type StatusFilter = typeof STATUS_FILTERS[number]

interface UnifiedInterview {
  id:         number
  type:       'technical' | 'coding'
  title:      string
  rawStatus:  string          // exact value from backend
  normStatus: StatusFilter    // normalised for display & filtering
  difficulty: string | null
  score:      number | null
  duration:   number | null
  created_at: string
  reportUrl:  string
  resumeUrl:  string
}

// ── Helpers ───────────────────────────────────────────────────────────────────
/** Map any backend status string to one of our four display buckets */
const normaliseStatus = (s: string | null | undefined): StatusFilter => {
  switch ((s ?? '').toLowerCase().replace(/-/g, '_')) {
    case 'completed':   return 'Completed'
    case 'in_progress':
    case 'running':
    case 'started':     return 'In Progress'
    case 'failed':      return 'Pending'  // treat explicitly failed as pending
    default:            return 'Pending'
  }
}

const STATUS_CONFIG: Record<StatusFilter, { icon: React.ReactNode; cls: string; dot: string }> = {
  Completed:   { icon: <CheckCircle  size={13} />, cls: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/25', dot: 'bg-emerald-400' },
  'In Progress':{ icon: <PlayCircle  size={13} />, cls: 'text-blue-400    bg-blue-500/10    border-blue-500/25',    dot: 'bg-blue-400 animate-pulse' },
  Pending:     { icon: <AlertCircle  size={13} />, cls: 'text-amber-400   bg-amber-500/10   border-amber-500/25',  dot: 'bg-amber-400' },
  All:         { icon: null,                        cls: '',                                                          dot: '' },
}

// ── Expandable row ────────────────────────────────────────────────────────────
const InterviewRow = ({ iv, index }: { iv: UnifiedInterview; index: number }) => {
  const [open, setOpen] = useState(false)
  const navigate        = useNavigate()
  const cfg             = STATUS_CONFIG[iv.normStatus]
  const isCoding        = iv.type === 'coding'
  const isCompleted     = iv.normStatus === 'Completed'
  const isInProgress    = iv.normStatus === 'In Progress'

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03 }}
    >
      <Card className={cn(
        'border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card',
        'transition-all duration-200 overflow-hidden',
        open && 'dark:border-brand-500/30 border-brand-500/20',
      )}>

        {/* ── Summary row (always visible) ───────────────────────── */}
        <button
          className="w-full flex items-center gap-4 p-4 sm:p-5 text-left group"
          onClick={() => setOpen(v => !v)}
          aria-expanded={open}
        >
          {/* Type icon */}
          <div className={cn(
            'p-3 rounded-xl shrink-0 transition-transform group-hover:scale-105',
            isCoding
              ? 'dark:bg-amber-500/10 bg-amber-50 text-amber-400'
              : 'dark:bg-brand-500/10 bg-brand-50 text-brand-500',
          )}>
            {isCoding ? <Code2 size={18} /> : <Brain size={18} />}
          </div>

          {/* Title + meta */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-0.5 flex-wrap">
              <p className="text-sm font-semibold dark:text-neutral-100 text-neutral-900 truncate">
                {iv.title}
              </p>
              <Badge variant={isCoding ? 'warning' : 'primary'} size="xs">
                {isCoding ? 'Coding' : 'Technical'}
              </Badge>
            </div>
            <div className="flex items-center gap-3 flex-wrap">
              <span className="flex items-center gap-1 text-[11px] font-medium dark:text-neutral-500 text-neutral-400">
                <Clock size={10} /> {formatDate(iv.created_at)}
              </span>
              {iv.difficulty && (
                <span className={cn('text-[11px] px-2 py-0.5 rounded-full font-semibold', difficultyColor(iv.difficulty))}>
                  {iv.difficulty}
                </span>
              )}
              {iv.duration != null && iv.duration > 0 && (
                <span className="flex items-center gap-1 text-[11px] dark:text-neutral-500 text-neutral-400">
                  <Timer size={10} /> {formatDuration(iv.duration)}
                </span>
              )}
            </div>
          </div>

          {/* Status pill + score + chevron */}
          <div className="flex items-center gap-3 shrink-0">
            {/* Status */}
            <span className={cn(
              'hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold border',
              cfg.cls,
            )}>
              <span className={cn('w-1.5 h-1.5 rounded-full', cfg.dot)} />
              {iv.normStatus}
            </span>

            {/* Score */}
            {iv.score != null && (
              <div className="flex items-center gap-1">
                <Trophy size={12} className={scoreColor(iv.score)} />
                <span className={cn('text-sm font-bold tabular-nums', scoreColor(iv.score))}>
                  {iv.score}
                </span>
              </div>
            )}

            {/* Chevron */}
            <div className="p-1 rounded-lg dark:text-neutral-500 text-neutral-400 group-hover:dark:text-neutral-200 group-hover:text-neutral-700 transition-colors">
              {open ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
            </div>
          </div>
        </button>

        {/* ── Expanded detail panel ───────────────────────────────── */}
        <AnimatePresence>
          {open && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2, ease: 'easeInOut' }}
              className="overflow-hidden"
            >
              <div className="px-4 sm:px-5 pb-5 pt-1 space-y-4 border-t dark:border-surface-border border-lsurface-border">

                {/* Stat chips */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-3">
                  <StatChip
                    icon={<BarChart2 size={13} />}
                    label="Status"
                    value={iv.normStatus}
                    valueClass={cfg.cls.split(' ')[0]}
                  />
                  <StatChip
                    icon={<Trophy size={13} />}
                    label="Score"
                    value={iv.score != null ? `${iv.score} / 100` : '—'}
                    valueClass={iv.score != null ? scoreColor(iv.score) : ''}
                  />
                  <StatChip
                    icon={<Timer size={13} />}
                    label="Duration"
                    value={formatDuration(iv.duration)}
                  />
                  <StatChip
                    icon={<Layers size={13} />}
                    label="Difficulty"
                    value={iv.difficulty ?? '—'}
                  />
                </div>

                {/* Status-specific message */}
                {isInProgress && (
                  <div className="flex items-start gap-2.5 px-3 py-2.5 rounded-xl bg-blue-500/5 border border-blue-500/15 text-xs dark:text-blue-300 text-blue-600 leading-relaxed">
                    <PlayCircle size={14} className="shrink-0 mt-0.5" />
                    <span>This session is still in progress. You can resume it and pick up exactly where you left off.</span>
                  </div>
                )}

                {iv.normStatus === 'Pending' && (
                  <div className="flex items-start gap-2.5 px-3 py-2.5 rounded-xl bg-amber-500/5 border border-amber-500/15 text-xs dark:text-amber-300 text-amber-700 leading-relaxed">
                    <AlertCircle size={14} className="shrink-0 mt-0.5" />
                    <span>This interview hasn't been started yet. Head to the setup page to begin.</span>
                  </div>
                )}

                {/* Action buttons */}
                <div className="flex items-center gap-2 flex-wrap pt-1">
                  {isCompleted && (
                    <Button
                      variant="primary"
                      size="sm"
                      icon={<ArrowRight size={13} />}
                      onClick={() => navigate(iv.reportUrl)}
                    >
                      View Full Report
                    </Button>
                  )}

                  {isInProgress && (
                    <Button
                      variant="primary"
                      size="sm"
                      icon={<PlayCircle size={13} />}
                      onClick={() => navigate(iv.resumeUrl)}
                    >
                      Resume Session
                    </Button>
                  )}

                  {iv.normStatus === 'Pending' && (
                    <Button
                      variant="secondary"
                      size="sm"
                      icon={<Brain size={13} />}
                      onClick={() => navigate(isCoding ? '/coding' : '/interview')}
                    >
                      Start New Session
                    </Button>
                  )}

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setOpen(false)}
                  >
                    Close
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    </motion.div>
  )
}

// ── Stat chip ─────────────────────────────────────────────────────────────────
const StatChip = ({
  icon, label, value, valueClass = '',
}: { icon: React.ReactNode; label: string; value: string; valueClass?: string }) => (
  <div className="flex flex-col gap-1 px-3 py-2.5 rounded-xl dark:bg-surface-base bg-lsurface-base border dark:border-surface-border border-lsurface-border">
    <div className="flex items-center gap-1.5 dark:text-neutral-500 text-neutral-400">
      {icon}
      <span className="text-[10px] font-semibold uppercase tracking-wider">{label}</span>
    </div>
    <p className={cn('text-xs font-bold dark:text-neutral-100 text-neutral-900 capitalize', valueClass)}>
      {value}
    </p>
  </div>
)

// ─────────────────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────────────────
export const HistoryPage = () => {
  const { data: technicalData, isLoading: loadingTechnical } = useMyInterviews()
  const { data: codingData,    isLoading: loadingCoding }    = useCodingHistory()

  const [typeFilter,   setTypeFilter]   = useState<TypeFilter>('All')
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('All')

  const isLoading = loadingTechnical || loadingCoding

  // Build unified list
  const allInterviews: UnifiedInterview[] = [
    ...(technicalData ?? []).map(iv => ({
      id:         iv.id,
      type:       'technical' as const,
      title:      iv.title ?? iv.role ?? 'Technical Interview',
      rawStatus:  iv.status ?? 'pending',
      normStatus: normaliseStatus(iv.status),
      difficulty: iv.difficulty ?? null,
      score:      iv.score ?? null,
      duration:   (iv as { duration?: number }).duration ?? null,
      created_at: iv.created_at,
      reportUrl:  `/results/${iv.id}`,
      resumeUrl:  `/interview/${iv.id}/session`,
    })),
    ...(codingData?.history ?? []).map(iv => ({
      id:         iv.id,
      type:       'coding' as const,
      title:      iv.company ? `${iv.role} @ ${iv.company}` : iv.role,
      rawStatus:  iv.status ?? 'pending',
      normStatus: normaliseStatus(iv.status),
      difficulty: iv.difficulty ?? null,
      score:      iv.score ?? null,
      duration:   (iv as { duration?: number }).duration ?? null,
      created_at: iv.created_at,
      reportUrl:  `/coding/${iv.id}/report`,
      resumeUrl:  `/coding/${iv.id}`,
    })),
  ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

  const filtered = allInterviews.filter(iv => {
    const matchType =
      typeFilter === 'All' ||
      (typeFilter === 'Technical' && iv.type === 'technical') ||
      (typeFilter === 'Coding'    && iv.type === 'coding')

    const matchStatus =
      statusFilter === 'All' || iv.normStatus === statusFilter

    return matchType && matchStatus
  })

  // Counts for header
  const totalTechnical = (technicalData ?? []).length
  const totalCoding    = codingData?.history?.length ?? 0

  // Status summary counts
  const counts = {
    completed:  allInterviews.filter(i => i.normStatus === 'Completed').length,
    inProgress: allInterviews.filter(i => i.normStatus === 'In Progress').length,
    pending:    allInterviews.filter(i => i.normStatus === 'Pending').length,
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">

      {/* ── Header banner ─────────────────────────────────────────── */}
      <div className="relative overflow-hidden rounded-2xl p-6 sm:p-8 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-500 text-xs font-semibold">
              <History size={13} />
              <span>Session Archive &amp; Scorecards</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
              Interview History
            </h1>
            <p className="dark:text-neutral-400 text-neutral-600 text-sm">
              Full session archive with performance metrics. Click any row to expand details.
            </p>
          </div>

          {/* Stats */}
          <div className="flex items-center gap-5 shrink-0 flex-wrap">
            <div className="text-center">
              <p className="text-2xl font-bold text-brand-500">{totalTechnical}</p>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold">Technical</p>
            </div>
            <div className="w-px h-8 dark:bg-surface-border bg-lsurface-border" />
            <div className="text-center">
              <p className="text-2xl font-bold text-amber-400">{totalCoding}</p>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold">Coding</p>
            </div>
            <div className="w-px h-8 dark:bg-surface-border bg-lsurface-border" />
            <div className="flex gap-3">
              <span className="flex flex-col items-center gap-0.5">
                <span className="text-sm font-bold text-emerald-400">{counts.completed}</span>
                <span className="text-[10px] dark:text-neutral-500 text-neutral-400 font-medium">Done</span>
              </span>
              <span className="flex flex-col items-center gap-0.5">
                <span className="text-sm font-bold text-blue-400">{counts.inProgress}</span>
                <span className="text-[10px] dark:text-neutral-500 text-neutral-400 font-medium">Active</span>
              </span>
              <span className="flex flex-col items-center gap-0.5">
                <span className="text-sm font-bold text-amber-400">{counts.pending}</span>
                <span className="text-[10px] dark:text-neutral-500 text-neutral-400 font-medium">Pending</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ── Filters ───────────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter size={13} className="dark:text-neutral-400 text-neutral-500 shrink-0" />
          <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider">TYPE:</span>
          <div className="flex gap-1.5 flex-wrap">
            {TYPE_FILTERS.map(f => (
              <button key={f} onClick={() => setTypeFilter(f)}
                className={cn(
                  'px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border',
                  typeFilter === f
                    ? 'bg-brand-500/10 text-brand-500 border-brand-500/30'
                    : 'dark:text-neutral-400 text-neutral-600 dark:border-surface-border border-lsurface-border dark:hover:bg-surface-hover hover:bg-lsurface-hover',
                )}>
                {f}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider">STATUS:</span>
          <div className="flex gap-1.5 flex-wrap">
            {STATUS_FILTERS.map(f => {
              const cfg = STATUS_CONFIG[f]
              return (
                <button key={f} onClick={() => setStatusFilter(f)}
                  className={cn(
                    'px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border',
                    statusFilter === f
                      ? 'bg-brand-500/10 text-brand-500 border-brand-500/30'
                      : 'dark:text-neutral-400 text-neutral-600 dark:border-surface-border border-lsurface-border dark:hover:bg-surface-hover hover:bg-lsurface-hover',
                  )}>
                  {f !== 'All' && cfg.dot && (
                    <span className={cn('inline-block w-1.5 h-1.5 rounded-full mr-1.5 align-middle', cfg.dot.replace('animate-pulse', ''))} />
                  )}
                  {f}
                </button>
              )
            })}
          </div>
        </div>
      </div>

      {/* ── List ──────────────────────────────────────────────────── */}
      {isLoading && (
        <div className="flex justify-center py-24"><Spinner size="lg" /></div>
      )}

      {!isLoading && filtered.length === 0 && (
        <EmptyState
          icon={<History size={40} />}
          title="No sessions found"
          description={
            statusFilter !== 'All' || typeFilter !== 'All'
              ? 'No sessions match the current filters.'
              : 'Start your first interview or coding challenge to build your history.'
          }
          className="py-20"
        />
      )}

      {!isLoading && filtered.length > 0 && (
        <div className="space-y-2.5">
          {filtered.map((iv, i) => (
            <InterviewRow key={`${iv.type}-${iv.id}`} iv={iv} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
