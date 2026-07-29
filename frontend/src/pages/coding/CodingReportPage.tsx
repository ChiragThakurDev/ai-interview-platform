import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowLeft,
  Code2,
  CheckCircle,
  XCircle,
  Trophy,
} from 'lucide-react'
import { useCodingReportData, useCodingInterview } from '@/hooks'
import { Card, Button, Spinner, EmptyState, Badge } from '@/components/ui'
import { scoreColor, difficultyColor } from '@/utils'

const ScoreRing = ({ score }: { score: number }) => {
  const color = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : '#ef4444'
  const r = 42
  const circ = 2 * Math.PI * r
  const dash = (score / 100) * circ

  return (
    <div className="relative flex items-center justify-center shrink-0">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={r} fill="none" stroke="#1e2238" strokeWidth="9" />
        <circle
          cx="55" cy="55" r={r} fill="none"
          stroke={color} strokeWidth="9"
          strokeDasharray={`${dash} ${circ}`}
          strokeDashoffset={circ / 4}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-2xl font-bold dark:text-neutral-100 text-neutral-900 leading-none">{score}</span>
        <span className="text-[10px] font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mt-0.5">/ 100</span>
      </div>
    </div>
  )
}

export const CodingReportPage = () => {
  const { interviewId } = useParams<{ interviewId: string }>()
  const id = Number(interviewId)
  const { data: report, isLoading } = useCodingReportData(id)
  const { data: interview } = useCodingInterview(id)

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Spinner size="lg" />
        <p className="dark:text-neutral-400 text-neutral-500 text-sm font-medium">Computing coding performance metrics…</p>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="max-w-2xl mx-auto mt-12">
        <EmptyState
          icon={<Code2 size={40} />}
          title="Report pending"
          description="Complete the coding challenges to generate your performance evaluation."
          action={
            <Link to="/coding">
              <Button>Start New Coding Arena</Button>
            </Link>
          }
        />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link to="/history">
            <Button variant="ghost" size="xs" icon={<ArrowLeft size={14} />}>
              History
            </Button>
          </Link>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
              Coding Arena Performance Evaluation
            </h1>
            {interview && (
              <p className="dark:text-neutral-400 text-neutral-500 text-xs mt-0.5 font-semibold">
                {interview.role}
                {interview.company ? ` · ${interview.company}` : ''}
                {' · '}
                <span className={`${difficultyColor(interview.difficulty)} px-2 py-0.5 rounded-full text-[10px] uppercase font-semibold`}>
                  {interview.difficulty}
                </span>
              </p>
            )}
          </div>
        </div>
        <Badge variant="purple" size="sm" dot>IDE Certified</Badge>
      </div>

      {/* Score overview Card */}
      <Card className="border dark:border-amber-500/30 border-amber-200 dark:bg-surface-card bg-lsurface-card shadow-sm p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row items-center gap-8">
          <ScoreRing score={report.overall_score} />
          <div className="flex-1 space-y-2 text-center sm:text-left">
            <div className="flex items-center justify-center sm:justify-start gap-3 flex-wrap">
              <h2 className="text-lg font-bold dark:text-neutral-100 text-neutral-900">
                Score: <span className={scoreColor(report.overall_score)}>{report.overall_score}%</span>
              </h2>
              <Badge
                variant={
                  report.technical_level?.toLowerCase().includes('senior') ? 'success' :
                  report.technical_level?.toLowerCase().includes('junior') ? 'warning' : 'info'
                }
              >
                {report.technical_level}
              </Badge>
            </div>
            <p className="text-xs sm:text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed font-medium">
              {report.summary}
            </p>
          </div>
        </div>
      </Card>

      {/* Recommendation Banner */}
      {report.recommendation && (
        <Card className="border dark:border-brand-500/30 border-brand-500/20 dark:bg-brand-500/5 bg-brand-500/5">
          <div className="flex items-start gap-3">
            <Trophy size={20} className="text-brand-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider mb-1">Recommendation</p>
              <p className="text-xs sm:text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{report.recommendation}</p>
            </div>
          </div>
        </Card>
      )}

      <div className="grid sm:grid-cols-2 gap-6">
        {/* Strengths */}
        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
          <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider mb-4">
            <CheckCircle size={16} className="text-emerald-400" /> Coding Strengths
          </h2>
          {report.strengths?.length > 0 ? (
            <ul className="space-y-2.5">
              {report.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-2.5 text-xs font-medium dark:text-neutral-300 text-neutral-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />
                  {s}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs dark:text-neutral-500 text-neutral-400">None recorded.</p>
          )}
        </Card>

        {/* Weaknesses */}
        <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
          <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 flex items-center gap-2 uppercase tracking-wider mb-4">
            <XCircle size={16} className="text-rose-400" /> Complexity & Quality Refinements
          </h2>
          {report.weaknesses?.length > 0 ? (
            <ul className="space-y-2.5">
              {report.weaknesses.map((w, i) => (
                <li key={i} className="flex items-start gap-2.5 text-xs font-medium dark:text-neutral-300 text-neutral-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mt-1.5 shrink-0" />
                  {w}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs dark:text-neutral-500 text-neutral-400">None recorded.</p>
          )}
        </Card>
      </div>

      {/* Actions */}
      <div className="flex gap-3 pb-8 flex-wrap">
        <Link to="/coding">
          <Button variant="primary" size="sm" icon={<Code2 size={14} />}>
            New Coding Challenge
          </Button>
        </Link>
        <Link to="/leaderboard">
          <Button variant="secondary" size="sm" icon={<Trophy size={14} />}>
            View Leaderboard
          </Button>
        </Link>
        <Link to="/history">
          <Button variant="ghost" size="sm">
            Session History
          </Button>
        </Link>
      </div>
    </div>
  )
}
