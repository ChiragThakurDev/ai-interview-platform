import { useState, useEffect, useCallback, createContext, useContext, forwardRef } from 'react'
import { createPortal } from 'react-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react'
import { cn } from '@/utils'

type ToastType = 'success' | 'error' | 'warning' | 'info'
interface ToastItem { id: string; type: ToastType; message: string; duration?: number }
interface ToastCtx  { add: (type: ToastType, message: string, duration?: number) => void }

const ToastContext = createContext<ToastCtx>({ add: () => {} })

const ICONS: Record<ToastType, React.ReactNode> = {
  success: <CheckCircle size={14} className="text-green-400 shrink-0" />,
  error:   <XCircle     size={14} className="text-red-400   shrink-0" />,
  warning: <AlertCircle size={14} className="text-yellow-400 shrink-0" />,
  info:    <Info        size={14} className="text-blue-400  shrink-0" />,
}

const BORDERS: Record<ToastType, string> = {
  success: 'border-l-green-500',
  error:   'border-l-red-500',
  warning: 'border-l-yellow-500',
  info:    'border-l-blue-500',
}

const ToastItemComponent = forwardRef<HTMLDivElement, { toast: ToastItem; onDismiss: (id: string) => void }>(
  ({ toast, onDismiss }, ref) => {
    useEffect(() => {
      const t = setTimeout(() => onDismiss(toast.id), toast.duration ?? 4000)
      return () => clearTimeout(t)
    }, [toast, onDismiss])

    return (
      <motion.div
        ref={ref}
        layout
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        exit={  { opacity: 0, x: 40 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className={cn(
          'flex items-start gap-2.5 px-3.5 py-3 rounded-md border border-l-2 shadow-lg pointer-events-auto',
          'dark:bg-surface-card dark:border-surface-border bg-white border-neutral-200',
          'max-w-xs w-full',
          BORDERS[toast.type]
        )}
      >
        <span className="mt-px">{ICONS[toast.type]}</span>
        <p className="text-xs dark:text-neutral-200 text-neutral-800 leading-relaxed flex-1">{toast.message}</p>
        <button
          onClick={() => onDismiss(toast.id)}
          className="shrink-0 dark:text-neutral-600 text-neutral-400 dark:hover:text-neutral-300 hover:text-neutral-700 transition-colors ml-1"
        >
          <X size={13} />
        </button>
      </motion.div>
    )
  }
)
ToastItemComponent.displayName = 'ToastItem'

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([])
  const dismiss = useCallback((id: string) => setToasts(p => p.filter(t => t.id !== id)), [])
  const add = useCallback((type: ToastType, message: string, duration = 4000) => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2)}`
    setToasts(p => [...p.slice(-4), { id, type, message, duration }])
  }, [])

  const portal = typeof document !== 'undefined' ? createPortal(
    <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 pointer-events-none">
      <AnimatePresence mode="popLayout">
        {toasts.map(t => <ToastItemComponent key={t.id} toast={t} onDismiss={dismiss} />)}
      </AnimatePresence>
    </div>,
    document.body
  ) : null

  return (
    <ToastContext.Provider value={{ add }}>
      {children}
      {portal}
    </ToastContext.Provider>
  )
}

export const useToast = () => useContext(ToastContext)

let _globalAdd: ToastCtx['add'] | null = null

export const AppToaster = () => {
  const { add } = useToast()
  useEffect(() => { _globalAdd = add }, [add])
  return null
}

interface ShowToastFn {
  (type: ToastType, message: string, duration?: number): void
  success: (msg: string, d?: number) => void
  error:   (msg: string, d?: number) => void
  warning: (msg: string, d?: number) => void
  info:    (msg: string, d?: number) => void
}

export const showToast: ShowToastFn = Object.assign(
  (type: ToastType, message: string, duration?: number) => _globalAdd?.(type, message, duration),
  {
    success: (msg: string, d?: number) => _globalAdd?.('success', msg, d),
    error:   (msg: string, d?: number) => _globalAdd?.('error',   msg, d),
    warning: (msg: string, d?: number) => _globalAdd?.('warning', msg, d),
    info:    (msg: string, d?: number) => _globalAdd?.('info',    msg, d),
  }
)
