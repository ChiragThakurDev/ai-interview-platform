import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft, Brain, CheckCircle, XCircle, Lightbulb,
  BarChart2, ChevronDown, ChevronUp, Award, TrendingUp,
  MessageSquare, Loader2, RefreshCw,
} from 'lucide-react'
import { useInterviewReport, useInterviewResults } from '@/hooks'
import { Card, Button, Spinner, ProgressBar, EmptyState, Badge } from '@/components/ui'
import { cn } from '@/utils'

// ── helpers ──────────────────────────────────────────────────────────────────
const scoreColor = (s: number) =>
  s >= 80 ? 'text-emerald-400' : s >= 60 ? 'text-amber-400' : 'text-red-400'

const scoreBorder = (s: number) =>
  s >= 80
    ? 'border-emerald-500/30 dark:bg-emerald-500/5 bg-emerald-50/60'
    : s >= 60
      ? 'border-amber-500/30 dark:bg-amber-500/5 bg-amber-50/60'
      : 'border-red-500/30 dark:bg-red-500/5 bg-red-50/60'

const scoreBarColor = (s: number): 'green' | 'yellow' | 'red' =>
  s >= 80 ? 'green' : s >= 60 ? 'yellow' : 'red'

// ── Score ring ────────────────────────────────────────────────────────────────
const ScoreRing = ({ score }: { score: number }) => {
  const c = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : '#ef4444'
  const r = 42
  const circ = 2 * Math.PI * r
  const dash = (score / 100) * circ

  return (
    <div className="relative flex items-center justify-center shrink-0">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={r} fill="none" stroke="currentColor"
          className="dark:text-surface-border text-neutral-200" strokeWidth="9" />
        <circle cx="55" cy="55" r={r} fill="none" stroke={c} strokeWidth="9"
          strokeDasharray={`${dash} ${circ}`} strokeDashoffset={circ / 4}
          strokeLinecap="round" className="transition-all duration-1000 ease-out" />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-2xl font-black dark:text-neutral-100 text-neutral-900 leading-none">{score}</span>
        <span className="text-[10px] font-semibold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider mt-0.5">/ 100</span>
      </div>
    </div>
  )
}

