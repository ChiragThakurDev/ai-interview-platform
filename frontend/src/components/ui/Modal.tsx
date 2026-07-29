import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
import { cn } from '@/utils'

interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  description?: string
  children: React.ReactNode
  className?: string
  size?: 'sm' | 'md' | 'lg'
}

const maxWidths = { sm: 'max-w-sm', md: 'max-w-md', lg: 'max-w-2xl' }

export const Modal = ({ open, onClose, title, description, children, className, size = 'md' }: ModalProps) => {
  useEffect(() => {
    if (!open) return
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', h)
    document.body.style.overflow = 'hidden'
    return () => { document.removeEventListener('keydown', h); document.body.style.overflow = '' }
  }, [open, onClose])

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="absolute inset-0 bg-black/70"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: 8 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
            className={cn(
              'relative z-10 w-full rounded-lg border shadow-xl',
              'dark:bg-surface-card dark:border-surface-border',
              'bg-white border-lsurface-border',
              maxWidths[size],
              className
            )}
          >
            {title && (
              <div className="flex items-start justify-between px-5 py-4 border-b dark:border-surface-border border-lsurface-border">
                <div>
                  <h2 className="text-sm font-semibold dark:text-neutral-100 text-neutral-900">{title}</h2>
                  {description && <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-0.5">{description}</p>}
                </div>
                <button
                  onClick={onClose}
                  className="p-1 ml-3 rounded dark:text-neutral-500 text-neutral-400 dark:hover:text-neutral-200 hover:text-neutral-700 dark:hover:bg-surface-raised hover:bg-neutral-100 transition-all"
                  aria-label="Close"
                >
                  <X size={15} />
                </button>
              </div>
            )}
            <div className={cn('px-5 pb-5', title ? 'pt-4' : 'pt-5')}>{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
