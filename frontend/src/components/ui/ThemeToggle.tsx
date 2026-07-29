import { Sun, Moon } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useThemeStore } from '@/store'
import { cn } from '@/utils'

interface ThemeToggleProps { className?: string }

export const ThemeToggle = ({ className }: ThemeToggleProps) => {
  const { theme, toggleTheme } = useThemeStore()
  const isDark = theme === 'dark'

  return (
    <button
      onClick={toggleTheme}
      aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      className={cn(
        'relative flex items-center justify-center w-8 h-8 rounded-md transition-all duration-150',
        'dark:text-neutral-400 dark:hover:text-neutral-100 dark:hover:bg-surface-raised',
        'text-neutral-500 hover:text-neutral-800 hover:bg-lsurface-raised',
        'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-brand-500',
        className
      )}
    >
      <AnimatePresence mode="wait">
        {isDark ? (
          <motion.span
            key="moon"
            initial={{ opacity: 0, rotate: -20, scale: 0.8 }}
            animate={{ opacity: 1, rotate: 0,  scale: 1 }}
            exit={{   opacity: 0, rotate:  20, scale: 0.8 }}
            transition={{ duration: 0.15 }}
          >
            <Moon size={15} />
          </motion.span>
        ) : (
          <motion.span
            key="sun"
            initial={{ opacity: 0, rotate: 20,  scale: 0.8 }}
            animate={{ opacity: 1, rotate: 0,   scale: 1 }}
            exit={{   opacity: 0, rotate: -20,  scale: 0.8 }}
            transition={{ duration: 0.15 }}
          >
            <Sun size={15} />
          </motion.span>
        )}
      </AnimatePresence>
    </button>
  )
}
