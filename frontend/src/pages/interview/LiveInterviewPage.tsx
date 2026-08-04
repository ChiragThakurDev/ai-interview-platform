import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Brain, Video, ArrowLeft, Loader2 } from 'lucide-react'
import { createInterviewRoom, startInterviewRoom, getLiveKitToken } from '@/api/livekit'
import { LiveInterviewRoom } from '@/components/interview/LiveInterviewRoom'
import { showToast } from '@/components/ui/Toast'
import { Button, Spinner } from '@/components/ui'
import { cn } from '@/utils'
import type { LiveKitConnectionStatus } from '@/types/livekit'

// ── Step label map ────────────────────────────────────────────────────────────
const STATUS_LABELS: Record<LiveKitConnectionStatus, string> = {
  idle:          'Ready to start',
  creating_room: 'Creating interview room…',
  starting_room: 'Starting room…',
  fetching_token: 'Securing your session…',
  connecting:    'Connecting to room…',
  connected:     'Connected',
  disconnected:  'Disconnected',
  error:         'Connection failed',
}

export const LiveInterviewPage = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const interviewId = Number(id)

  const [status, setStatus] = useState<LiveKitConnectionStatus>('idle')
  const [livekitToken, setLivekitToken] = useState<string | null>(null)
  const [livekitUrl, setLivekitUrl] = useState<string | null>(null)
  const [roomName, setRoomName] = useState<string | null>(null)

  // Redirect if id is invalid
  useEffect(() => {
    if (!id || isNaN(interviewId)) {
      showToast.error('Invalid interview ID.')
      navigate('/interview')
    }
  }, [id, interviewId, navigate])

  const initRoom = useCallback(async () => {
    try {
      // 1 — Create room
      setStatus('creating_room')
      const createRes = await createInterviewRoom(interviewId)
      if (!createRes.success) throw new Error('Failed to create interview room.')
      setRoomName(createRes.room.room_name)

      // 2 — Start room
      setStatus('starting_room')
      const startRes = await startInterviewRoom(interviewId)
      if (!startRes.success) throw new Error('Failed to start interview room.')

      // 3 — Get LiveKit token
      setStatus('fetching_token')
      const tokenRes = await getLiveKitToken(interviewId)
      if (!tokenRes.success || !tokenRes.token) throw new Error('Failed to obtain session token.')

      setLivekitToken(tokenRes.token)
      setLivekitUrl(tokenRes.url)
      setStatus('connecting')
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Unexpected error during setup.'
      showToast.error(message)
      setStatus('error')
    }
  }, [interviewId])

  const handleLeave = useCallback(() => {
    setStatus('disconnected')
    setLivekitToken(null)
    setLivekitUrl(null)
    navigate(`/interview/${interviewId}/report`)
  }, [navigate, interviewId])

  const isLoading = ['creating_room', 'starting_room', 'fetching_token', 'connecting'].includes(status)
  const isReady   = status === 'connecting' && !!livekitToken && !!livekitUrl

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] max-h-[calc(100vh-64px)]">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between px-4 py-3 border-b dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(`/interview/${interviewId}/session`)}
            className="p-1.5 rounded-lg dark:text-neutral-400 text-neutral-500 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors"
            aria-label="Back to interview session"
          >
            <ArrowLeft size={16} />
          </button>
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-brand-500 text-white">
              <Brain size={16} />
            </div>
            <div>
              <h1 className="text-sm font-bold dark:text-neutral-100 text-neutral-900 leading-tight">
                Live Video Interview
              </h1>
              {roomName && (
                <p className="text-[11px] dark:text-neutral-500 text-neutral-400 font-mono">
                  {roomName}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Status pill */}
        <div className={cn(
          'flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold border',
          status === 'connecting' || status === 'connected'
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
            : status === 'error' || status === 'disconnected'
              ? 'bg-red-500/10 border-red-500/30 text-red-400'
              : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-400 text-neutral-500'
        )}>
          {isLoading && <Loader2 size={10} className="animate-spin" />}
          {(status === 'connecting' || status === 'connected') && (
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          )}
          {STATUS_LABELS[status]}
        </div>
      </div>

      {/* ── Body ───────────────────────────────────────────────────────── */}
      <div className="flex-1 min-h-0 p-4">

        {/* Idle — prompt user to begin */}
        {status === 'idle' && (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full gap-6 text-center"
          >
            <div className="p-6 rounded-3xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
              <Video size={52} />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-bold dark:text-neutral-100 text-neutral-900">
                Start Your Video Interview
              </h2>
              <p className="text-sm dark:text-neutral-400 text-neutral-500 max-w-sm">
                Make sure your camera and microphone are working before joining.
                The session will be recorded for evaluation.
              </p>
            </div>
            <Button
              variant="primary"
              size="lg"
              onClick={initRoom}
              icon={<Video size={16} />}
            >
              Join Interview Room
            </Button>
          </motion.div>
        )}

        {/* Loading steps */}
        {isLoading && !isReady && (
          <div className="flex flex-col items-center justify-center h-full gap-5">
            <Spinner size="lg" />
            <div className="text-center space-y-1">
              <p className="text-sm font-semibold dark:text-neutral-200 text-neutral-800">
                {STATUS_LABELS[status]}
              </p>
              <p className="text-xs dark:text-neutral-500 text-neutral-400">
                This may take a few seconds…
              </p>
            </div>
            {/* Progress steps */}
            <div className="flex items-center gap-2 mt-2">
              {(['creating_room', 'starting_room', 'fetching_token', 'connecting'] as const).map(
                (step, i) => {
                  const steps: LiveKitConnectionStatus[] = ['creating_room', 'starting_room', 'fetching_token', 'connecting']
                  const currentIdx = steps.indexOf(status)
                  const isDone = i < currentIdx
                  const isActive = i === currentIdx
                  return (
                    <div key={step} className="flex items-center gap-2">
                      <div className={cn(
                        'w-2 h-2 rounded-full transition-all duration-300',
                        isActive  ? 'bg-brand-500 scale-125' :
                        isDone    ? 'bg-emerald-400' :
                                    'dark:bg-surface-border bg-lsurface-border'
                      )} />
                      {i < 3 && (
                        <div className={cn(
                          'w-6 h-px',
                          isDone ? 'bg-emerald-400' : 'dark:bg-surface-border bg-lsurface-border'
                        )} />
                      )}
                    </div>
                  )
                }
              )}
            </div>
          </div>
        )}

        {/* LiveKit room — rendered once token is ready */}
        {isReady && livekitToken && livekitUrl && (
          <LiveInterviewRoom
            token={livekitToken}
            serverUrl={livekitUrl}
            interviewId={interviewId}
            onLeave={handleLeave}
          />
        )}

        {/* Error state */}
        {status === 'error' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center h-full gap-5 text-center"
          >
            <div className="p-5 rounded-3xl bg-red-500/10 text-red-400 border border-red-500/20">
              <Video size={40} />
            </div>
            <div className="space-y-1">
              <h2 className="text-lg font-bold dark:text-neutral-100 text-neutral-900">
                Could Not Connect
              </h2>
              <p className="text-sm dark:text-neutral-400 text-neutral-500 max-w-xs">
                Please check your internet connection and try again.
              </p>
            </div>
            <Button variant="primary" size="md" onClick={initRoom}>
              Retry
            </Button>
          </motion.div>
        )}

        {/* Disconnected state */}
        {status === 'disconnected' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center h-full gap-5 text-center"
          >
            <p className="text-sm dark:text-neutral-400 text-neutral-500">
              You have left the interview room.
            </p>
            <Button
              variant="secondary"
              size="md"
              onClick={() => navigate(`/interview/${interviewId}/report`)}
            >
              View Report
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  )
}
