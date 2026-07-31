import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Editor from '@monaco-editor/react'
import {
  Send, ChevronLeft, ChevronRight, Code2, Terminal,
  CheckCircle2, XCircle, Loader2, Flag, RotateCcw,
  Copy, Check, Zap, Wifi, WifiOff,
} from 'lucide-react'
import {
  useCodingInterview, useCodingQuestions, useSubmitCode,
  useCodingProgress, useFinishCodingInterview, useCodingDraft,
} from '@/hooks'
import { useCodingWebSocket } from '@/hooks/useCodingWebSocket'
import type {
  WsServerPayload, WsInterviewStartedPayload,
  WsSubmissionResultPayload, WsNextQuestionPayload,
  WsInterviewCompletedPayload,
} from '@/hooks/useCodingWebSocket'
import { useThemeStore } from '@/store'
import { Card, Button, ProgressBar, Spinner, Badge, Modal } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'
import type { EvaluationResult, CodingQuestion, WsQuestionPayload } from '@/types'

const LANGUAGE_MAP: Record<string, string> = {
  python: 'python', javascript: 'javascript', typescript: 'typescript',
  java: 'java', cpp: 'cpp', go: 'go', rust: 'rust',
}

// Convert WS question payload to CodingQuestion shape
const wsQToQuestion = (q: WsQuestionPayload): CodingQuestion => ({
  id: q.id, title: q.title, description: q.description,
  difficulty: q.difficulty, starter_code: q.starter_code ?? null,
  function_name: q.function_name ?? null,
})

const diffColor = (d: string) => {
  if (d === 'easy') return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
  if (d === 'hard') return 'text-red-400 bg-red-500/10 border-red-500/20'
  return 'text-amber-400 bg-amber-500/10 border-amber-500/20'
}

const scoreColor = (s: number) =>
  s >= 80 ? 'text-emerald-400' : s >= 60 ? 'text-amber-400' : 'text-red-400'

