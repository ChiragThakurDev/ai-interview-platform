import { useState, useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, ChevronDown, LogOut, User, Settings } from 'lucide-react'
import { useAuthStore } from '@/store'
import { useLogout } from '@/hooks'
import { ThemeToggle } from '@/components/ui'
import { cn } from '@/utils'

export const Navbar = ({ onMenuClick }: { onMenuClick: () => void }) => {
  const { user } = useAuthStore()
  const { mutate: logout } = useLogout()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const h = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false) }
    document.addEventListener('mousedown', h)
    return () => document.removeEventListener('mousedown', h)
  }, [])

  const initials = user?.name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) ?? '?'

  return (
    <header className="h-12 flex items-center px-4 gap-3 sticky top-0 z-30 dark:bg-surface-card/95 bg-white/95 backdrop-blur-sm dark:border-surface-border border-lsurface-border border-b">
      <button
        onClick={onMenuClick}
        className="lg:hidden p-1.5 rounded dark:text-neutral-400 text-neutral-600 dark:hover:text-neutral-200 dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-all"
        aria-label="Menu"
      >
        <Menu size={17} />
      </button>

      <div className="flex-1" />

      <ThemeToggle />

      <div className="w-px h-4 dark:bg-surface-border bg-lsurface-border" />

      {/* User dropdown */}
      <div className="relative" ref={ref}>
        <button
          onClick={() => setOpen(o => !o)}
          className="flex items-center gap-2 px-1.5 py-1 rounded transition-all dark:hover:bg-surface-raised hover:bg-lsurface-raised"
        >
          <div className="w-6 h-6 rounded-md bg-brand-500 flex items-center justify-center text-2xs font-bold text-white shrink-0">
            {initials}
          </div>
          <span className="hidden sm:block text-xs font-medium dark:text-neutral-300 text-neutral-700 max-w-[100px] truncate">
            {user?.name ?? 'User'}
          </span>
          <ChevronDown size={12} className={cn('dark:text-neutral-500 text-neutral-400 transition-transform', open && 'rotate-180')} />
        </button>

        <AnimatePresence>
          {open && (
            <motion.div
              initial={{ opacity: 0, y: -4, scale: 0.97 }}
              animate={{ opacity: 1, y: 0,  scale: 1 }}
              exit={  { opacity: 0, y: -4, scale: 0.97 }}
              transition={{ duration: 0.12 }}
              className="absolute right-0 top-full mt-1.5 w-48 rounded-lg border shadow-lg z-50 dark:bg-surface-card dark:border-surface-border bg-white border-lsurface-border py-1 overflow-hidden"
            >
              <div className="px-3 py-2 border-b dark:border-surface-border border-lsurface-border">
                <p className="text-xs font-semibold dark:text-neutral-200 text-neutral-800 truncate">{user?.name}</p>
                <p className="text-2xs dark:text-neutral-500 text-neutral-500 truncate">{user?.email}</p>
              </div>
              {[
                { to: '/profile',  icon: User,     label: 'Profile' },
                { to: '/settings', icon: Settings, label: 'Settings' },
              ].map(({ to, icon: Icon, label }) => (
                <Link
                  key={to}
                  to={to}
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-2 px-3 py-2 text-xs dark:text-neutral-300 text-neutral-700 dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-colors"
                >
                  <Icon size={13} className="opacity-70" /> {label}
                </Link>
              ))}
              <div className="border-t dark:border-surface-border border-lsurface-border my-1" />
              <button
                onClick={() => { setOpen(false); logout() }}
                className="w-full flex items-center gap-2 px-3 py-2 text-xs text-red-400 hover:text-red-300 dark:hover:bg-surface-raised hover:bg-red-50 transition-colors"
              >
                <LogOut size={13} /> Logout
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  )
}
