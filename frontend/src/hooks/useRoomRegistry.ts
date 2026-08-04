/**
 * useRoomRegistry
 * ─────────────────────────────────────────────────────────────────────────────
 * localStorage-backed registry of PUBLIC room listings.
 * BroadcastChannel keeps all open tabs in sync.
 *
 * Lifecycle rules:
 *   • Rooms older than 8 h are always pruned (host closed tab without cleanup).
 *   • When participantCount drops to 0, emptyAt is set to now().
 *   • Rooms that have been empty for ≥ EMPTY_TIMEOUT_MS (15 min) are pruned.
 *   • The cleanup interval runs every 60 s in every open tab.
 */

import { useState, useEffect, useCallback } from 'react'
import type { RoomListing } from '@/types/livekit'

const STORAGE_KEY      = 'video_room_registry'
const BC_CHANNEL       = 'room_registry_sync'
const TTL_MS           = 8 * 60 * 60 * 1000   // 8 h — stale host tab
export const EMPTY_TIMEOUT_MS = 15 * 60 * 1000 // 15 min — nobody in the room

// ── Pure helpers ──────────────────────────────────────────────────────────────
const readRegistry = (): RoomListing[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as RoomListing[]) : []
  } catch { return [] }
}

const writeRegistry = (rooms: RoomListing[]) =>
  localStorage.setItem(STORAGE_KEY, JSON.stringify(rooms))

const isExpired = (r: RoomListing): boolean => {
  const now = Date.now()
  // Too old overall
  if (now - new Date(r.createdAt).getTime() > TTL_MS) return true
  // Empty for too long
  if (r.emptyAt && now - new Date(r.emptyAt).getTime() > EMPTY_TIMEOUT_MS) return true
  return false
}

const prune = (rooms: RoomListing[]): RoomListing[] =>
  rooms.filter(r => !isExpired(r))

// ── Hook ──────────────────────────────────────────────────────────────────────
export const useRoomRegistry = () => {
  const [rooms, setRooms] = useState<RoomListing[]>(() => prune(readRegistry()))

  const reload = useCallback(() => {
    const fresh = prune(readRegistry())
    writeRegistry(fresh)
    setRooms(fresh)
  }, [])

  const broadcast = useCallback(() => {
    if (typeof window === 'undefined' || !('BroadcastChannel' in window)) return
    const bc = new BroadcastChannel(BC_CHANNEL)
    bc.postMessage('sync')
    bc.close()
  }, [])

  // BroadcastChannel sync across tabs
  useEffect(() => {
    if (typeof window === 'undefined' || !('BroadcastChannel' in window)) return
    const bc = new BroadcastChannel(BC_CHANNEL)
    bc.onmessage = reload
    return () => bc.close()
  }, [reload])

  // Cleanup interval — runs in every tab, prunes expired rooms every 60 s
  useEffect(() => {
    const id = setInterval(() => {
      const before = readRegistry()
      const after  = prune(before)
      if (after.length !== before.length) {
        writeRegistry(after)
        setRooms(after)
        broadcast()
      }
    }, 60_000)
    return () => clearInterval(id)
  }, [broadcast])

  /** Add or replace a room listing */
  const addRoom = useCallback((listing: RoomListing) => {
    const next = [
      ...prune(readRegistry()).filter(r => r.roomCode !== listing.roomCode),
      { ...listing, emptyAt: listing.emptyAt ?? null },
    ]
    writeRegistry(next)
    setRooms(next)
    broadcast()
  }, [broadcast])

  /** Remove a room listing by code */
  const removeRoom = useCallback((roomCode: string) => {
    const next = prune(readRegistry()).filter(r => r.roomCode !== roomCode)
    writeRegistry(next)
    setRooms(next)
    broadcast()
  }, [broadcast])

  /**
   * Update participant count.
   * When count reaches 0, stamp emptyAt so the timeout clock starts.
   * When count rises above 0 again, clear emptyAt.
   */
  const updateCount = useCallback((roomCode: string, delta: 1 | -1) => {
    const next = prune(readRegistry()).map(r => {
      if (r.roomCode !== roomCode) return r
      const newCount = Math.max(0, r.participantCount + delta)
      return {
        ...r,
        participantCount: newCount,
        emptyAt: newCount === 0
          ? (r.emptyAt ?? new Date().toISOString())  // stamp only once
          : null,                                      // clear when someone joins
      }
    })
    writeRegistry(next)
    setRooms(next)
    broadcast()
  }, [broadcast])

  const publicRooms = rooms
    .filter(r => r.visibility === 'public')
    .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())

  return { publicRooms, allRooms: rooms, addRoom, removeRoom, updateCount, reload }
}
