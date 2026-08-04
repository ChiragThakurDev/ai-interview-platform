import { useEffect, useCallback, useState, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LiveKitRoom, RoomAudioRenderer, useRoomContext,
  useTracks, VideoTrack,
} from '@livekit/components-react'
import '@livekit/components-styles'
import { Track, RoomEvent, DataPacket_Kind, createLocalScreenTracks } from 'livekit-client'
import type { Participant } from 'livekit-client'
import {
  Mic, MicOff, Video as VideoIcon, VideoOff, PhoneOff,
  Copy, Check, Wifi, WifiOff, Users, User, Link2, Hash,
  Monitor, MonitorOff, MessageSquare, Send, X, Brain,
  AlertTriangle, UserCheck, UsersRound, Globe, Lock, Clock,
} from 'lucide-react'
import { useVideoRoom } from '@/hooks/useVideoRoom'
import { useRoomRegistry, EMPTY_TIMEOUT_MS } from '@/hooks/useRoomRegistry'
import { InterviewTimer } from '@/components/interview/InterviewTimer'
import { Button, Card, Spinner } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { roomTypeFromCode, roomVisibilityFromCode, ROOM_MAX } from '@/types/livekit'
import type { RoomType, RoomVisibility } from '@/types/livekit'
import { cn } from '@/utils'

// ── Data-channel message types ────────────────────────────────────────────────
type DataMsg =
  | { type: 'chat';          text: string }
  | { type: 'screen_req';    from: string }   // requester asks current sharer
  | { type: 'screen_accept' }                 // current sharer accepts handoff
  | { type: 'screen_deny' }                   // current sharer denies

// ── Chat message ──────────────────────────────────────────────────────────────
interface ChatMsg { id: string; sender: string; text: string; self: boolean; ts: number }

// ── Reusable control button ───────────────────────────────────────────────────
interface CtrlBtnProps {
  onClick: () => void; active?: boolean; danger?: boolean
  icon: React.ReactNode; offIcon?: React.ReactNode
  label: string; badge?: number; disabled?: boolean
}
const CtrlBtn = ({ onClick, active = true, danger, icon, offIcon, label, badge, disabled }: CtrlBtnProps) => (
  <button onClick={onClick} disabled={disabled} title={label}
    className={cn(
      'relative flex flex-col items-center gap-1 px-3 py-2.5 rounded-xl transition-all duration-150',
      'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500',
      'disabled:opacity-40 disabled:cursor-not-allowed',
      danger
        ? 'bg-red-600 hover:bg-red-500 text-white'
        : active
          ? 'dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-200 text-neutral-700 dark:hover:bg-surface-hover hover:bg-lsurface-hover dark:border-surface-border border-lsurface-border border'
          : 'bg-red-500/15 text-red-400 hover:bg-red-500/25 border border-red-500/30',
    )}>
    {active ? icon : (offIcon ?? icon)}
    <span className="text-[10px] font-semibold leading-none">{label}</span>
    {badge != null && badge > 0 && (
      <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-brand-500 text-white text-[9px] font-bold flex items-center justify-center">
        {badge > 9 ? '9+' : badge}
      </span>
    )}
  </button>
)

