import { apiClient } from './client'
import type {
  LiveKitTokenResponse,
  CreateInterviewRoomResponse,
  StartInterviewRoomResponse,
  RoomStatusResponse,
} from '@/types/livekit'

// POST /livekit/token/{interview_id}
export const getLiveKitToken = async (
  interviewId: number
): Promise<LiveKitTokenResponse> => {
  const { data } = await apiClient.post<LiveKitTokenResponse>(
    `/livekit/token/${interviewId}`
  )
  return data
}

// POST /interview/{interview_id}/room/create
export const createInterviewRoom = async (
  interviewId: number
): Promise<CreateInterviewRoomResponse> => {
  const { data } = await apiClient.post<CreateInterviewRoomResponse>(
    `/interview/${interviewId}/room/create`
  )
  return data
}

// POST /interview/{interview_id}/room/start
export const startInterviewRoom = async (
  interviewId: number
): Promise<StartInterviewRoomResponse> => {
  const { data } = await apiClient.post<StartInterviewRoomResponse>(
    `/interview/${interviewId}/room/start`
  )
  return data
}

// POST /interview/{interview_id}/room/end  — prepared for future use
export const endInterviewRoom = async (
  interviewId: number
): Promise<{ success: boolean }> => {
  const { data } = await apiClient.post<{ success: boolean }>(
    `/interview/${interviewId}/room/end`
  )
  return data
}

// GET /interview/{interview_id}/room  — poll room status
export const getInterviewRoom = async (
  interviewId: number
): Promise<RoomStatusResponse> => {
  const { data } = await apiClient.get<RoomStatusResponse>(
    `/interview/${interviewId}/room`
  )
  return data
}

// ─────────────────────────────────────────────────────────────────────────────
// Standalone two-person room helpers
// Uses POST /livekit/room-token/{room_code} — no interview DB record needed.
// ─────────────────────────────────────────────────────────────────────────────

export interface StandaloneRoomTokenResponse {
  success: boolean
  room_code: string
  room: string
  token: string
  url: string
  participant: { id: number; name: string }
}

/** Fetch a LiveKit JWT for any arbitrary room code (no DB required) */
export const getRoomToken = async (
  roomCode: string
): Promise<StandaloneRoomTokenResponse> => {
  const { data } = await apiClient.post<StandaloneRoomTokenResponse>(
    `/livekit/room-token/${roomCode}`
  )
  return data
}

/**
 * Host flow: generate a prefixed room code, get a token, build invite link.
 *
 * Code prefixes:
 *   pub-s-xxxxxx  public  single  (max 2)
 *   pub-g-xxxxxx  public  group   (max 10)
 *   s-xxxxxx      private single  (max 2)
 *   g-xxxxxx      private group   (max 10)
 */
export const setupStandaloneRoom = async (
  roomType:   'single' | 'group' = 'single',
  visibility: 'public' | 'private' = 'private',
) => {
  const suffix     = Math.random().toString(36).slice(2, 8)
  const typePfx    = roomType === 'group' ? 'g' : 's'
  const roomCode   = visibility === 'public'
    ? `pub-${typePfx}-${suffix}`   // e.g. "pub-s-k7m2xq"
    : `${typePfx}-${suffix}`       // e.g. "s-k7m2xq"

  const res = await getRoomToken(roomCode)
  if (!res.success || !res.token) throw new Error('Failed to obtain session token')

  const inviteLink = `${window.location.origin}/room/${roomCode}`

  return { roomCode, roomType, visibility, token: res.token, serverUrl: res.url, roomName: res.room, inviteLink, participant: res.participant }
}

/**
 * Guest flow: join an existing room by its code.
 * Same endpoint — LiveKit allows any authenticated user to join.
 */
export const joinStandaloneRoom = async (roomCode: string) => {
  const res = await getRoomToken(roomCode)
  if (!res.success || !res.token) throw new Error('Failed to obtain session token')
  return {
    roomCode,
    token:       res.token,
    serverUrl:   res.url,
    roomName:    res.room,
    participant: res.participant,
  }
}
