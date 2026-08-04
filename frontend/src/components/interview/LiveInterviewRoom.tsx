import { useEffect, useCallback, useState } from 'react'
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useRoomContext,
  useTracks,
  VideoTrack,
} from '@livekit/components-react'
import '@livekit/components-styles'
import { Track, RoomEvent } from 'livekit-client'
import { motion } from 'framer-motion'
import { Brain, User, Wifi, WifiOff } from 'lucide-react'
import { showToast } from '@/components/ui/Toast'
import { InterviewControls } from './InterviewControls'
import { InterviewTimer } from './InterviewTimer'
import { cn } from '@/utils'

// ── Inner room component (must be child of <LiveKitRoom>) ────────────────────
const RoomContent = ({
  onLeave,
}: {
  interviewId?: number
  onLeave: () => void
}) => {
  const room = useRoomContext()

  const [micEnabled, setMicEnabled] = useState(true)
  const [cameraEnabled, setCameraEnabled] = useState(true)
  const [connected, setConnected] = useState(false)

  // Local camera track
  const localTracks = useTracks(
    [{ source: Track.Source.Camera, withPlaceholder: true }],
    { onlySubscribed: false }
  )

  // Remote participant tracks
  const remoteTracks = useTracks(
    [{ source: Track.Source.Camera, withPlaceholder: true }],
    { onlySubscribed: true }
  )

  useEffect(() => {
    const handleConnected = () => {
      setConnected(true)
      showToast.success('Connected to interview room')
    }
    const handleDisconnected = () => {
      setConnected(false)
      showToast.info('Disconnected from interview room')
    }
    const handleError = (err: Error) => {
      showToast.error(`Connection error: ${err.message}`)
    }

    room.on(RoomEvent.Connected, handleConnected)
    room.on(RoomEvent.Disconnected, handleDisconnected)
    room.on(RoomEvent.MediaDevicesError, handleError)

    return () => {
      room.off(RoomEvent.Connected, handleConnected)
      room.off(RoomEvent.Disconnected, handleDisconnected)
      room.off(RoomEvent.MediaDevicesError, handleError)
    }
  }, [room])

  const handleToggleMic = useCallback(async () => {
    try {
      await room.localParticipant.setMicrophoneEnabled(!micEnabled)
      setMicEnabled((v) => !v)
    } catch {
      showToast.error('Could not toggle microphone. Check browser permissions.')
    }
  }, [room, micEnabled])

  const handleToggleCamera = useCallback(async () => {
    try {
      await room.localParticipant.setCameraEnabled(!cameraEnabled)
      setCameraEnabled((v) => !v)
    } catch {
      showToast.error('Could not toggle camera. Check browser permissions.')
    }
  }, [room, cameraEnabled])

  const handleLeave = useCallback(async () => {
    await room.disconnect()
    onLeave()
  }, [room, onLeave])

  const localVideoTrack = localTracks.find(
    (t) => t.participant === room.localParticipant
  )
  const remoteVideoTrack = remoteTracks.find(
    (t) => t.participant !== room.localParticipant
  )

  return (
    <div className="flex flex-col h-full gap-3">
      {/* ── Status bar ──────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2 text-xs dark:text-neutral-400 text-neutral-500">
          {connected ? (
            <Wifi size={13} className="text-emerald-400" />
          ) : (
            <WifiOff size={13} className="text-red-400 animate-pulse" />
          )}
          <span>{connected ? 'Live' : 'Reconnecting…'}</span>
        </div>
        <InterviewTimer running={connected} />
      </div>

      {/* ── Video grid ──────────────────────────────────────────────────── */}
      <div className="flex-1 grid grid-rows-2 gap-3 min-h-0">
        {/* Remote participant */}
        <div
          className={cn(
            'relative rounded-2xl overflow-hidden border',
            'dark:border-surface-border border-lsurface-border',
            'dark:bg-neutral-900 bg-neutral-100',
            'flex items-center justify-center'
          )}
        >
          {remoteVideoTrack ? (
            <VideoTrack
              trackRef={remoteVideoTrack}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="flex flex-col items-center gap-3 text-center px-6">
              <div className="p-4 rounded-full bg-brand-500/20 text-brand-400">
                <Brain size={36} />
              </div>
              <p className="text-sm font-semibold dark:text-neutral-300 text-neutral-600">
                Interviewer
              </p>
              <p className="text-xs dark:text-neutral-500 text-neutral-400">
                Waiting for interviewer to join…
              </p>
            </div>
          )}
          <span className="absolute bottom-2 left-3 text-[11px] font-semibold dark:text-neutral-200 text-white drop-shadow">
            Interviewer
          </span>
        </div>

        {/* Local participant */}
        <div
          className={cn(
            'relative rounded-2xl overflow-hidden border',
            'dark:border-surface-border border-lsurface-border',
            'dark:bg-neutral-900 bg-neutral-100',
            'flex items-center justify-center'
          )}
        >
          {localVideoTrack && !localVideoTrack.publication?.isMuted ? (
            <VideoTrack
              trackRef={localVideoTrack}
              className="w-full h-full object-cover scale-x-[-1]"
            />
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="p-4 rounded-full dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-400 text-neutral-500">
                <User size={36} />
              </div>
              <p className="text-sm font-semibold dark:text-neutral-300 text-neutral-600">
                Camera off
              </p>
            </div>
          )}
          <span className="absolute bottom-2 left-3 text-[11px] font-semibold dark:text-neutral-200 text-white drop-shadow">
            You
          </span>
          {!micEnabled && (
            <span className="absolute top-2 right-2 bg-red-600 text-white text-[10px] font-semibold px-2 py-0.5 rounded-full">
              Muted
            </span>
          )}
        </div>
      </div>

      {/* ── Controls ────────────────────────────────────────────────────── */}
      <InterviewControls
        micEnabled={micEnabled}
        cameraEnabled={cameraEnabled}
        onToggleMic={handleToggleMic}
        onToggleCamera={handleToggleCamera}
        onLeave={handleLeave}
      />

      <RoomAudioRenderer />
    </div>
  )
}

// ── Public component: handles LiveKitRoom wrapper ────────────────────────────
interface LiveInterviewRoomProps {
  token: string
  serverUrl: string
  /** Used only for the default leave navigation (optional) */
  interviewId?: number
  onLeave?: () => void
}

export const LiveInterviewRoom = ({
  token,
  serverUrl,
  interviewId,
  onLeave = () => {},
}: LiveInterviewRoomProps) => {
  const handleError = useCallback((err: Error) => {
    const msg = err.message.toLowerCase()
    if (msg.includes('permission') || msg.includes('notallowed')) {
      showToast.error('Camera/microphone permission denied. Please allow access and rejoin.')
    } else if (msg.includes('token') || msg.includes('invalid')) {
      showToast.error('Invalid session token. Please restart the interview.')
    } else {
      showToast.error(`Failed to connect: ${err.message}`)
    }
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.25 }}
      className="h-full"
    >
      <LiveKitRoom
        token={token}
        serverUrl={serverUrl}
        connect={true}
        video={true}
        audio={true}
        onError={handleError}
        className="h-full"
        data-lk-theme="default"
      >
        <RoomContent interviewId={interviewId} onLeave={onLeave} />
      </LiveKitRoom>
    </motion.div>
  )
}