// ── Generic confirmation modal ────────────────────────────────────────────────
interface ConfirmModalProps {
  open: boolean
  icon: React.ReactNode
  title: string
  body: string
  confirmLabel: string
  cancelLabel?: string
  onConfirm: () => void
  onCancel: () => void
  confirmVariant?: 'primary' | 'danger'
  autoCloseMs?: number
}
const ConfirmModal = ({
  open, icon, title, body, confirmLabel, cancelLabel = 'Dismiss',
  onConfirm, onCancel, confirmVariant = 'primary', autoCloseMs,
}: ConfirmModalProps) => {
  useEffect(() => {
    if (!open || !autoCloseMs) return
    const t = setTimeout(onCancel, autoCloseMs)
    return () => clearTimeout(t)
  }, [open, autoCloseMs, onCancel])

  return (
    <AnimatePresence>
      {open && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.92, y: 16 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.92, y: 8 }}
            className="w-full max-w-sm dark:bg-surface-card bg-white rounded-2xl border dark:border-surface-border border-lsurface-border shadow-xl p-6 space-y-4">
            <div className="flex flex-col items-center gap-3 text-center">
              <div className="p-3 rounded-2xl dark:bg-surface-raised bg-lsurface-raised">{icon}</div>
              <h3 className="text-base font-bold dark:text-neutral-100 text-neutral-900">{title}</h3>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 leading-relaxed">{body}</p>
            </div>
            <div className="flex gap-2 pt-2">
              <Button variant="secondary" size="md" className="flex-1" onClick={onCancel}>{cancelLabel}</Button>
              <Button variant={confirmVariant} size="md" className="flex-1" onClick={onConfirm}>{confirmLabel}</Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// ── SessionContent (must live inside <LiveKitRoom>) ───────────────────────────
interface SessionContentProps {
  roomCode: string; roomType: RoomType; maxParticipants: number
  inviteLink: string; onLeave: () => void; onCopyLink: () => void; copied: boolean
  visibility: RoomVisibility; isHost: boolean
}

const SessionContent = ({
  roomCode, roomType, maxParticipants, inviteLink, onLeave, onCopyLink, copied,
  visibility, isHost,
}: SessionContentProps) => {
  const room = useRoomContext()
  const { updateCount, removeRoom } = useRoomRegistry()
  const isPublic = visibility === 'public'

  // ── media ──────────────────────────────────────────────────────────────────
  const [mic,     setMic]     = useState(true)
  const [cam,     setCam]     = useState(true)
  const [sharing, setSharing] = useState(false)

  // ── UI ─────────────────────────────────────────────────────────────────────
  const [connected,        setConnected]        = useState(false)
  const [participantCount, setParticipantCount] = useState(1)
  const [showInfo,         setShowInfo]         = useState(false)
  const [chatOpen,         setChatOpen]         = useState(false)
  const [unread,           setUnread]           = useState(0)

  // ── empty-room timeout countdown (seconds remaining) ──────────────────────
  // Only the host tracks this; guests see nothing.
  const TIMEOUT_SECS = EMPTY_TIMEOUT_MS / 1000  // 900 s = 15 min
  const [emptyCountdown, setEmptyCountdown] = useState<number | null>(null)
  const emptyTimerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startEmptyTimer = useCallback(() => {
    if (!isHost || !isPublic) return
    setEmptyCountdown(TIMEOUT_SECS)
    emptyTimerRef.current = setInterval(() => {
      setEmptyCountdown(prev => {
        if (prev === null) return null
        if (prev <= 1) return 0
        return prev - 1
      })
    }, 1000)
  }, [isHost, isPublic, TIMEOUT_SECS])

  const stopEmptyTimer = useCallback(() => {
    if (emptyTimerRef.current) { clearInterval(emptyTimerRef.current); emptyTimerRef.current = null }
    setEmptyCountdown(null)
  }, [])

  // Auto-close when countdown hits 0
  useEffect(() => {
    if (emptyCountdown === 0) {
      stopEmptyTimer()
      if (isPublic) removeRoom(roomCode)
      showToast.info('Room closed — no participants joined within 15 minutes.')
      room.disconnect().then(onLeave)
    }
  }, [emptyCountdown, stopEmptyTimer, isPublic, removeRoom, roomCode, room, onLeave])

  // ── chat ───────────────────────────────────────────────────────────────────
  const [messages,  setMessages]  = useState<ChatMsg[]>([])
  const [chatInput, setChatInput] = useState('')
  const chatBottomRef             = useRef<HTMLDivElement>(null)

  // ── screen-share handoff modals ────────────────────────────────────────────
  const [shareReqModal,     setShareReqModal]     = useState(false)
  const [shareRequester,    setShareRequester]    = useState('')
  const [sharePendingModal, setSharePendingModal] = useState(false)

  // ── video tracks ───────────────────────────────────────────────────────────
  const allCamTracks = useTracks(
    [{ source: Track.Source.Camera, withPlaceholder: true }],
    { onlySubscribed: false },
  )
  const screenTracks = useTracks(
    [{ source: Track.Source.ScreenShare, withPlaceholder: false }],
    { onlySubscribed: false },
  )
  const localCam     = allCamTracks.find(t => t.participant.isLocal)
  const remoteCams   = allCamTracks.filter(t => !t.participant.isLocal)
  const activeScreen = screenTracks[0] ?? null
  const isGroup      = roomType === 'group'

  // ── send helper ────────────────────────────────────────────────────────────
  const sendData = useCallback(async (msg: DataMsg, to?: Participant) => {
    const payload = new TextEncoder().encode(JSON.stringify(msg))
    await room.localParticipant.publishData(payload, {
      reliable: true,
      kind: DataPacket_Kind.RELIABLE,
      ...(to ? { destinationIdentities: [to.identity] } : {}),
    })
  }, [room])

  // ── room events ────────────────────────────────────────────────────────────
  useEffect(() => {
    const syncCount = () => {
      const count = room.numParticipants
      setParticipantCount(count)
      if (isPublic) updateCount(roomCode, 0 as unknown as 1) // force-set via dedicated path below
      // Only 1 = just the host → start timeout
      if (count <= 1 && isHost && isPublic) {
        startEmptyTimer()
      } else {
        stopEmptyTimer()
      }
    }

    const onConn = () => { setConnected(true); syncCount() }
    const onDisconn = () => setConnected(false)
    const onJoin = (p: Participant) => {
      showToast.success(`${p.name || 'Someone'} joined`)
      const count = room.numParticipants
      setParticipantCount(count)
      stopEmptyTimer()  // someone joined — cancel timeout
      // Update registry count
      if (isPublic && isHost) updateCount(roomCode, 1)
    }
    const onLeaveP = (p: Participant) => {
      const count = room.numParticipants
      setParticipantCount(count)
      if (isPublic && isHost) updateCount(roomCode, -1)
      if (count <= 1 && isHost && isPublic) startEmptyTimer()
    }

    room.on(RoomEvent.Connected,               onConn)
    room.on(RoomEvent.Disconnected,            onDisconn)
    room.on(RoomEvent.ParticipantConnected,    onJoin)
    room.on(RoomEvent.ParticipantDisconnected, onLeaveP)

    return () => {
      room.off(RoomEvent.Connected,               onConn)
      room.off(RoomEvent.Disconnected,            onDisconn)
      room.off(RoomEvent.ParticipantConnected,    onJoin)
      room.off(RoomEvent.ParticipantDisconnected, onLeaveP)
      stopEmptyTimer()
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [room, isHost, isPublic, roomCode])

  // ── incoming data messages ─────────────────────────────────────────────────
  useEffect(() => {
    const onData = (payload: Uint8Array, participant?: Participant) => {
      let parsed: DataMsg
      try { parsed = JSON.parse(new TextDecoder().decode(payload)) }
      catch { return }

      if (parsed.type === 'chat') {
        setMessages(prev => [...prev, {
          id: `${Date.now()}-${Math.random()}`,
          sender: participant?.name || 'Guest',
          text: parsed.text, self: false, ts: Date.now(),
        }])
        if (!chatOpen) setUnread(u => u + 1)
        return
      }

      // Screen-share handoff — someone is asking us (the current sharer) to yield
      if (parsed.type === 'screen_req' && sharing) {
        setShareRequester(participant?.name || 'Someone')
        setShareReqModal(true)
        return
      }

      // Sharer accepted → we can start sharing now
      if (parsed.type === 'screen_accept') {
        setSharePendingModal(false)
        showToast.info('Screen share handed over — starting your share…')
        startScreenShare()
        return
      }

      // Sharer denied
      if (parsed.type === 'screen_deny') {
        setSharePendingModal(false)
        showToast.warning('Request declined. The other person is still sharing.')
      }
    }
    room.on(RoomEvent.DataReceived, onData)
    return () => { room.off(RoomEvent.DataReceived, onData) }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [room, chatOpen, sharing])

  useEffect(() => { chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])
  useEffect(() => { if (chatOpen) setUnread(0) }, [chatOpen])

  // ── media controls ─────────────────────────────────────────────────────────
  const toggleMic = useCallback(async () => {
    try { await room.localParticipant.setMicrophoneEnabled(!mic); setMic(v => !v) }
    catch { showToast.error('Cannot toggle mic.') }
  }, [room, mic])

  const toggleCam = useCallback(async () => {
    try { await room.localParticipant.setCameraEnabled(!cam); setCam(v => !v) }
    catch { showToast.error('Cannot toggle camera.') }
  }, [room, cam])

  // Inner start — called both directly and after handoff-accept
  const startScreenShare = useCallback(async () => {
    try {
      const tracks = await createLocalScreenTracks({ audio: false })
      if (!tracks.length) return
      const t = tracks[0]
      t.mediaStreamTrack.addEventListener('ended', () => setSharing(false), { once: true })
      await room.localParticipant.publishTrack(t)
      setSharing(true)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message.toLowerCase() : ''
      if (!msg.includes('cancel') && !msg.includes('permission'))
        showToast.error('Could not start screen share.')
    }
  }, [room])

  const stopScreenShare = useCallback(async () => {
    const pub = room.localParticipant.getTrackPublication(Track.Source.ScreenShare)
    if (pub?.track) await room.localParticipant.unpublishTrack(pub.track)
    setSharing(false)
  }, [room])

  const toggleScreen = useCallback(async () => {
    if (sharing) { await stopScreenShare(); return }

    // If someone else is already sharing → send a handoff request
    const remoteSharing = screenTracks.some(t => !t.participant.isLocal)
    if (remoteSharing) {
      const sharer = screenTracks.find(t => !t.participant.isLocal)?.participant
      if (sharer) {
        await sendData({ type: 'screen_req', from: room.localParticipant.name || 'Someone' }, sharer)
        setSharePendingModal(true)
        return
      }
    }

    await startScreenShare()
  }, [room, sharing, screenTracks, sendData, startScreenShare, stopScreenShare])

  // Sharer accepts handoff: stop own share, notify requester
  const acceptShareHandoff = useCallback(async () => {
    setShareReqModal(false)
    await stopScreenShare()
    // Broadcast accept so the requester can start
    await sendData({ type: 'screen_accept' })
  }, [stopScreenShare, sendData])

  const denyShareHandoff = useCallback(async () => {
    setShareReqModal(false)
    await sendData({ type: 'screen_deny' })
  }, [sendData])

  // ── chat send ──────────────────────────────────────────────────────────────
  const sendChatMessage = useCallback(async () => {
    const text = chatInput.trim()
    if (!text) return
    await sendData({ type: 'chat', text })
    setMessages(prev => [...prev, {
      id: `${Date.now()}-self`, sender: room.localParticipant.name || 'You',
      text, self: true, ts: Date.now(),
    }])
    setChatInput('')
  }, [room, chatInput, sendData])

  const handleLeave = useCallback(async () => {
    await room.disconnect(); onLeave()
  }, [room, onLeave])

  const fmt = (ts: number) => {
    const d = new Date(ts)
    return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
  }

  return (
    <div className="flex flex-col h-full dark:bg-surface-base bg-lsurface-base">

      {/* ── Modals ──────────────────────────────────────────────── */}
      {/* Screen-share REQUEST — shown to current sharer */}
      <ConfirmModal
        open={shareReqModal}
        icon={<Monitor size={28} className="text-brand-500" />}
        title="Screen Share Request"
        body={`${shareRequester} wants to share their screen. Do you want to hand over screen share and stop yours?`}
        confirmLabel="Hand Over"
        cancelLabel="Decline"
        confirmVariant="primary"
        autoCloseMs={20000}
        onConfirm={acceptShareHandoff}
        onCancel={denyShareHandoff}
      />

      {/* Screen-share PENDING — shown to requester while waiting */}
      <ConfirmModal
        open={sharePendingModal}
        icon={<Monitor size={28} className="text-brand-500 animate-pulse" />}
        title="Waiting for Response"
        body="Your screen share request has been sent. Waiting for the other person to respond…"
        confirmLabel="Cancel Request"
        cancelLabel=""
        confirmVariant="danger"
        autoCloseMs={25000}
        onConfirm={() => setSharePendingModal(false)}
        onCancel={() => setSharePendingModal(false)}
      />

      {/* ── Top bar ──────────────────────────────────────────────── */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shrink-0">
        <div className="flex items-center gap-3 flex-wrap">
          <div className={cn('flex items-center gap-1.5 text-xs font-semibold',
            connected ? 'text-emerald-400' : 'text-red-400')}>
            {connected ? <><Wifi size={12}/><span>Live</span></> : <><WifiOff size={12} className="animate-pulse"/><span>Reconnecting…</span></>}
          </div>
          {/* Participant count with limit */}
          <div className={cn(
            'flex items-center gap-1.5 text-xs font-semibold border-l dark:border-surface-border border-lsurface-border pl-3',
            participantCount >= maxParticipants ? 'text-amber-400' : 'dark:text-neutral-400 text-neutral-500',
          )}>
            <Users size={12} />
            <span>{participantCount} / {maxParticipants}</span>
            {participantCount >= maxParticipants && <span className="text-[10px]">· Full</span>}
          </div>
          {/* Room type badge */}
          <div className="flex items-center gap-1.5 text-xs dark:text-neutral-500 text-neutral-400 border-l dark:border-surface-border border-lsurface-border pl-3">
            {isGroup ? <UsersRound size={11}/> : <UserCheck size={11}/>}
            <span className="capitalize">{roomType}</span>
          </div>
          <div className="flex items-center gap-1 text-xs dark:text-neutral-500 text-neutral-400 border-l dark:border-surface-border border-lsurface-border pl-3">
            <Hash size={11}/><span className="font-mono">{roomCode}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <InterviewTimer running={connected} />
          <button onClick={() => setShowInfo(v => !v)}
            className={cn('p-1.5 rounded-lg transition-colors',
              showInfo ? 'bg-brand-500/15 text-brand-500 border dark:border-brand-500/30 border-brand-500/20'
                       : 'dark:text-neutral-400 text-neutral-500 dark:hover:bg-surface-raised hover:bg-lsurface-raised')}>
            <Link2 size={14}/>
          </button>
        </div>
      </div>

      {/* ── Empty-room timeout banner (host only, public rooms) ──── */}
      <AnimatePresence>
        {emptyCountdown !== null && emptyCountdown > 0 && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}
            className="shrink-0 overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2 bg-amber-500/10 border-b border-amber-500/20">
              <div className="flex items-center gap-2 text-xs font-semibold text-amber-400">
                <Clock size={13} className="shrink-0" />
                <span>
                  Room is empty — will be closed in{' '}
                  <span className="tabular-nums font-bold">
                    {Math.floor(emptyCountdown / 60)}:{String(emptyCountdown % 60).padStart(2, '0')}
                  </span>
                  {' '}unless someone joins
                </span>
              </div>
              <button
                onClick={stopEmptyTimer}
                className="text-[11px] font-semibold text-amber-400 hover:text-amber-300 transition-colors underline"
              >
                Dismiss
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Info drawer ──────────────────────────────────────────── */}
      <AnimatePresence>
        {showInfo && (
          <motion.div initial={{ height:0, opacity:0 }} animate={{ height:'auto', opacity:1 }}
            exit={{ height:0, opacity:0 }} transition={{ duration:0.18 }}
            className="overflow-hidden dark:bg-surface-raised bg-lsurface-raised border-b dark:border-surface-border border-lsurface-border shrink-0">
            <div className="px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-3">
              <div className="flex-1 min-w-0">
                <p className="text-[11px] dark:text-neutral-500 text-neutral-400 font-semibold uppercase tracking-wider mb-1">Invite Link</p>
                <p className="text-xs dark:text-neutral-200 text-neutral-800 font-mono truncate">{inviteLink}</p>
              </div>
              <button onClick={onCopyLink}
                className={cn('flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold shrink-0 border transition-all',
                  copied ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                         : 'dark:bg-surface-card bg-lsurface-card dark:border-surface-border border-lsurface-border dark:text-neutral-300 text-neutral-700 hover:border-brand-500')}>
                {copied ? <Check size={12}/> : <Copy size={12}/>}
                {copied ? 'Copied!' : 'Copy Link'}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Body ─────────────────────────────────────────────────── */}
      <div className="flex-1 min-h-0 flex overflow-hidden">
        <div className="flex-1 min-w-0 flex flex-col p-3 gap-3">

          {/* Screen share tile */}
          <AnimatePresence>
            {activeScreen && (
              <motion.div initial={{ opacity:0, scale:0.98 }} animate={{ opacity:1, scale:1 }}
                exit={{ opacity:0 }}
                className="relative rounded-xl overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card flex-1 min-h-0 flex items-center justify-center">
                <VideoTrack trackRef={activeScreen} className="w-full h-full object-contain" />
                <span className="absolute top-2 left-3 text-[11px] font-semibold dark:text-neutral-200 text-white drop-shadow flex items-center gap-1">
                  <Monitor size={11} className="text-brand-500"/>
                  {activeScreen.participant.isLocal ? 'Your screen' : `${activeScreen.participant.name}'s screen`}
                </span>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Camera grid — 2-col for single, responsive wrap for group */}
          <div className={cn(
            'min-h-0',
            activeScreen ? 'h-32 shrink-0' : 'flex-1',
            isGroup
              ? 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2'
              : 'grid grid-cols-1 md:grid-cols-2 gap-3',
          )}>
            {/* Remote cams */}
            {isGroup ? (
              remoteCams.length > 0 ? remoteCams.map(track => (
                <div key={track.participant.identity}
                  className="relative rounded-xl overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card flex items-center justify-center min-h-[100px]">
                  {!track.publication?.isMuted
                    ? <VideoTrack trackRef={track} className="w-full h-full object-cover"/>
                    : <div className="flex flex-col items-center gap-1 dark:text-neutral-500 text-neutral-400 p-2">
                        <User size={24}/><p className="text-[10px]">{track.participant.name || 'Participant'}</p>
                      </div>}
                  <span className="absolute bottom-1.5 left-2 text-[10px] font-semibold dark:text-neutral-100 text-white drop-shadow">
                    {track.participant.name || 'Participant'}
                  </span>
                </div>
              )) : (
                <div className="col-span-full flex flex-col items-center justify-center gap-3 dark:bg-surface-card bg-lsurface-card rounded-xl border dark:border-surface-border border-lsurface-border min-h-[120px] text-center px-4">
                  <div className="p-3 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20"><Brain size={28}/></div>
                  <p className="text-sm font-semibold dark:text-neutral-300 text-neutral-600">Waiting for participants…</p>
                  <p className="text-xs dark:text-neutral-500 text-neutral-400">Share the invite link — up to {maxParticipants} people can join</p>
                  <div className="absolute inset-0 pointer-events-none flex items-center justify-center rounded-xl">
                    <div className="w-20 h-20 rounded-full border-2 border-brand-500/20 animate-ping"/>
                  </div>
                </div>
              )
            ) : (
              /* Single room — one remote slot */
              <div className="relative rounded-xl overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card flex items-center justify-center">
                {remoteCams[0] && !remoteCams[0].publication?.isMuted ? (
                  <VideoTrack trackRef={remoteCams[0]} className="w-full h-full object-cover"/>
                ) : (
                  <div className="flex flex-col items-center gap-3 text-center px-4">
                    {participantCount < 2 ? (
                      <>
                        <div className="p-4 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20"><Brain size={32}/></div>
                        <div>
                          <p className="text-sm font-semibold dark:text-neutral-300 text-neutral-600">Waiting for other person…</p>
                          <p className="text-xs dark:text-neutral-500 text-neutral-400 mt-0.5">Share the invite link</p>
                        </div>
                        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
                          <div className="w-20 h-20 rounded-full border-2 border-brand-500/20 animate-ping"/>
                        </div>
                      </>
                    ) : (
                      <div className="p-4 rounded-full dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-500 text-neutral-400"><User size={32}/></div>
                    )}
                  </div>
                )}
                <span className="absolute bottom-2 left-2.5 text-[11px] font-semibold dark:text-neutral-100 text-white drop-shadow">
                  {remoteCams[0] ? (remoteCams[0].participant.name || 'Participant') : 'Waiting…'}
                </span>
              </div>
            )}

            {/* Local cam (always shown) */}
            <div className="relative rounded-xl overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card flex items-center justify-center">
              {localCam && !localCam.publication?.isMuted && cam
                ? <VideoTrack trackRef={localCam} className="w-full h-full object-cover scale-x-[-1]"/>
                : <div className="flex flex-col items-center gap-2 dark:text-neutral-500 text-neutral-400">
                    <div className="p-4 rounded-full dark:bg-surface-raised bg-lsurface-raised"><User size={isGroup ? 24 : 32}/></div>
                    <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500">Camera off</p>
                  </div>}
              {!mic && (
                <span className="absolute top-2 right-2 flex items-center gap-1 bg-red-600 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">
                  <MicOff size={9}/> Muted
                </span>
              )}
              <span className="absolute bottom-2 left-2.5 text-[11px] font-semibold dark:text-neutral-100 text-white drop-shadow">You</span>
            </div>
          </div>
        </div>

        {/* ── Chat panel ──────────────────────────────────────────── */}
        <AnimatePresence>
          {chatOpen && (
            <motion.div initial={{ width:0, opacity:0 }} animate={{ width:300, opacity:1 }}
              exit={{ width:0, opacity:0 }} transition={{ duration:0.2 }}
              className="shrink-0 flex flex-col border-l dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card overflow-hidden">
              <div className="flex items-center justify-between px-3 py-2.5 border-b dark:border-surface-border border-lsurface-border shrink-0">
                <div className="flex items-center gap-2">
                  <MessageSquare size={13} className="text-brand-500"/>
                  <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900">In-call Chat</span>
                </div>
                <button onClick={() => setChatOpen(false)}
                  className="p-1 dark:text-neutral-500 text-neutral-400 dark:hover:text-neutral-200 hover:text-neutral-700 rounded-md dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-colors">
                  <X size={13}/>
                </button>
              </div>
              <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
                {messages.length === 0
                  ? <div className="flex flex-col items-center justify-center h-full gap-2 text-center opacity-60">
                      <MessageSquare size={22} className="dark:text-neutral-600 text-neutral-400"/>
                      <p className="text-xs dark:text-neutral-500 text-neutral-400">No messages yet</p>
                    </div>
                  : messages.map(m => (
                    <div key={m.id} className={cn('flex flex-col gap-0.5', m.self ? 'items-end' : 'items-start')}>
                      <div className="flex items-center gap-1.5">
                        <span className="text-[10px] font-semibold dark:text-neutral-400 text-neutral-500">{m.self ? 'You' : m.sender}</span>
                        <span className="text-[10px] dark:text-neutral-600 text-neutral-400">{fmt(m.ts)}</span>
                      </div>
                      <div className={cn('px-3 py-2 rounded-xl text-xs leading-relaxed max-w-[230px] border',
                        m.self
                          ? 'dark:bg-brand-500/10 bg-brand-50 dark:border-brand-500/25 border-brand-200 dark:text-neutral-100 text-neutral-900 rounded-tr-sm'
                          : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-200 text-neutral-800 rounded-tl-sm')}>
                        {m.text}
                      </div>
                    </div>
                  ))}
                <div ref={chatBottomRef}/>
              </div>
              <div className="shrink-0 px-3 py-2.5 border-t dark:border-surface-border border-lsurface-border">
                <div className="flex items-end gap-2">
                  <textarea value={chatInput} onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChatMessage() } }}
                    placeholder="Type a message…" rows={2}
                    className="flex-1 dark:bg-surface-base bg-lsurface-base border dark:border-surface-border border-lsurface-border focus:border-brand-500 rounded-xl px-3 py-2 text-xs dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-600 placeholder:text-neutral-400 resize-none focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition-all"/>
                  <button onClick={sendChatMessage} disabled={!chatInput.trim()}
                    className="p-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all shrink-0">
                    <Send size={13}/>
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ── Control bar ─────────────────────────────────────────────────── */}
      <div className="shrink-0 flex items-center justify-center gap-2 px-4 py-3 border-t dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        <CtrlBtn onClick={toggleMic}    active={mic}     icon={<Mic size={17}/>}       offIcon={<MicOff size={17}/>}     label={mic ? 'Mute' : 'Unmute'}/>
        <CtrlBtn onClick={toggleCam}    active={cam}     icon={<VideoIcon size={17}/>} offIcon={<VideoOff size={17}/>}   label={cam ? 'Stop Video' : 'Start Video'}/>
        <CtrlBtn onClick={toggleScreen} active={!sharing} icon={<Monitor size={17}/>}  offIcon={<MonitorOff size={17} className="text-brand-400"/>} label={sharing ? 'Stop Share' : 'Share Screen'}/>
        <CtrlBtn onClick={() => setChatOpen(v => !v)} active={chatOpen} icon={<MessageSquare size={17}/>} label="Chat" badge={unread}/>
        <CtrlBtn onClick={onCopyLink}   active={!copied} icon={<Copy size={17}/>}      offIcon={<Check size={17} className="text-emerald-400"/>} label={copied ? 'Copied!' : 'Copy Link'}/>
        <CtrlBtn onClick={handleLeave}  danger icon={<PhoneOff size={17}/>} label="Leave"/>
      </div>

      <RoomAudioRenderer/>
    </div>
  )
}

// ── Room Full screen ──────────────────────────────────────────────────────────
const RoomFullScreen = ({ roomCode, maxParticipants, roomType, onBack }:
  { roomCode: string; maxParticipants: number; roomType: RoomType; onBack: () => void }) => (
  <div className="flex flex-col items-center justify-center h-[calc(100vh-64px)] gap-5 text-center dark:bg-surface-base bg-lsurface-base px-4">
    <motion.div initial={{ scale:0.8, opacity:0 }} animate={{ scale:1, opacity:1 }}
      className="p-5 rounded-3xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
      <AlertTriangle size={44}/>
    </motion.div>
    <div className="space-y-2">
      <h2 className="text-xl font-bold dark:text-neutral-100 text-neutral-900">Room is Full</h2>
      <p className="text-sm dark:text-neutral-400 text-neutral-500 max-w-sm leading-relaxed">
        Room <span className="font-mono dark:text-neutral-200 text-neutral-800">{roomCode}</span> already has{' '}
        <strong>{maxParticipants}</strong> participant{maxParticipants > 1 ? 's' : ''} — the maximum for a{' '}
        <span className="capitalize">{roomType}</span> room.
      </p>
      <p className="text-xs dark:text-neutral-500 text-neutral-400">
        Ask the host to create a new room or wait for someone to leave.
      </p>
    </div>
    <Button variant="secondary" size="md" onClick={onBack}>Back to Rooms</Button>
  </div>
)

// ── Page shell ────────────────────────────────────────────────────────────────
export const VideoRoomSessionPage = () => {
  const { roomId } = useParams<{ roomId: string }>()
  const navigate   = useNavigate()
  const roomCode   = roomId ?? ''
  const roomType   = roomTypeFromCode(roomCode)
  const maxPeople  = ROOM_MAX[roomType]

  const { status, session, copied, joinRoom, copyInviteLink, reset } = useVideoRoom()

  useEffect(() => {
    if (!roomCode) return
    joinRoom(roomCode)
    return () => { reset() }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roomCode])

  const handleLeave = useCallback(() => navigate('/video-room'), [navigate])
  const handleCopy  = useCallback(() => { if (session) copyInviteLink(session.inviteLink) }, [session, copyInviteLink])

  if (status === 'full') {
    return <RoomFullScreen roomCode={roomCode} maxParticipants={maxPeople} roomType={roomType} onBack={() => navigate('/video-room')}/>
  }

  if (status === 'loading' || status === 'idle') {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-64px)] gap-4 dark:bg-surface-base bg-lsurface-base">
        <Spinner size="lg"/>
        <p className="text-sm font-semibold dark:text-neutral-200 text-neutral-800">Connecting to room…</p>
        <p className="text-xs dark:text-neutral-500 text-neutral-400 font-mono">{roomCode}</p>
      </div>
    )
  }

  if (status === 'error' || !session) {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-64px)] gap-5 text-center dark:bg-surface-base bg-lsurface-base">
        <div className="p-5 rounded-3xl bg-red-500/10 border border-red-500/20 text-red-400"><VideoIcon size={40}/></div>
        <div className="space-y-1">
          <h2 className="text-lg font-bold dark:text-neutral-100 text-neutral-900">Could Not Join Room</h2>
          <p className="text-sm dark:text-neutral-400 text-neutral-500 max-w-xs">
            Room code <span className="font-mono dark:text-neutral-200 text-neutral-800">"{roomCode}"</span> is invalid or the host hasn't created it yet.
          </p>
        </div>
        <Button variant="secondary" size="md" onClick={() => navigate('/video-room')}>Back to Rooms</Button>
      </div>
    )
  }

  return (
    <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} className="h-[calc(100vh-64px)] overflow-hidden">
      <LiveKitRoom
        token={session.token} serverUrl={session.serverUrl}
        connect={true} video={true} audio={true}
        onError={err => {
          const m = err.message.toLowerCase()
          showToast.error(m.includes('permission') || m.includes('notallowed')
            ? 'Camera/mic permission denied.'
            : `Connection error: ${err.message}`)
        }}
        className="h-full"
      >
        <SessionContent
          roomCode={roomCode}
          roomType={roomType}
          maxParticipants={maxPeople}
          inviteLink={session.inviteLink}
          visibility={session.visibility}
          isHost={session.role === 'host'}
          onLeave={handleLeave}
          onCopyLink={handleCopy}
          copied={copied}
        />
      </LiveKitRoom>
    </motion.div>
  )
}