// ── Question row (expandable) ─────────────────────────────────────────────────
const QuestionRow = ({
  idx, question, category, difficulty, answer, score, feedback,
}: {
  idx: number
  question: string
  category: string
  difficulty: string
  answer: string | null
  score: number | null
  feedback: string | null
}) => {
  const [open, setOpen] = useState(false)
  const s = score ?? 0

  return (
    <Card
      onClick={() => setOpen(v => !v)}
      className={cn(
        'cursor-pointer border transition-all',
        open
          ? 'dark:border-brand-500/30 border-brand-500/20 dark:bg-surface-raised bg-brand-50/20'
          : 'dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card hover:dark:border-brand-500/20 hover:border-brand-500/15'
      )}
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <span className="w-7 h-7 rounded-xl dark:bg-surface-raised bg-neutral-100 flex items-center justify-center text-xs font-bold text-brand-500 shrink-0">
            {idx + 1}
          </span>
          <div className="min-w-0">
            <p className="text-xs sm:text-sm font-semibold dark:text-neutral-200 text-neutral-800 truncate">{question}</p>
            <div className="flex items-center gap-1.5 mt-1 flex-wrap">
              {category && (
                <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-md dark:bg-surface-raised bg-neutral-100 dark:text-neutral-400 text-neutral-500">
                  {category}
                </span>
              )}
              {difficulty && (
                <span className={cn(
                  'text-[10px] font-semibold px-1.5 py-0.5 rounded-md',
                  difficulty.toLowerCase() === 'easy'   ? 'bg-emerald-500/10 text-emerald-400' :
                  difficulty.toLowerCase() === 'hard'   ? 'bg-red-500/10 text-red-400' :
                                                          'bg-amber-500/10 text-amber-400'
                )}>
                  {difficulty}
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {score != null ? (
            <span className={cn('text-xs sm:text-sm font-black tabular-nums', scoreColor(s))}>
              {s}/100
            </span>
          ) : (
            <span className="text-xs dark:text-neutral-500 text-neutral-400">—</span>
          )}
          {open ? <ChevronUp size={15} className="dark:text-neutral-400 text-neutral-500" />
                : <ChevronDown size={15} className="dark:text-neutral-400 text-neutral-500" />}
        </div>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 space-y-3 border-t dark:border-surface-border border-lsurface-border pt-4 overflow-hidden"
            onClick={e => e.stopPropagation()}>
            <div>
              <p className="text-xs font-bold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider mb-1.5">Your Answer</p>
              <p className={cn(
                'text-xs dark:text-neutral-300 text-neutral-700 leading-relaxed font-mono p-3 rounded-xl border',
                'dark:bg-surface-base bg-neutral-50 dark:border-surface-border border-lsurface-border'
              )}>
                {answer || <span className="italic opacity-60">No answer recorded</span>}
              </p>
            </div>
            {feedback && (
              <div>
                <p className="text-xs font-bold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider mb-1.5">AI Feedback</p>
                <p className="text-xs dark:text-neutral-300 text-neutral-700 leading-relaxed">{feedback}</p>
              </div>
            )}
            {score != null && (
              <ProgressBar value={s} max={100} color={scoreBarColor(s)} size="sm" />
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────
export const InterviewReportPage = () => {
  const { interviewId } = useParams<{ interviewId: string }>()
  const id = Number(interviewId)
  const [retryCount, setRetryCount] = useState(0)

  // Fetch both: full AI report + per-question results
  const {
    data: report,
    isLoading: loadingReport,
    isError: reportError,
    refetch: refetchReport,
  } = useInterviewReport(id)

  const { data: results, isLoading: loadingResults } = useInterviewResults(id)

  // Auto-retry up to 5 times every 4 seconds while report is not yet generated
  // (AI generation takes time — backend generates lazily on first GET)
  useEffect(() => {
    if (report || retryCount >= 5) return
    if (loadingReport) return

    const timer = setTimeout(() => {
      setRetryCount(c => c + 1)
      refetchReport()
    }, 4000)

    return () => clearTimeout(timer)
  }, [report, loadingReport, retryCount, refetchReport])

  const isGenerating = !report && (loadingReport || retryCount < 5)
  const loading = loadingReport || loadingResults

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <Spinner size="lg" />
      <p className="dark:text-neutral-400 text-neutral-500 text-sm font-medium">Loading performance report…</p>
    </div>
  )

  if (!report && isGenerating) return (
    <div className="flex flex-col items-center justify-center min-h-[65vh] gap-5 text-center">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        className="p-5 rounded-3xl bg-brand-500/10 border border-brand-500/20 text-brand-400"
      >
        <Brain size={40} />
      </motion.div>
      <div>
        <h2 className="text-xl font-bold dark:text-neutral-100 text-neutral-900 mb-2">
          Generating Your Report
        </h2>
        <p className="dark:text-neutral-400 text-neutral-500 text-sm max-w-sm leading-relaxed">
          AI is analysing your answers and generating a comprehensive performance report.
          This takes 15–30 seconds.
        </p>
      </div>
      <div className="flex items-center gap-2 text-xs dark:text-neutral-500 text-neutral-400">
        <Loader2 size={13} className="animate-spin" />
        Attempt {retryCount + 1} of 5…
      </div>
      <Button variant="secondary" size="sm" icon={<RefreshCw size={13} />}
        onClick={() => { setRetryCount(0); refetchReport() }}>
        Retry Now
      </Button>
    </div>
  )

  if (!report) return (
    <div className="max-w-2xl mx-auto mt-12">
      <EmptyState icon={<Brain size={40} />} title="Report not available"
        description="The report could not be generated. Make sure you completed the interview and answered at least one question."
        action={
          <div className="flex gap-3">
            <Button variant="primary" size="sm" icon={<RefreshCw size={13} />}
              onClick={() => { setRetryCount(0); refetchReport() }}>
              Try Again
            </Button>
            <Link to="/interview"><Button variant="ghost" size="sm">New Interview</Button></Link>
          </div>
        } />
    </div>
  )

  // Normalise strengths/weaknesses — backend returns list[str]
  const strengths: string[] = Array.isArray(report.strengths) ? report.strengths : []
  const weaknesses: string[] = Array.isArray(report.weaknesses) ? report.weaknesses : []
  const questions = results?.questions ?? []
  const interviewInfo = results?.interview
  const averageScore = results?.average_score ?? null
  const totalQuestions = results?.total_questions ?? questions.length

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">

      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="flex items-center gap-3">
          <Link to="/history">
            <Button variant="ghost" size="xs" icon={<ArrowLeft size={14} />}>History</Button>
          </Link>
          <div>
            <h1 className="text-xl sm:text-2xl font-black dark:text-neutral-100 text-neutral-900 tracking-tight">
              Interview Report
            </h1>
            {interviewInfo && (
              <p className="text-xs dark:text-neutral-400 text-neutral-500 mt-0.5 font-semibold">
                {interviewInfo.role} · <span className="capitalize">{interviewInfo.difficulty}</span>
              </p>
            )}
          </div>
        </div>
        <Badge variant="success" size="sm" dot>Evaluation Complete</Badge>
      </div>

      {/* Score overview */}
      <Card className="border dark:border-brand-500/25 border-brand-500/20 dark:bg-surface-card bg-lsurface-card p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row items-center gap-8">
          <ScoreRing score={report.overall_score} />
          <div className="flex-1 space-y-3 text-center sm:text-left">
            <div className="flex flex-wrap items-center gap-3 justify-center sm:justify-start">
              <h2 className="text-lg font-black dark:text-neutral-100 text-neutral-900">
                Overall: <span className={scoreColor(report.overall_score)}>{report.overall_score}/100</span>
              </h2>
              {averageScore != null && (
                <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500">
                  Avg: <span className={scoreColor(Math.round(averageScore))}>{Math.round(averageScore)}</span>
                  {totalQuestions > 0 && <span className="ml-1 dark:text-neutral-500 text-neutral-400">· {totalQuestions} questions</span>}
                </span>
              )}
              {report.technical_level && (
                <Badge variant="primary" size="xs">{report.technical_level}</Badge>
              )}
              {report.communication && (
                <Badge variant="default" size="xs">Comm: {report.communication}</Badge>
              )}
            </div>
            <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{report.summary}</p>
            {report.recommendation && (
              <div className="p-3 rounded-xl border dark:border-amber-500/25 border-amber-200 dark:bg-amber-500/5 bg-amber-50/60">
                <p className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <Lightbulb size={11} /> Recommendation
                </p>
                <p className="text-xs dark:text-neutral-300 text-neutral-700 leading-relaxed">{report.recommendation}</p>
              </div>
            )}
          </div>
        </div>
      </Card>

      {/* Strengths + Weaknesses grid */}
      <div className="grid sm:grid-cols-2 gap-5">
        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider mb-4">
            <CheckCircle size={15} className="text-emerald-400" /> Strengths
          </h2>
          {strengths.length > 0 ? (
            <ul className="space-y-2">
              {strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-2 text-xs font-medium dark:text-neutral-300 text-neutral-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />{s}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs dark:text-neutral-500 text-neutral-400">No strengths recorded.</p>
          )}
        </Card>

        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider mb-4">
            <XCircle size={15} className="text-rose-400" /> Areas to Improve
          </h2>
          {weaknesses.length > 0 ? (
            <ul className="space-y-2">
              {weaknesses.map((w, i) => (
                <li key={i} className="flex items-start gap-2 text-xs font-medium dark:text-neutral-300 text-neutral-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mt-1.5 shrink-0" />{w}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs dark:text-neutral-500 text-neutral-400">No improvement areas recorded.</p>
          )}
        </Card>
      </div>

      {/* Score distribution mini chart */}
      {questions.length > 0 && (
        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5">
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider mb-4">
            <TrendingUp size={14} className="text-brand-500" /> Per-Question Scores
          </h2>
          <div className="flex items-end gap-1.5 h-16">
            {questions.map((q, i) => {
              const s = q.score ?? 0
              const pct = (s / 100) * 100
              const col = s >= 80 ? 'bg-emerald-500' : s >= 60 ? 'bg-amber-500' : 'bg-red-500'
              return (
                <div key={i} title={`Q${i+1}: ${s}/100`}
                  className="flex-1 flex flex-col items-center gap-1 group cursor-default">
                  <span className="text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity dark:text-neutral-300 text-neutral-600">{s}</span>
                  <div className="w-full rounded-t overflow-hidden dark:bg-surface-border bg-neutral-200 flex flex-col-reverse" style={{ height: '40px' }}>
                    <motion.div initial={{ height: 0 }} animate={{ height: `${pct}%` }}
                      transition={{ duration: 0.5, delay: i * 0.04 }}
                      className={cn('w-full rounded-t', col)} />
                  </div>
                  <span className="text-2xs dark:text-neutral-500 text-neutral-400">Q{i+1}</span>
                </div>
              )
            })}
          </div>
        </Card>
      )}

      {/* Question-by-question breakdown */}
      {questions.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider">
            <BarChart2 size={14} className="text-brand-500" />
            Question Breakdown
            <span className="font-normal dark:text-neutral-500 text-neutral-400 ml-1">({questions.length} questions)</span>
          </h2>
          <div className="space-y-3">
            {questions.map((q, i) => (
              <motion.div key={q.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
                <QuestionRow
                  idx={i}
                  question={q.question}
                  category={q.category}
                  difficulty={q.difficulty}
                  answer={q.answer}
                  score={q.score != null ? Math.round(q.score) : null}
                  feedback={q.feedback}
                />
              </motion.div>
            ))}
          </div>
        </section>
      )}

      {/* Inline report from /results (fallback if full report unavailable) */}
      {!questions.length && results?.report && (
        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card space-y-3">
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider">
            <MessageSquare size={14} className="text-brand-500" /> Quick Summary
          </h2>
          {results.report.summary && (
            <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{results.report.summary}</p>
          )}
        </Card>
      )}

      {/* Actions */}
      <div className="flex gap-3 pb-8 flex-wrap">
        <Link to="/interview">
          <Button variant="primary" size="sm" icon={<Brain size={14} />}>New Practice</Button>
        </Link>
        <Link to="/history">
          <Button variant="secondary" size="sm" icon={<BarChart2 size={14} />}>All Reports</Button>
        </Link>
        <Link to="/dashboard">
          <Button variant="ghost" size="sm">Dashboard</Button>
        </Link>
      </div>
    </div>
  )
}