export const CodingSessionPage = () => {
  const { interviewId } = useParams<{ interviewId: string }>()
  const navigate = useNavigate()
  const id = Number(interviewId)
  const { theme } = useThemeStore()

  // ── REST data ───────────────────────────────────────────────────────────────
  const { data: interview } = useCodingInterview(id)
  const { data: restQuestions, isLoading: loadingQ } = useCodingQuestions(id)
  const { data: progress, refetch: refetchProgress } = useCodingProgress(id)
  const { mutate: submitCodeRest, isPending: submittingRest } = useSubmitCode()
  const { mutate: finishInterview, isPending: finishing } = useFinishCodingInterview()

  // ── UI state ────────────────────────────────────────────────────────────────
  const [currentIndex, setCurrentIndex] = useState(0)
  const [code, setCode] = useState('')
  const [lastEval, setLastEval] = useState<EvaluationResult | null>(null)
  const [output, setOutput] = useState('')
  const [activeTab, setActiveTab] = useState<'description' | 'evaluation'>('description')
  const [showFinishModal, setShowFinishModal] = useState(false)
  const [copied, setCopied] = useState(false)
  const [wsSubmitting, setWsSubmitting] = useState(false)
  const [totalQ, setTotalQ] = useState(0)
  // When WS pushes a new question we override the REST list entry at currentIndex
  const [wsCurrentQ, setWsCurrentQ] = useState<CodingQuestion | null>(null)

  const autosaveTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const language = interview?.language ?? 'python'
  const monacoLang = LANGUAGE_MAP[language] ?? 'python'

  // Use WS-pushed question if available, otherwise fall back to REST list
  const questions = restQuestions ?? []
  const currentQuestion: CodingQuestion | undefined = wsCurrentQ ?? questions[currentIndex]

  // Load draft / starter code when question changes
  const { data: draft } = useCodingDraft(
    currentQuestion?.id ?? 0,
    !!currentQuestion?.id,
  )
  useEffect(() => {
    if (draft?.code) setCode(draft.code)
    else if (currentQuestion?.starter_code) setCode(currentQuestion.starter_code)
    else setCode(`# Write your ${language} solution here\n`)
    setLastEval(null)
    setOutput('')
    setActiveTab('description')
    setWsCurrentQ(null)
  }, [currentIndex, currentQuestion?.id]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── WebSocket message handler ───────────────────────────────────────────────
  const handleWsMessage = useCallback((msg: WsServerPayload) => {
    switch (msg.type) {
      case 'interview_started': {
        const p = msg as WsInterviewStartedPayload
        setTotalQ(p.total_questions)
        setWsCurrentQ(wsQToQuestion(p.question))
        setCode(p.question.starter_code ?? `# Write your ${language} solution here\n`)
        setActiveTab('description')
        showToast.info('Interview started — good luck!')
        break
      }
      case 'submission_result': {
        const p = msg as WsSubmissionResultPayload
        setWsSubmitting(false)
        setLastEval(p.evaluation)
        setOutput(p.evaluation.passed
          ? '✅ All test cases passed!'
          : `❌ Score: ${p.evaluation.score}/100 — see evaluation tab`)
        setActiveTab('evaluation')
        showToast(p.evaluation.passed ? 'success' : 'info',
          p.evaluation.passed ? `Passed! Score: ${p.evaluation.score}/100` : `Score: ${p.evaluation.score}/100`)
        refetchProgress()
        break
      }
      case 'next_question': {
        const p = msg as WsNextQuestionPayload
        setWsCurrentQ(wsQToQuestion(p.question))
        setCode(p.question.starter_code ?? `# Write your ${language} solution here\n`)
        setLastEval(null); setOutput(''); setActiveTab('description')
        setCurrentIndex(i => i + 1)
        break
      }
      case 'interview_completed': {
        const p = msg as WsInterviewCompletedPayload
        showToast.success(`Interview complete! Final score: ${p.score}`)
        setTimeout(() => navigate(`/coding/${id}/report`), 1500)
        break
      }
      case 'draft_saved':
        // silent autosave confirmation
        break
      case 'error':
        setWsSubmitting(false)
        showToast.error((msg as { type: 'error'; message: string }).message ?? 'WebSocket error')
        break
    }
  }, [id, language, navigate, refetchProgress])

  const sendRef = useRef<ReturnType<typeof useCodingWebSocket>['send'] | null>(null)

  const { status: wsStatus, send } = useCodingWebSocket({
    interviewId: id,
    onMessage: handleWsMessage,
    onClose: () => setWsSubmitting(false),
    onError: () => {
      setWsSubmitting(false)
      showToast.warning('Real-time connection failed — using REST fallback')
    },
  })

  // Keep sendRef fresh so effects always have the latest send fn
  useEffect(() => { sendRef.current = send }, [send])

  // Fire start_interview as soon as WebSocket is truly open
  useEffect(() => {
    if (wsStatus === 'connected') {
      sendRef.current?.('start_interview')
    }
  }, [wsStatus])

  const isWsConnected = wsStatus === 'connected'
  const submitting = wsSubmitting || submittingRest

  // ── Autosave via WS ─────────────────────────────────────────────────────────
  useEffect(() => {
    if (!currentQuestion || !isWsConnected) return
    if (autosaveTimer.current) clearTimeout(autosaveTimer.current)
    autosaveTimer.current = setTimeout(() => {
      send('autosave', {
        question_id: currentQuestion.id,
        language,
        code,
      })
    }, 2000)
    return () => { if (autosaveTimer.current) clearTimeout(autosaveTimer.current) }
  }, [code]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Submit handler — tries WS first, falls back to REST ────────────────────
  const handleSubmit = useCallback(() => {
    if (!currentQuestion || !code.trim()) return

    if (isWsConnected) {
      setWsSubmitting(true)
      const sent = send('submit_code', {
        question_id: currentQuestion.id,
        language,
        code,
      })
      if (!sent) { setWsSubmitting(false) }
      return
    }

    // REST fallback
    submitCodeRest(
      { interview_id: id, question_id: currentQuestion.id, language, code },
      {
        onSuccess: (result) => {
          setLastEval(result.evaluation)
          setOutput(result.evaluation.passed ? '✅ All test cases passed!' : `❌ Score: ${result.evaluation.score}/100`)
          setActiveTab('evaluation')
          if (result.completed) setTimeout(() => navigate(`/coding/${id}/report`), 1500)
        },
        onError: () => showToast.error('Code submission failed'),
      },
    )
  }, [currentQuestion, code, id, language, isWsConnected, send, submitCodeRest, navigate])

  const handleFinish = () => {
    finishInterview(id, {
      onSuccess: () => navigate(`/coding/${id}/report`),
      onError: () => showToast.error('Could not finish interview'),
    })
  }

  const copyCode = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const resetCode = () => {
    if (currentQuestion?.starter_code) setCode(currentQuestion.starter_code)
    else setCode(`# Write your ${language} solution here\n`)
  }

  if (loadingQ) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
      <Spinner size="lg" />
      <p className="text-sm font-medium dark:text-neutral-400 text-neutral-500">Loading coding workspace…</p>
    </div>
  )

  if (!questions.length && !wsCurrentQ) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center gap-2">
      <Code2 size={40} className="dark:text-neutral-500 text-neutral-400" />
      <p className="dark:text-neutral-300 text-neutral-700 font-semibold">No questions found for this session.</p>
    </div>
  )

  const displayProgress = progress ?? {
    answered_questions: 0,
    total_questions: totalQ || questions.length,
    current_score: 0,
    progress_percentage: 0,
    remaining_questions: questions.length,
    interview_id: id,
    status: 'running',
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] gap-3 overflow-hidden">

      {/* ── Top Bar ── */}
      <div className="flex items-center justify-between flex-wrap gap-3 px-4 py-3 rounded-2xl border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-amber-500 text-white"><Code2 size={17} /></div>
          <div>
            <h1 className="text-sm font-bold dark:text-neutral-100 text-neutral-900 leading-tight">Live Coding Arena</h1>
            <p className="text-xs dark:text-neutral-400 text-neutral-500">{interview?.role ?? 'Coding Interview'} · {interview?.company ?? ''}</p>
          </div>
          {interview && <Badge variant="warning" size="sm">{interview.language}</Badge>}
          {/* WS status indicator */}
          <div className={cn('flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-semibold border',
            isWsConnected
              ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
              : 'text-neutral-500 bg-surface-raised border-surface-border')}>
            {isWsConnected ? <Wifi size={11} /> : <WifiOff size={11} />}
            {isWsConnected ? 'Live' : 'REST'}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold dark:text-neutral-400 text-neutral-500">
            {displayProgress.answered_questions}/{displayProgress.total_questions} solved
            {displayProgress.current_score > 0 && ` · ${displayProgress.current_score} pts`}
          </span>
          <Button variant="danger" size="xs" onClick={() => setShowFinishModal(true)} icon={<Flag size={13} />}>
            End Interview
          </Button>
        </div>
      </div>

      {displayProgress.total_questions > 0 && (
        <ProgressBar value={displayProgress.answered_questions} max={displayProgress.total_questions} size="sm" color="yellow" />
      )}

      {/* ── Split workspace ── */}
      <div className="grid lg:grid-cols-2 gap-3 flex-1 min-h-0 overflow-hidden">

        {/* LEFT — question + eval */}
        <div className="flex flex-col gap-3 min-h-0 overflow-hidden">
          {/* Question pills */}
          <div className="flex items-center gap-2 flex-wrap shrink-0">
            {questions.map((q, i) => (
              <button key={q.id} onClick={() => { setCurrentIndex(i); setWsCurrentQ(null) }}
                className={cn('w-8 h-8 rounded-xl text-xs font-bold transition-all border',
                  i === currentIndex
                    ? 'bg-brand-500 border-brand-500 text-white'
                    : 'dark:bg-surface-card bg-lsurface-card dark:border-surface-border border-lsurface-border dark:text-neutral-400 text-neutral-600 hover:border-brand-500')}>
                {i + 1}
              </button>
            ))}
          </div>

          {/* Tabs */}
          <div className="flex gap-1 dark:bg-surface-raised bg-lsurface-raised p-1 rounded-xl w-fit shrink-0">
            {(['description', 'evaluation'] as const).map(tab => (
              <button key={tab} onClick={() => setActiveTab(tab)}
                className={cn('px-3 py-1.5 rounded-lg text-xs font-semibold transition-all capitalize',
                  activeTab === tab
                    ? 'dark:bg-surface-card bg-lsurface-card dark:text-neutral-100 text-neutral-900 shadow-sm'
                    : 'dark:text-neutral-400 text-neutral-600')}>
                {tab}
                {tab === 'evaluation' && lastEval && (
                  <span className={cn('ml-1.5 font-bold', scoreColor(lastEval.score))}>
                    {lastEval.score}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <AnimatePresence mode="wait">
            {activeTab === 'description' && currentQuestion && (
              <motion.div key="desc" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="flex-1 overflow-y-auto min-h-0">
                <Card className="h-full border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <h2 className="font-bold text-base dark:text-neutral-100 text-neutral-900 leading-snug">{currentQuestion.title}</h2>
                    <span className={cn('text-xs px-2.5 py-1 rounded-full font-semibold border shrink-0', diffColor(currentQuestion.difficulty))}>
                      {currentQuestion.difficulty}
                    </span>
                  </div>
                  <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed whitespace-pre-wrap">
                    {currentQuestion.description}
                  </p>
                  {currentQuestion.function_name && (
                    <div className="p-3 rounded-xl dark:bg-surface-base bg-lsurface-base border dark:border-surface-border border-lsurface-border">
                      <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold mb-1">Function signature:</p>
                      <code className="text-sm text-brand-500 font-mono font-bold">{currentQuestion.function_name}</code>
                    </div>
                  )}
                </Card>
              </motion.div>
            )}

            {activeTab === 'evaluation' && (
              <motion.div key="eval" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="flex-1 overflow-y-auto min-h-0">
                {!lastEval ? (
                  <Card className="h-full flex flex-col items-center justify-center text-center p-8 border dark:border-surface-border border-lsurface-border">
                    <Zap size={28} className="dark:text-neutral-500 text-neutral-400 mb-2" />
                    <p className="dark:text-neutral-400 text-neutral-600 text-sm">Submit code to see AI evaluation.</p>
                  </Card>
                ) : (
                  <Card className="space-y-4 border dark:border-surface-border border-lsurface-border">
                    <div className={cn('flex items-center justify-between p-3 rounded-xl border',
                      lastEval.passed ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-400' : 'bg-red-500/10 border-red-500/25 text-red-400')}>
                      <div className="flex items-center gap-2">
                        {lastEval.passed ? <CheckCircle2 size={18} /> : <XCircle size={18} />}
                        <span className="font-semibold text-sm">{lastEval.passed ? 'All tests passed!' : 'Tests incomplete'}</span>
                      </div>
                      <span className="font-black text-lg">{lastEval.score}/100</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      {[
                        { label: 'Correctness', value: `${lastEval.correctness}/100`, score: lastEval.correctness },
                        { label: 'Code Quality', value: `${lastEval.code_quality}/100`, score: lastEval.code_quality },
                        { label: 'Time', value: lastEval.time_complexity, score: -1 },
                        { label: 'Space', value: lastEval.space_complexity, score: -1 },
                      ].map(m => (
                        <div key={m.label} className="dark:bg-surface-base bg-lsurface-base rounded-xl p-3 border dark:border-surface-border border-lsurface-border">
                          <p className="dark:text-neutral-400 text-neutral-500 text-xs font-semibold mb-1">{m.label}</p>
                          <p className={cn('font-bold text-sm font-mono', m.score >= 0 ? scoreColor(m.score) : 'text-brand-500')}>{m.value}</p>
                        </div>
                      ))}
                    </div>
                    <div>
                      <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold uppercase tracking-wider mb-1">AI Feedback</p>
                      <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{lastEval.feedback}</p>
                    </div>
                    {lastEval.bugs.length > 0 && (
                      <div>
                        <p className="text-xs text-red-400 font-semibold uppercase tracking-wider mb-2">Bugs Found</p>
                        <ul className="space-y-1">{lastEval.bugs.map((b, i) => (
                          <li key={i} className="text-xs dark:text-neutral-300 text-neutral-700 flex gap-1.5"><span className="text-red-400">•</span>{b}</li>
                        ))}</ul>
                      </div>
                    )}
                    {lastEval.optimization_suggestions.length > 0 && (
                      <div>
                        <p className="text-xs text-amber-400 font-semibold uppercase tracking-wider mb-2">Optimisations</p>
                        <ul className="space-y-1">{lastEval.optimization_suggestions.map((s, i) => (
                          <li key={i} className="text-xs dark:text-neutral-300 text-neutral-700 flex gap-1.5"><span className="text-amber-400">•</span>{s}</li>
                        ))}</ul>
                      </div>
                    )}
                    {lastEval.strengths.length > 0 && (
                      <div>
                        <p className="text-xs text-emerald-400 font-semibold uppercase tracking-wider mb-2">Strengths</p>
                        <ul className="space-y-1">{lastEval.strengths.map((s, i) => (
                          <li key={i} className="text-xs dark:text-neutral-300 text-neutral-700 flex gap-1.5"><span className="text-emerald-400">•</span>{s}</li>
                        ))}</ul>
                      </div>
                    )}
                  </Card>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* RIGHT — Monaco + console */}
        <div className="flex flex-col gap-3 min-h-0 overflow-hidden">
          {/* Editor */}
          <div className="flex-1 rounded-2xl overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-[#1e1e1e] bg-slate-900 flex flex-col min-h-[300px]">
            <div className="px-4 py-2 flex items-center justify-between text-xs dark:bg-[#2d2d2d] bg-slate-800 border-b dark:border-[#3d3d3d] border-slate-700 shrink-0">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
                <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
                <span className="w-2.5 h-2.5 rounded-full bg-green-500/70" />
                <span className="text-slate-300 font-mono font-semibold ml-2">{language}</span>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={resetCode} className="flex items-center gap-1 text-slate-400 hover:text-white transition-colors">
                  <RotateCcw size={12} /> Reset
                </button>
                <button onClick={copyCode} className="flex items-center gap-1 text-slate-400 hover:text-white transition-colors">
                  {copied ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                  {copied ? 'Copied' : 'Copy'}
                </button>
              </div>
            </div>
            <div className="flex-1 min-h-0">
              <Editor
                height="100%"
                language={monacoLang}
                value={code}
                onChange={val => setCode(val ?? '')}
                theme={theme === 'dark' ? 'vs-dark' : 'light'}
                options={{
                  fontSize: 14, minimap: { enabled: false }, scrollBeyondLastLine: false,
                  wordWrap: 'on', tabSize: 2, lineNumbers: 'on', renderLineHighlight: 'all',
                  smoothScrolling: true, cursorBlinking: 'smooth',
                  fontFamily: 'JetBrains Mono, Fira Code, monospace',
                }}
              />
            </div>
          </div>

          {/* Console */}
          <Card className="dark:bg-[#1a1a1a] bg-slate-900 border dark:border-[#2d2d2d] border-slate-700 shrink-0 px-4 py-3">
            <div className="flex items-center gap-2 mb-1.5">
              <Terminal size={13} className="text-brand-500" />
              <span className="text-xs font-bold dark:text-neutral-400 text-slate-400 uppercase tracking-wider">Console</span>
              {isWsConnected && <span className="ml-auto text-xs dark:text-neutral-600 text-slate-500">autosave on</span>}
            </div>
            {submitting ? (
              <div className="flex items-center gap-2 text-brand-500 text-xs font-semibold">
                <Loader2 size={13} className="animate-spin" /> Executing in sandbox…
              </div>
            ) : output ? (
              <p className="text-xs font-mono dark:text-neutral-200 text-slate-200 whitespace-pre-wrap">{output}</p>
            ) : (
              <p className="text-xs dark:text-neutral-600 text-slate-500 font-mono">Ready.</p>
            )}
          </Card>

          {/* Actions */}
          <div className="flex items-center justify-between shrink-0 gap-2">
            <div className="flex gap-2">
              <Button variant="secondary" size="xs" disabled={currentIndex === 0}
                onClick={() => { setCurrentIndex(i => i - 1); setWsCurrentQ(null) }}
                icon={<ChevronLeft size={13} />}>Prev</Button>
              <Button variant="secondary" size="xs" disabled={currentIndex >= questions.length - 1}
                onClick={() => { setCurrentIndex(i => i + 1); setWsCurrentQ(null) }}>
                Next <ChevronRight size={13} />
              </Button>
            </div>
            <Button onClick={handleSubmit} loading={submitting} disabled={!code.trim() || submitting}
              variant="primary" size="md" icon={!submitting ? <Send size={14} /> : undefined}>
              {submitting ? 'Executing…' : 'Run & Submit'}
            </Button>
          </div>
        </div>
      </div>

      {/* Finish modal */}
      <Modal open={showFinishModal} onClose={() => setShowFinishModal(false)} title="Finish Coding Interview?">
        <p className="dark:text-neutral-300 text-neutral-600 text-sm mb-6 leading-relaxed">
          You've solved {displayProgress.answered_questions} of {displayProgress.total_questions} questions.
          Finishing will lock your submissions and generate your performance report.
        </p>
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={() => setShowFinishModal(false)}>Keep Coding</Button>
          <Button variant="primary" loading={finishing} onClick={handleFinish}>Finish & View Report</Button>
        </div>
      </Modal>
    </div>
  )
}
