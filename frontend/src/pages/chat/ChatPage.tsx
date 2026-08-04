import { useState, useEffect, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  MessageSquare, Plus, Send, Trash2, Mic, MicOff,
  Volume2, Code, Brain, Terminal, Copy, Check, User, Bot, X, Map,
} from 'lucide-react'
import {
  useChatSessions, useChatMessages, useCreateChatSession,
  useSendMessage, useDeleteChatSession,
} from '@/hooks'
import { Card, Button, Spinner, EmptyState } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'

const QUICK_PROMPTS = [
  { icon: Brain,    label: 'System Design', prompt: 'Walk me through designing a real-time notification system like Slack.' },
  { icon: Code,     label: 'DSA Prep',       prompt: 'Explain the difference between Dynamic Programming and Greedy algorithms with examples.' },
  { icon: Terminal, label: 'Behavioral',      prompt: 'How do I answer "Tell me about a time you had a conflict" using the STAR method?' },
  { icon: Map,      label: 'Roadmap',         prompt: 'Create a 4-week interview prep roadmap for backend engineering with daily practice goals.' },
  { icon: Brain,    label: 'Resume Tips',     prompt: 'What key achievements should I highlight for a Senior Full Stack Engineer role?' },
]

const TypewriterText = ({ text }: { text: string }) => {
  const [displayed, setDisplayed] = useState('')

  useEffect(() => {
    let i = 0
    setDisplayed('')
    const timer = setInterval(() => {
      setDisplayed(text.substring(0, i + 5)) // typing chunks of 5 chars for speed
      i += 5
      if (i >= text.length) clearInterval(timer)
    }, 15)
    return () => clearInterval(timer)
  }, [text])

  return <p className="whitespace-pre-wrap">{displayed}</p>
}

