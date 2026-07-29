import { useEffect, useRef, useCallback, useState } from 'react'
import { useAuthStore } from '@/store'
import type { WsMessage, WsEventType, WsQuestionPayload, EvaluationResult } from '@/types'

const WS_BASE = import.meta.env.VITE_WS_BASE_URL ?? 'ws://localhost:8000'

// ── Typed payloads received from server ─────────────────────────────────────
export interface WsInterviewStartedPayload {
  type: 'interview_started'
  question: WsQuestionPayload
  total_questions: number
}

export interface WsSubmissionResultPayload {
  type: 'submission_result'
  execution: { success: boolean; stdout: string; stderr: string; return_code: number }
  evaluation: EvaluationResult
}

export interface WsNextQuestionPayload {
  type: 'next_question'
  question: WsQuestionPayload
}

export interface WsInterviewCompletedPayload {
  type: 'interview_completed'
  score: number
  message: string
}

export interface WsDraftSavedPayload {
  type: 'draft_saved'
}

export interface WsErrorPayload {
  type: 'error'
  message: string
}

export type WsServerPayload =
  | WsInterviewStartedPayload
  | WsSubmissionResultPayload
  | WsNextQuestionPayload
  | WsInterviewCompletedPayload
  | WsDraftSavedPayload
  | WsErrorPayload

export type WsStatus = 'idle' | 'connecting' | 'connected' | 'disconnected' | 'error'

interface UseCodingWebSocketOptions {
  interviewId: number
  onMessage: (msg: WsServerPayload) => void
  onOpen?: () => void
  onClose?: () => void
  onError?: (e: Event) => void
  autoConnect?: boolean
}

export const useCodingWebSocket = ({
  interviewId,
  onMessage,
  onOpen,
  onClose,
  onError,
  autoConnect = true,
}: UseCodingWebSocketOptions) => {
  const [status, setStatus] = useState<WsStatus>('idle')
  const wsRef = useRef<WebSocket | null>(null)
  const onMessageRef = useRef(onMessage)
  const onOpenRef = useRef(onOpen)
  const onCloseRef = useRef(onClose)
  const onErrorRef = useRef(onError)

  // Keep callback refs fresh without re-connecting
  useEffect(() => { onMessageRef.current = onMessage }, [onMessage])
  useEffect(() => { onOpenRef.current = onOpen }, [onOpen])
  useEffect(() => { onCloseRef.current = onClose }, [onClose])
  useEffect(() => { onErrorRef.current = onError }, [onError])

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    const token = useAuthStore.getState().accessToken
    if (!token) return

    setStatus('connecting')

    const url = `${WS_BASE}/ws/coding-interview/${interviewId}?token=${encodeURIComponent(token)}`
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      setStatus('connected')
      onOpenRef.current?.()
    }

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data) as WsServerPayload
        onMessageRef.current(msg)
      } catch {
        console.error('[WS] Failed to parse message:', event.data)
      }
    }

    ws.onclose = () => {
      setStatus('disconnected')
      onCloseRef.current?.()
      wsRef.current = null
    }

    ws.onerror = (e) => {
      setStatus('error')
      onErrorRef.current?.(e)
    }
  }, [interviewId])

  const disconnect = useCallback(() => {
    wsRef.current?.close()
    wsRef.current = null
    setStatus('disconnected')
  }, [])

  const send = useCallback((type: WsEventType, payload?: Record<string, unknown>) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) {
      console.warn('[WS] Cannot send — not connected')
      return false
    }
    wsRef.current.send(JSON.stringify({ type, ...payload }))
    return true
  }, [])

  // Auto-connect on mount
  useEffect(() => {
    if (autoConnect) connect()
    return () => { wsRef.current?.close(); wsRef.current = null }
  }, [connect, autoConnect])

  return { status, connect, disconnect, send }
}
