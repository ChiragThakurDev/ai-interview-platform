import { useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, FileText, Brain, Code2, Trophy,
  History, User, Settings, MessageSquare, X, Zap, Shield, Key, Video,
} from 'lucide-react'
import { cn } from '@/utils'
import { useAuthStore } from '@/store'
import { useActiveSession } from '@/hooks/useActiveSession'
import { LeaveSessionModal } from '@/components/ui/LeaveSessionModal'

const NAV = [
  { to: '/dashboard',   icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/resume',      icon: FileText,         label: 'Resume' },
  { to: '/interview',   icon: Brain,             label: 'Technical Interview' },
  { to: '/coding',      icon: Code2,             label: 'Coding Interview' },
  { to: '/video-room',  icon: Video,             label: 'Video Interview' },
  { to: '/leaderboard', icon: Trophy,            label: 'Leaderboard' },
  { to: '/history',     icon: History,           label: 'History' },
  { to: '/chat',        icon: MessageSquare,     label: 'AI Assistant' },
]

const BOTTOM = [
  { to: '/profile',          icon: User,     label: 'Profile' },
  { to: '/settings',         icon: Settings, label: 'Settings' },
  { to: '/settings/api-keys',icon: Key,      label: 'API Keys' },
]

// ── NavItem — intercepts clicks when a session is active ─────────────────────
const NavItem = ({
  to, icon: Icon, label, onClick,
}: {
  to: string; icon: React.ElementType; label: string; onClick?: () => void
}) => {
  const location = useLocation()
  const isActive = location.pathname === to ||
    (to !== '/dashboard' && location.pathname.startsWith(to + '/')) ||
    (to !== '/dashboard' && location.pathname === to)

  return (
    <button
      onClick={onClick}
      className={cn(
        'w-full relative flex items-center gap-2.5 px-3 py-2 rounded text-xs font-medium transition-all duration-150 text-left',
        isActive
          ? 'dark:bg-surface-hover bg-lsurface-hover dark:text-neutral-50 text-neutral-900 nav-active-bar'
          : 'dark:text-neutral-400 text-neutral-600 dark:hover:bg-surface-raised dark:hover:text-neutral-200 hover:bg-lsurface-raised hover:text-neutral-800',
      )}
    >
      <Icon size={15} className={cn('shrink-0', isActive ? 'text-brand-500' : 'opacity-70')} />
      <span>{label}</span>
    </button>
  )
}

const Content = ({ onClose }: { onClose: () => void }) => {
  const { user }    = useAuthStore()
  const navigate    = useNavigate()
  const location    = useLocation()
  const isAdmin     = user?.role === 'admin'
  const { activeSession, confirmNavAway, pendingNav, confirmLeave, cancelLeave } = useActiveSession()

  const handleNav = (to: string) => {
    if (window.innerWidth < 1024) onClose()
    confirmNavAway(to, () => navigate(to))
  }

  return (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-4 py-4 border-b dark:border-surface-border border-lsurface-border">
        <div className="w-7 h-7 rounded-md bg-brand-500 flex items-center justify-center shrink-0">
          <Zap size={14} className="text-white" />
        </div>
        <div>
          <p className="text-sm font-bold dark:text-neutral-50 text-neutral-900 leading-none">AI Interview</p>
          <p className="text-2xs dark:text-neutral-500 text-neutral-500 mt-0.5">Practice Platform</p>
        </div>
        <button
          onClick={onClose}
          className="ml-auto lg:hidden p-1 dark:text-neutral-500 text-neutral-400 dark:hover:text-neutral-200 hover:text-neutral-700 transition-colors"
          aria-label="Close"
        >
          <X size={15} />
        </button>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-y-auto">
        {NAV.map(item => (
          <NavItem key={item.to} {...item} onClick={() => handleNav(item.to)} />
        ))}

        {/* Admin section — only visible to admins */}
        {isAdmin && (
          <div className="pt-3">
            <p className="px-3 text-2xs font-bold dark:text-neutral-600 text-neutral-400 uppercase tracking-widest mb-1">
              Admin
            </p>
            <button
              onClick={() => handleNav('/admin')}
              className={cn(
                'w-full relative flex items-center gap-2.5 px-3 py-2 rounded text-xs font-medium transition-all duration-150 text-left',
                location.pathname === '/admin'
                  ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                  : 'dark:text-neutral-400 text-neutral-600 dark:hover:bg-surface-raised dark:hover:text-neutral-200 hover:bg-lsurface-raised hover:text-neutral-800',
              )}
            >
              <Shield size={15} className={cn('shrink-0', location.pathname === '/admin' ? 'text-red-400' : 'opacity-70')} />
              <span>Admin Panel</span>
            </button>
          </div>
        )}
      </nav>

      {/* Bottom */}
      <div className="px-2 py-3 space-y-0.5 border-t dark:border-surface-border border-lsurface-border">
        {BOTTOM.map(item => (
          <NavItem key={item.to} {...item} onClick={() => handleNav(item.to)} />
        ))}
      </div>

      {/* Leave-session confirmation modal */}
      <LeaveSessionModal
        open={!!pendingNav}
        sessionLabel={activeSession?.label ?? 'Session'}
        onConfirm={confirmLeave}
        onCancel={cancelLeave}
      />
    </div>
  )
}

export const Sidebar = ({ open, onClose }: { open: boolean; onClose: () => void }) => (
  <>
    {/* Desktop */}
    <aside className="hidden lg:flex flex-col w-56 h-screen sticky top-0 shrink-0 dark:bg-surface-card dark:border-surface-border bg-lsurface-card border-lsurface-border border-r">
      <Content onClose={onClose} />
    </aside>

    {/* Mobile */}
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/60 lg:hidden"
            onClick={onClose}
          />
          <motion.aside
            initial={{ x: -240 }} animate={{ x: 0 }} exit={{ x: -240 }}
            transition={{ type: 'tween', duration: 0.2 }}
            className="fixed inset-y-0 left-0 z-50 w-56 lg:hidden dark:bg-surface-card dark:border-surface-border bg-white border-r border-lsurface-border"
          >
            <Content onClose={onClose} />
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  </>
)
