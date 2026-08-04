/**
 * useActiveSession
 * ─────────────────────────────────────────────────────────────────────────────
 * Tracks whether the user is currently in an active interview or coding session.
 * Returns the active session info and a confirmation callback to use before
 * navigating away.
 *
 * "Active" means the current URL matches a session route:
 *   /interview/:id/session
 *   /coding/:id   (but NOT /coding/:id/report)
 *   /room/:roomId
 */

import { useLocation, useNavigate } from 'react-router-dom'
import { useState, useCallback } from 'react'

export type SessionKind = 'interview' | 'coding' | 'video' | null

interface ActiveSession {
  kind:      SessionKind
  id:        string
  returnUrl: string
  label:     string
}

const PATTERNS: Array<{ regex: RegExp; kind: SessionKind; label: string }> = [
  { regex: /^\/interview\/(\d+)\/session$/,     kind: 'interview', label: 'Technical Interview' },
  { regex: /^\/coding\/(\d+)$/,                 kind: 'coding',    label: 'Coding Interview'   },
  { regex: /^\/room\/([^/]+)$/,                 kind: 'video',     label: 'Video Interview'    },
]

export const useActiveSession = (): {
  activeSession: ActiveSession | null
  /** Returns true if navigation is safe (no active session or user confirmed). */
  confirmNavAway: (destination: string, onConfirmed: () => void) => boolean
  pendingNav: string | null
  confirmLeave: () => void
  cancelLeave: () => void
} => {
  const location = useNavigate()  // eslint-disable-line @typescript-eslint/no-unused-vars
  const loc      = useLocation()
  const navigate = useNavigate()

  const [pendingNav, setPendingNav] = useState<string | null>(null)

  // Detect active session from current pathname
  const activeSession: ActiveSession | null = (() => {
    for (const p of PATTERNS) {
      const m = loc.pathname.match(p.regex)
      if (m) {
        return {
          kind:      p.kind,
          id:        m[1],
          returnUrl: loc.pathname,
          label:     p.label,
        }
      }
    }
    return null
  })()

  const confirmNavAway = useCallback((destination: string, onConfirmed: () => void): boolean => {
    if (!activeSession) {
      onConfirmed()
      return true
    }
    // Same section — always allow
    if (destination.startsWith(loc.pathname.split('/').slice(0, 3).join('/'))) {
      onConfirmed()
      return true
    }
    setPendingNav(destination)
    return false
  }, [activeSession, loc.pathname])

  const confirmLeave = useCallback(() => {
    if (pendingNav) {
      navigate(pendingNav)
    }
    setPendingNav(null)
  }, [pendingNav, navigate])

  const cancelLeave = useCallback(() => {
    setPendingNav(null)
  }, [])

  return { activeSession, confirmNavAway, pendingNav, confirmLeave, cancelLeave }
}
