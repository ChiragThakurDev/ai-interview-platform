import { useState, useCallback } from 'react'
import { setupStandaloneRoom, joinStandaloneRoom } from '@/api/livekit'
import { showToast } from '@/components/ui/Toast'
import { roomTypeFromCode, roomVisibilityFromCode, ROOM_MAX } from '@/types/livekit'
import type { RoomParticipantRole, RoomType, RoomVisibility } from '@/types/livekit'
import { useRoomRegistry } from './useRoomRegistry'

export type VideoRoomStatus = 'idle' | 'loading' | 'ready' | 'full' | 'error'

export interface VideoRoomSession {
  roomCode:        string
  token:           string
  serverUrl:       string
  roomName:        string
  inviteLink:      string
  role:            RoomParticipantRole
  roomType:        RoomType
  visibility:      RoomVisibility
  title:           string
  maxParticipants: number
  participantName: string
}

const isRoomFull = (err: unknown): boolean => {
  const msg = err instanceof Error
    ? err.message
    : String((err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? '')
  return msg.includes('ROOM_FULL')
}

export const useVideoRoom = () => {
  const [status,  setStatus]  = useState<VideoRoomStatus>('idle')
  const [session, setSession] = useState<VideoRoomSession | null>(null)
  const [copied,  setCopied]  = useState(false)
  const [error,   setError]   = useState<string | null>(null)

  const { addRoom, removeRoom } = useRoomRegistry()

  // ── Host: create room ─────────────────────────────────────────────────────
  const createRoom = useCallback(async (
    roomType:   RoomType       = 'single',
    visibility: RoomVisibility = 'private',
    title:      string         = '',
    hostName:   string         = 'Host',
  ) => {
    setStatus('loading')
    setError(null)
    try {
      const res  = await setupStandaloneRoom(roomType, visibility)
      const type = roomTypeFromCode(res.roomCode)
      const vis  = roomVisibilityFromCode(res.roomCode)
      const sess: VideoRoomSession = {
        roomCode:        res.roomCode,
        token:           res.token,
        serverUrl:       res.serverUrl,
        roomName:        res.roomName,
        inviteLink:      res.inviteLink,
        role:            'host',
        roomType:        type,
        visibility:      vis,
        title:           title || `${hostName}'s ${type} room`,
        maxParticipants: ROOM_MAX[type],
        participantName: res.participant.name,
      }
      setSession(sess)
      setStatus('ready')

      // Register public rooms so the lobby can list them
      if (vis === 'public') {
        addRoom({
          roomCode:         res.roomCode,
          roomType:         type,
          visibility:       vis,
          hostName,
          title:            sess.title,
          createdAt:        new Date().toISOString(),
          participantCount: 1,
        })
      }

      showToast.success(vis === 'public' ? 'Public room created and listed!' : 'Room created! Share the invite link.')
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create room'
      setError(msg)
      setStatus('error')
      showToast.error(msg)
    }
  }, [addRoom])

  // ── Guest: join by code ───────────────────────────────────────────────────
  const joinRoom = useCallback(async (roomCode: string) => {
    setStatus('loading')
    setError(null)
    try {
      const res  = await joinStandaloneRoom(roomCode)
      const type = roomTypeFromCode(roomCode)
      const vis  = roomVisibilityFromCode(roomCode)
      setSession({
        roomCode,
        token:           res.token,
        serverUrl:       res.serverUrl,
        roomName:        res.roomName,
        inviteLink:      `${window.location.origin}/room/${roomCode}`,
        role:            'guest',
        roomType:        type,
        visibility:      vis,
        title:           '',
        maxParticipants: ROOM_MAX[type],
        participantName: res.participant.name,
      })
      setStatus('ready')
    } catch (err) {
      if (isRoomFull(err)) {
        setStatus('full')
        setError('room_full')
      } else {
        const msg = err instanceof Error ? err.message : 'Failed to join room'
        setError(msg)
        setStatus('error')
        showToast.error(msg)
      }
    }
  }, [])

  // ── Leave: remove public room from registry ───────────────────────────────
  const leaveRoom = useCallback(() => {
    if (session?.visibility === 'public' && session.role === 'host') {
      removeRoom(session.roomCode)
    }
    reset()
  }, [session, removeRoom]) // eslint-disable-line react-hooks/exhaustive-deps

  const copyInviteLink = useCallback(async (link: string) => {
    try {
      await navigator.clipboard.writeText(link)
      setCopied(true)
      showToast.success('Invite link copied!')
      setTimeout(() => setCopied(false), 2500)
    } catch {
      showToast.error('Could not copy — please copy manually.')
    }
  }, [])

  const reset = useCallback(() => {
    setStatus('idle')
    setSession(null)
    setError(null)
    setCopied(false)
  }, [])

  return { status, session, copied, error, createRoom, joinRoom, leaveRoom, copyInviteLink, reset }
}