export const ChatPage = () => {
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null)
  const [inputMessage, setInputMessage] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [optimisticMessage, setOptimisticMessage] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const { data: sessions, isLoading: loadingSessions } = useChatSessions()
  const { data: messages, isLoading: loadingMessages } = useChatMessages(
    activeSessionId ?? 0,
    !!activeSessionId,
  )
  const { mutate: createSession, isPending: creatingSession } = useCreateChatSession()
  const { mutate: sendMsg, isPending: sendingMsg } = useSendMessage()
  const { mutate: deleteSession } = useDeleteChatSession()

  // Auto-select first session on load
  useEffect(() => {
    if (sessions && sessions.length > 0 && !activeSessionId) {
      setActiveSessionId(sessions[0].id)
    }
  }, [sessions, activeSessionId])

  // Clear optimistic message when new messages arrive
  useEffect(() => {
    setOptimisticMessage(null)
  }, [messages])

  // Scroll to bottom when messages change or AI is thinking
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, sendingMsg, optimisticMessage])

  const selectSession = (id: number) => {
    setActiveSessionId(id)
    setSidebarOpen(false)
  }

  const handleCreateNewSession = (title = 'New Chat') => {
    createSession({ title }, {
      onSuccess: (s) => { setActiveSessionId(s.id); setSidebarOpen(false) },
      onError: () => showToast('error', 'Failed to create chat session'),
    })
  }

  const doSend = (text: string) => {
    text = text.trim()
    if (!text || sendingMsg) return

    if (!activeSessionId) {
      setOptimisticMessage(text)
      setInputMessage('')
      createSession({ title: text.slice(0, 40) }, {
        onSuccess: (s) => {
          setActiveSessionId(s.id)
          sendMsg({ sessionId: s.id, body: { message: text } }, {
            onError: () => { setOptimisticMessage(null); showToast('error', 'Failed to send message') },
          })
        },
        onError: () => { setOptimisticMessage(null); showToast('error', 'Failed to create chat session') },
      })
      return
    }

    setOptimisticMessage(text)
    setInputMessage('')
    sendMsg({ sessionId: activeSessionId, body: { message: text } }, {
      onError: () => {
        showToast('error', 'Failed to send message')
        setInputMessage(text)
        setOptimisticMessage(null)
      },
    })
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      doSend(inputMessage)
    }
  }

  const handleDeleteSession = (e: React.MouseEvent, id: number) => {
    e.stopPropagation()
    deleteSession(id, {
      onSuccess: () => {
        showToast('info', 'Chat deleted')
        if (activeSessionId === id) {
          const remaining = sessions?.filter(s => s.id !== id)
          setActiveSessionId(remaining && remaining.length > 0 ? remaining[0].id : null)
        }
      },
      onError: () => showToast('error', 'Failed to delete chat'),
    })
  }

  // Voice input
  const toggleVoice = () => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SR) { showToast('warning', 'Speech recognition not supported in this browser'); return }
    if (isListening) { setIsListening(false); return }
    const r = new SR()
    r.continuous = false; r.interimResults = false; r.lang = 'en-US'
    r.onstart = () => setIsListening(true)
    r.onend   = () => setIsListening(false)
    r.onerror = () => { setIsListening(false); showToast('error', 'Speech recognition error') }
    r.onresult = (ev: any) => {
      const t = ev.results[0][0].transcript
      setInputMessage(p => p ? `${p} ${t}` : t)
      inputRef.current?.focus()
    }
    r.start()
  }

  const speak = (text: string) => {
    if (!('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    window.speechSynthesis.speak(Object.assign(new SpeechSynthesisUtterance(text), { rate: 1 }))
  }

  const copy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const showEmpty = !activeSessionId || (!loadingMessages && (!messages || messages.length === 0) && !optimisticMessage)

  // Combine real messages with optimistic user message
  const displayMessages = useMemo(() => {
    if (!messages) return optimisticMessage ? [{ role: 'user', content: optimisticMessage, id: 'opt' }] : []
    return optimisticMessage
      ? [...messages, { role: 'user', content: optimisticMessage, id: 'opt' }]
      : messages
  }, [messages, optimisticMessage])

  return (
    <div className="h-[calc(100vh-5.5rem)] flex gap-4 overflow-hidden">

      {/* ── Sessions sidebar ─────────────────────── */}
      {/* Desktop */}
      <Card className="hidden md:flex flex-col w-64 shrink-0 h-full p-0 overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        <div className="flex items-center justify-between px-4 py-3.5 border-b dark:border-surface-border border-lsurface-border">
          <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2">
            <MessageSquare size={14} className="text-brand-500" /> Chats
          </span>
          <Button size="xs" variant="primary" onClick={() => handleCreateNewSession()} loading={creatingSession} icon={<Plus size={12} />}>New</Button>
        </div>
        <SessionList sessions={sessions} loadingSessions={loadingSessions} activeSessionId={activeSessionId}
          onSelect={selectSession} onDelete={handleDeleteSession} />
      </Card>

      {/* Mobile sidebar overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-black/60 md:hidden" onClick={() => setSidebarOpen(false)} />
            <motion.div initial={{ x: -280 }} animate={{ x: 0 }} exit={{ x: -280 }}
              transition={{ type: 'tween', duration: 0.2 }}
              className="fixed inset-y-0 left-0 z-50 w-72 dark:bg-surface-card bg-white border-r dark:border-surface-border border-lsurface-border flex flex-col md:hidden">
              <div className="flex items-center justify-between px-4 py-3.5 border-b dark:border-surface-border border-lsurface-border">
                <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2">
                  <MessageSquare size={14} className="text-brand-500" /> Chats
                </span>
                <div className="flex items-center gap-2">
                  <Button size="xs" variant="primary" onClick={() => handleCreateNewSession()} loading={creatingSession} icon={<Plus size={12} />}>New</Button>
                  <button onClick={() => setSidebarOpen(false)} className="p-1 dark:text-neutral-400 text-neutral-500"><X size={15} /></button>
                </div>
              </div>
              <SessionList sessions={sessions} loadingSessions={loadingSessions} activeSessionId={activeSessionId}
                onSelect={selectSession} onDelete={handleDeleteSession} />
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* ── Main chat pane ─────────────────────── */}
      <Card className="flex-1 flex flex-col h-full p-0 overflow-hidden border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        {/* Header */}
        <div className="flex items-center gap-3 px-5 py-3.5 border-b dark:border-surface-border border-lsurface-border dark:bg-surface-raised bg-lsurface-raised shrink-0">
          {/* Mobile hamburger */}
          <button onClick={() => setSidebarOpen(true)}
            className="md:hidden p-1.5 rounded-lg dark:text-neutral-400 text-neutral-500 dark:hover:bg-surface-hover hover:bg-lsurface-hover">
            <MessageSquare size={15} />
          </button>
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-600 to-brand-500 flex items-center justify-center shrink-0">
            <Bot size={16} className="text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold dark:text-neutral-100 text-neutral-900">AI Technical Assistant</p>
            <p className="text-xs dark:text-neutral-500 text-neutral-400 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse inline-block" />
              Ready for coding, system design, and interview Q&A
            </p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-5 py-5 space-y-5">
          {loadingMessages && activeSessionId ? (
            <div className="flex justify-center py-12"><Spinner size="md" /></div>
          ) : showEmpty ? (
            /* Welcome / quick prompts */
            <div className="h-full flex flex-col items-center justify-center text-center max-w-lg mx-auto py-8">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 to-brand-500 flex items-center justify-center mb-5 shadow-xl shadow-purple-500/20">
                <Bot size={28} className="text-white" />
              </div>
              <h3 className="text-lg font-bold dark:text-neutral-100 text-neutral-900 mb-2">How can I help you today?</h3>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 mb-8 leading-relaxed">
                Ask about coding problems, system design, or mock behavioral questions.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
                {QUICK_PROMPTS.map((qp, i) => (
                  <button key={i} onClick={() => doSend(qp.prompt)}
                    className="group p-4 rounded-xl border dark:border-surface-border border-lsurface-border dark:bg-surface-raised bg-lsurface-raised hover:border-brand-500/40 hover:dark:bg-surface-hover hover:bg-lsurface-hover transition-all text-left">
                    <div className="flex items-center gap-2 mb-2">
                      <qp.icon size={14} className="text-brand-500 group-hover:scale-110 transition-transform" />
                      <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900">{qp.label}</span>
                    </div>
                    <p className="text-xs dark:text-neutral-500 text-neutral-400 line-clamp-2 leading-snug">
                      {qp.prompt}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            displayMessages.map((m, i) => {
              const isUser = m.role === 'user'
              const mid = `msg-${m.id ?? i}`
              const isLatestAi = !isUser && i === displayMessages.length - 1 && !optimisticMessage
              return (
                <motion.div key={mid} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={cn('flex items-start gap-3 max-w-3xl', isUser ? 'ml-auto flex-row-reverse' : '')}>
                  {/* Avatar */}
                  <div className={cn(
                    'w-7 h-7 rounded-xl flex items-center justify-center shrink-0 text-white',
                    isUser ? 'bg-brand-500' : 'bg-gradient-to-br from-purple-600 to-brand-500'
                  )}>
                    {isUser ? <User size={13} /> : <Bot size={13} />}
                  </div>
                  {/* Bubble */}
                  <div className={cn(
                    'group relative rounded-2xl px-4 py-3 text-xs leading-relaxed border max-w-[85%]',
                    isUser
                      ? 'dark:bg-brand-500/10 bg-brand-50 dark:border-brand-500/25 border-brand-200 dark:text-neutral-100 text-neutral-900 rounded-tr-sm'
                      : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-200 text-neutral-800 rounded-tl-sm shadow-sm',
                    m.id === 'opt' && 'opacity-70'
                  )}>
                    {isLatestAi ? <TypewriterText text={m.content as string} /> : <p className="whitespace-pre-wrap">{m.content}</p>}
                    {!isUser && (
                      <div className="flex gap-3 mt-2.5 pt-2 border-t dark:border-surface-border border-lsurface-border text-xs dark:text-neutral-500 text-neutral-400">
                        <button onClick={() => copy(m.content, mid)}
                          className="flex items-center gap-1 hover:text-brand-500 transition-colors">
                          {copiedId === mid ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />}
                          {copiedId === mid ? 'Copied' : 'Copy'}
                        </button>
                        <button onClick={() => speak(m.content)}
                          className="flex items-center gap-1 hover:text-brand-500 transition-colors">
                          <Volume2 size={11} /> Read
                        </button>
                      </div>
                    )}
                  </div>
                </motion.div>
              )
            })
          )}

          {/* Typing indicator */}
          {sendingMsg && (
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              className="flex items-start gap-3">
              <div className="w-7 h-7 rounded-xl bg-gradient-to-br from-purple-600 to-brand-500 flex items-center justify-center text-white shrink-0">
                <Bot size={13} />
              </div>
              <div className="rounded-2xl rounded-tl-sm px-4 py-3 dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                <div className="flex items-center gap-1.5">
                  {[0, 0.2, 0.4].map(d => (
                    <motion.span key={d} animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1, delay: d, repeat: Infinity }}
                      className="w-1.5 h-1.5 rounded-full bg-brand-500 inline-block" />
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="shrink-0 px-4 py-3 border-t dark:border-surface-border border-lsurface-border dark:bg-surface-raised bg-lsurface-raised">
          <div className="flex items-end gap-2">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={e => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything… (Enter to send, Shift+Enter for new line)"
              rows={2}
              disabled={sendingMsg}
              className="flex-1 dark:bg-surface-base bg-lsurface-base border dark:border-surface-border border-lsurface-border focus:border-brand-500 rounded-xl px-4 py-2.5 text-xs dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-500 placeholder:text-neutral-400 resize-none focus:outline-none focus:ring-2 focus:ring-brand-500/20 disabled:opacity-60 transition-all"
            />
            <div className="flex flex-col gap-2 shrink-0">
              <button onClick={toggleVoice}
                className={cn(
                  'p-2 rounded-xl transition-all',
                  isListening ? 'bg-red-500 text-white animate-pulse' : 'dark:text-neutral-400 text-neutral-500 dark:hover:bg-surface-hover hover:bg-lsurface-hover'
                )}>
                {isListening ? <MicOff size={15} /> : <Mic size={15} />}
              </button>
              <button
                onClick={() => doSend(inputMessage)}
                disabled={!inputMessage.trim() || sendingMsg}
                className="p-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              >
                <Send size={15} />
              </button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}

// ── SessionList sub-component ──────────────────────────────────────────────
const SessionList = ({
  sessions, loadingSessions, activeSessionId, onSelect, onDelete,
}: {
  sessions: import('@/types').ChatSession[] | undefined
  loadingSessions: boolean
  activeSessionId: number | null
  onSelect: (id: number) => void
  onDelete: (e: React.MouseEvent, id: number) => void
}) => (
  <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
    {loadingSessions ? (
      <div className="flex justify-center py-8"><Spinner size="sm" /></div>
    ) : !sessions || sessions.length === 0 ? (
      <EmptyState icon={<MessageSquare size={22} />} title="No chats yet"
        description="Create a new chat to get started." className="py-8 px-4" />
    ) : (
      sessions.map(s => (
        <div key={s.id} onClick={() => onSelect(s.id)}
          className={cn(
            'group flex items-center justify-between gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-all',
            s.id === activeSessionId
              ? 'dark:bg-brand-500/10 bg-brand-50 dark:text-neutral-100 text-brand-700 border dark:border-brand-500/25 border-brand-200'
              : 'dark:text-neutral-300 text-neutral-600 dark:hover:bg-surface-hover hover:bg-lsurface-hover'
          )}>
          <div className="flex items-center gap-2 min-w-0">
            <MessageSquare size={13} className={s.id === activeSessionId ? 'text-brand-500 shrink-0' : 'shrink-0 opacity-50'} />
            <span className="text-xs font-semibold truncate">{s.title || 'Untitled Chat'}</span>
          </div>
          <button onClick={e => onDelete(e, s.id)}
            className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 transition-all shrink-0"
            title="Delete">
            <Trash2 size={12} />
          </button>
        </div>
      ))
    )}
  </div>
)
