// ── LiveKit Token ────────────────────────────────────────────────────────────
export interface LiveKitTokenResponse {
  success: boolean
  room: string
  token: string
  url: string
  participant: {
    id: number
    name: string
  }
}

// ── Interview Room ────────────────────────────────────────────────────────────
export interface InterviewRoomDetails {
  id: number
  room_name: string
  livekit_url: string
  status: 'waiting' | 'active' | 'ended'
}

export interface CreateInterviewRoomResponse {
  success: boolean
  room: InterviewRoomDetails
}

export interface StartInterviewRoomResponse {
  success: boolean
  status: string
  started_at: string
}

// ── Connection state used by UI components ───────────────────────────────────
export type LiveKitConnectionStatus =
  | 'idle'
  | 'creating_room'
  | 'starting_room'
  | 'fetching_token'
  | 'connecting'
  | 'connected'
  | 'disconnected'
  | 'error'

// ─────────────────────────────────────────────────────────────────────────────
// Standalone Video Room (two-person, shareable link)
// ─────────────────────────────────────────────────────────────────────────────

export type RoomParticipantRole = 'host' | 'guest'
export type RoomType            = 'single' | 'group'
export type RoomVisibility      = 'public' | 'private'

export const ROOM_MAX: Record<RoomType, number> = { single: 2, group: 10 }

/** Derive room type from a room code prefix */
export const roomTypeFromCode = (code: string): RoomType =>
  code.startsWith('g-') ? 'group' : 'single'

/** Derive visibility from a room code prefix (pub- = public) */
export const roomVisibilityFromCode = (code: string): RoomVisibility =>
  code.startsWith('pub-') ? 'public' : 'private'

// ── Public room registry entry (stored in localStorage) ──────────────────────
export interface RoomListing {
  roomCode:         string
  roomType:         RoomType
  visibility:       RoomVisibility
  hostName:         string
  title:            string          // custom title set by host
  createdAt:        string          // ISO timestamp
  participantCount: number          // updated on join/leave via BroadcastChannel
  emptyAt:          string | null   // ISO — set when participantCount drops to 0; null otherwise
}

/** Stored in localStorage so we can rejoin after refresh */
export interface RoomSession {
  roomCode:        string
  roomName:        string
  token:           string
  serverUrl:       string
  role:            RoomParticipantRole
  roomType:        RoomType
  visibility:      RoomVisibility
  title:           string
  participantName: string
  createdAt:       string
}

/** Shape returned when the host creates a standalone room via our backend */
export interface CreateRoomResponse {
  success: boolean
  roomCode: string
  roomName: string
  token: string
  url: string
  inviteLink: string     // full shareable URL constructed on frontend
}

/** Shape returned when a guest joins by room code */
export interface JoinRoomResponse {
  success: boolean
  roomCode: string
  roomName: string
  token: string
  url: string
}

/** Minimal status check response */
export interface RoomStatusResponse {
  success: boolean
  roomCode: string
  status: 'waiting' | 'active' | 'ended'
  participantCount: number
}
