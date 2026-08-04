import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Brain, Mic, MicOff, Volume2, Clock, CheckCircle2, Award, Tag } from 'lucide-react'
import {
  useStartInterview,
  useCurrentQuestion,
  useSubmitAnswer,
} from '@/hooks'
import { Card, Button, ProgressBar, Spinner, Badge } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'

export const InterviewSessionPage = () => {
  const { interviewId } = useParams<{ interviewId: string }>()
  const navigate = useNavigate()
  const id = Number(interviewId)

  const [started, setStarted] = useState(false)
  const [answer, setAnswer] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [lastFeedback, setLastFeedback] = useState<{
    score: number
    feedback: string
  } | null>(null)
  const [questionCount, setQuestionCount] = useState(0)
  const [totalQuestions, setTotalQuestions] = useState(0)
  const [completed, setCompleted] = useState(false)
  const [timeLeft, setTimeLeft] = useState(180) // 3 minutes per question timer

  const { mutate: startInterview, isPending: starting } = useStartInterview()
  const {
    data: currentQ,
    isLoading: loadingQ,
    refetch: refetchQ,
  } = useCurrentQuestion(id, started && !completed)
  const { mutate: submit, isPending: submitting } = useSubmitAnswer()

  // Start the interview on mount
  useEffect(() => {
    startInterview(id, {
      onSuccess: () => {
        setStarted(true)
        setTotalQuestions(0)
      },
      onError: () => {
        showToast('error', 'Failed to initialize interview session.')
      }
    })
  }, [id])

  useEffect(() => {
    if (currentQ) {
      setTotalQuestions(currentQ.total_questions)
      // backend current_question is already 1-indexed (starts at 1)
      setQuestionCount(Math.min(currentQ.current_question, currentQ.total_questions))
      setTimeLeft(180)
    }
  }, [currentQ])

  // Question countdown timer effect
  useEffect(() => {
    if (!started || completed || loadingQ || !currentQ) return
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          return 0
        }
        return prev - 1
      })
    }, 1000)
    return () => clearInterval(timer)
  }, [started, completed, loadingQ, currentQ])

  const handleSubmit = () => {
    if (!answer.trim()) return
    if (isListening) setIsListening(false)

    submit(
      { interviewId: id, body: { answer } },
      {
        onSuccess: (res) => {
          setAnswer('')
          if (res.score != null && res.feedback) {
            setLastFeedback({ score: res.score, feedback: res.feedback })
          } else {
            setLastFeedback(null)
          }

          if (res.interview_completed) {
            setCompleted(true)
            showToast('success', 'Interview complete! Generating report…')
            setTimeout(() => navigate(`/interview/${id}/report`), 1800)
          } else {
            refetchQ()
          }
        },
        onError: () => {
          showToast('error', 'Failed to submit answer.')
        }
      }
    )
  }

  // Voice Speech Recognition
  const toggleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      showToast('warning', 'Speech recognition is not supported in this browser.')
      return
    }

    if (isListening) {
      setIsListening(false)
      return
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-US'

    recognition.onstart = () => setIsListening(true)
    recognition.onend = () => setIsListening(false)
    recognition.onerror = () => setIsListening(false)
    recognition.onresult = (event: any) => {
      let finalTranscript = ''
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript
        }
      }
      if (finalTranscript) {
        setAnswer((prev) => (prev ? `${prev} ${finalTranscript}` : finalTranscript))
      }
    }

    recognition.start()
  }

  // Read question text aloud
  const readQuestionAloud = () => {
    if (!currentQ?.question || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(currentQ.question)
    utterance.rate = 0.95
    window.speechSynthesis.speak(utterance)
  }

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`
  }

  if (starting || (!started && !completed)) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Spinner size="lg" />
        <p className="text-sm font-medium dark:text-neutral-400 text-neutral-500">Preparing your technical interview...</p>
      </div>
    )
  }

  if (completed) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[65vh] gap-4 text-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="p-5 rounded-3xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 text-emerald-400 border border-emerald-500/30"
        >
          <Award size={48} />
        </motion.div>
        <h2 className="text-2xl font-bold dark:text-neutral-100 text-neutral-900">Technical Interview Completed!</h2>
        <p className="dark:text-neutral-400 text-neutral-500 text-sm max-w-sm">
          Analyzing your responses and generating your comprehensive skill scorecard...
        </p>
        <Spinner size="md" className="mt-2" />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* ── Top Header Bar ────────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shadow-sm">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-brand-500 text-white">
            <Brain size={20} />
          </div>
          <div>
            <h1 className="text-base font-bold dark:text-neutral-100 text-neutral-900">Technical Evaluation Session</h1>
            <p className="text-xs dark:text-neutral-400 text-neutral-500">Question {questionCount} of {totalQuestions || '?'}</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Timer pill */}
          <div className={cn(
            'flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-colors',
            timeLeft < 30
              ? 'bg-red-500/10 border-red-500/30 text-red-400 animate-pulse'
              : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-300 text-neutral-700'
          )}>
            <Clock size={14} />
            <span>Time Left: {formatTimer(timeLeft)}</span>
          </div>

          <Badge variant="primary" size="sm">Live Evaluation</Badge>
        </div>
      </div>

      {totalQuestions > 0 && (
        <ProgressBar
          value={questionCount}
          max={totalQuestions}
          color="primary"
          size="sm"
        />
      )}

      {/* ── Last Question Evaluation Feedback ─────────────────────────── */}
      <AnimatePresence>
        {lastFeedback && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <Card className={cn(
              'border',
              lastFeedback.score >= 70
                ? 'border-emerald-500/30 dark:bg-emerald-500/5 bg-emerald-50'
                : lastFeedback.score >= 50
                  ? 'border-amber-500/30 dark:bg-amber-500/5 bg-amber-50'
                  : 'border-red-500/30 dark:bg-red-500/5 bg-red-50'
            )}>
              <div className="flex items-start gap-3">
                <CheckCircle2
                  size={20}
                  className={
                    lastFeedback.score >= 70
                      ? 'text-emerald-400 mt-0.5 shrink-0'
                      : lastFeedback.score >= 50
                        ? 'text-amber-400 mt-0.5 shrink-0'
                        : 'text-red-400 mt-0.5 shrink-0'
                  }
                />
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-bold dark:text-neutral-100 text-neutral-900">
                      Previous Answer Score:
                    </span>
                    <span className={cn(
                      'text-sm font-bold',
                      lastFeedback.score >= 70 ? 'text-emerald-400' : lastFeedback.score >= 50 ? 'text-amber-400' : 'text-red-400'
                    )}>
                      {lastFeedback.score} / 100
                    </span>
                  </div>
                  <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{lastFeedback.feedback}</p>
                </div>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Current Question Card ─────────────────────────────────────── */}
      <Card className="relative overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        {loadingQ ? (
          <div className="flex flex-col items-center justify-center py-12 gap-3">
            <Spinner size="md" />
            <p className="text-xs dark:text-neutral-400 text-neutral-500">Loading question...</p>
          </div>
        ) : currentQ ? (
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-semibold text-brand-500 uppercase tracking-wider">
                  Question {questionCount} of {totalQuestions}
                </span>
                {currentQ.category && (
                  <Badge variant="default" size="xs">
                    <Tag size={9} className="mr-1" />{currentQ.category}
                  </Badge>
                )}
                {currentQ.difficulty && (
                  <Badge
                    variant={
                      currentQ.difficulty.toLowerCase() === 'easy' ? 'success'
                      : currentQ.difficulty.toLowerCase() === 'hard' ? 'error'
                      : 'warning'
                    }
                    size="xs"
                  >
                    {currentQ.difficulty}
                  </Badge>
                )}
              </div>
              <button
                onClick={readQuestionAloud}
                className="flex items-center gap-1.5 text-xs font-semibold dark:text-neutral-400 text-neutral-500 hover:text-brand-500 transition-colors p-1.5 rounded-lg dark:hover:bg-surface-hover hover:bg-lsurface-hover"
                title="Read question aloud"
              >
                <Volume2 size={15} /> Read Aloud
              </button>
            </div>
            <p className="text-lg font-semibold dark:text-neutral-100 text-neutral-900 leading-relaxed">
              {currentQ.question}
            </p>
          </div>
        ) : null}
      </Card>

      {/* ── Response Card ────────────────────────────────────────────── */}
      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        <div className="flex items-center justify-between mb-3">
          <label className="text-xs font-semibold uppercase tracking-wider dark:text-neutral-300 text-neutral-700 flex items-center gap-2">
            Your Response
            <span className="dark:text-neutral-500 text-neutral-400 font-normal lowercase">(Ctrl+Enter to submit)</span>
          </label>
          {isListening && (
            <span className="text-xs font-semibold text-red-400 flex items-center gap-1 animate-pulse">
              <Mic size={13} /> Recording voice input...
            </span>
          )}
        </div>

        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && e.ctrlKey) handleSubmit()
          }}
          placeholder="Type your response or use the microphone to speak your answer clearly..."
          rows={7}
          className="w-full dark:bg-surface-base bg-lsurface-base border dark:border-surface-border border-lsurface-border focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 rounded-xl px-4 py-3 text-sm dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-500 placeholder:text-neutral-400 resize-none focus:outline-none transition-colors duration-200"
          disabled={submitting}
        />

        <div className="flex items-center justify-between mt-4 pt-3 border-t dark:border-surface-border border-lsurface-border">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={toggleVoiceInput}
              className={cn(
                'flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border',
                isListening
                  ? 'bg-red-500 text-white border-red-400 animate-pulse'
                  : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-300 text-neutral-700 hover:border-brand-500'
              )}
            >
              {isListening ? <MicOff size={14} /> : <Mic size={14} />}
              {isListening ? 'Stop Mic' : 'Voice Input'}
            </button>
            <span className="text-xs dark:text-neutral-500 text-neutral-400 font-medium">
              {answer.length} characters
            </span>
          </div>

          <Button
            onClick={handleSubmit}
            disabled={!answer.trim() || submitting}
            loading={submitting}
            variant="primary"
            size="md"
            icon={!submitting ? <Send size={14} /> : undefined}
          >
            {submitting ? 'Evaluating...' : 'Submit Answer'}
          </Button>
        </div>
      </Card>
    </div>
  )
}
