import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, ArrowLeft, LogOut } from 'lucide-react'
import { Button } from './Button'

interface LeaveSessionModalProps {
  open:        boolean
  sessionLabel: string
  onConfirm:   () => void
  onCancel:    () => void
}

export const LeaveSessionModal = ({
  open, sessionLabel, onConfirm, onCancel,
}: LeaveSessionModalProps) => (
  <AnimatePresence>
    {open && (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[9998] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
        onClick={onCancel}
      >
        <motion.div
          initial={{ scale: 0.92, y: 16 }}
          animate={{ scale: 1, y: 0 }}
          exit={{ scale: 0.92, y: 8 }}
          onClick={e => e.stopPropagation()}
          className="w-full max-w-sm dark:bg-surface-card bg-white rounded-2xl border dark:border-surface-border border-lsurface-border shadow-xl p-6 space-y-5"
        >
          {/* Icon + title */}
          <div className="flex flex-col items-center gap-3 text-center">
            <div className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
              <AlertTriangle size={28} />
            </div>
            <h3 className="text-base font-bold dark:text-neutral-100 text-neutral-900">
              Leave Active Session?
            </h3>
            <p className="text-xs dark:text-neutral-400 text-neutral-500 leading-relaxed">
              You have an active <span className="font-semibold dark:text-neutral-200 text-neutral-700">{sessionLabel}</span> in progress.
              Navigating away will <span className="text-amber-400 font-semibold">not end your session</span> — you can return to it via History or the sidebar.
            </p>
          </div>

          {/* Actions */}
          <div className="flex flex-col gap-2">
            <Button
              variant="secondary"
              size="md"
              className="w-full"
              onClick={onCancel}
              icon={<ArrowLeft size={14} />}
            >
              Stay in Session
            </Button>
            <Button
              variant="danger"
              size="md"
              className="w-full"
              onClick={onConfirm}
              icon={<LogOut size={14} />}
            >
              Leave Anyway
            </Button>
          </div>
        </motion.div>
      </motion.div>
    )}
  </AnimatePresence>
)
