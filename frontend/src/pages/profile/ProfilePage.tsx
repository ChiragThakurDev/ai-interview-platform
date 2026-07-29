import { motion } from 'framer-motion'
import { User, Mail, Shield, Star, Brain, Code2, Trophy, TrendingUp } from 'lucide-react'
import { useAuthStore } from '@/store'
import { useDashboard } from '@/hooks'
import { Card, Badge, Spinner } from '@/components/ui'

export const ProfilePage = () => {
  const { user } = useAuthStore()
  const { data: dashboard, isLoading } = useDashboard()

  const initials = user?.name
    ?.split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) ?? '?'

  const stats = [
    {
      label: 'Total Sessions',
      value: dashboard?.total_interviews ?? 0,
      icon: Brain,
      gradient: 'from-brand-500 to-indigo-600',
    },
    {
      label: 'Completed',
      value: dashboard?.completed_interviews ?? 0,
      icon: Trophy,
      gradient: 'from-emerald-600 to-teal-500',
    },
    {
      label: 'Average Score',
      value: dashboard?.average_score != null ? `${Math.round(dashboard.average_score)}%` : '—',
      icon: TrendingUp,
      gradient: 'from-amber-500 to-orange-500',
    },
    {
      label: 'Best Score',
      value: dashboard?.best_score ?? '—',
      icon: Star,
      gradient: 'from-purple-600 to-pink-500',
    },
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* Profile Hero Card */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-3xl border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shadow-sm"
      >
        <div className="relative z-10 p-6 sm:p-8 flex flex-col sm:flex-row items-center sm:items-start gap-6">
          {/* Avatar */}
          <div className="relative shrink-0">
            <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-3xl bg-gradient-to-br from-brand-500 via-purple-600 to-indigo-600 flex items-center justify-center text-2xl font-bold text-white ring-4 ring-brand-500/20">
              {initials}
            </div>
            <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-emerald-500 border-2 dark:border-surface-card border-lsurface-card flex items-center justify-center">
              <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
            </div>
          </div>

          {/* Info */}
          <div className="flex-1 text-center sm:text-left space-y-3">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
                {user?.name}
              </h1>
              <div className="flex items-center justify-center sm:justify-start gap-2 mt-1">
                <Badge variant={user?.role === 'admin' ? 'danger' : 'purple'} size="sm" dot>
                  {user?.role === 'admin' ? 'Admin' : 'Candidate'}
                </Badge>
                {user?.is_active && (
                  <Badge variant="success" size="sm">Active</Badge>
                )}
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-3">
              <div className="flex items-center gap-2.5 p-3 rounded-xl dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                <Mail size={15} className="text-brand-500 shrink-0" />
                <div className="min-w-0">
                  <p className="text-[10px] font-semibold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider">Email</p>
                  <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 truncate">{user?.email}</p>
                </div>
              </div>
              <div className="flex items-center gap-2.5 p-3 rounded-xl dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                <Shield size={15} className="text-cyan-400 shrink-0" />
                <div>
                  <p className="text-[10px] font-semibold dark:text-neutral-500 text-neutral-400 uppercase tracking-wider">Platform Role</p>
                  <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 capitalize">{user?.role}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Performance Stats */}
      <div>
        <h2 className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-4 flex items-center gap-2">
          <TrendingUp size={13} className="text-brand-500" />
          Interview Performance Metrics
        </h2>

        {isLoading ? (
          <div className="flex justify-center py-12"><Spinner size="md" /></div>
        ) : (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map(({ label, value, icon: Icon, gradient }, i) => (
              <motion.div
                key={label}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.07 }}
              >
                <Card className="relative overflow-hidden group border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card hover-lift">
                  <div className="relative">
                    <div className={`p-2.5 rounded-xl bg-gradient-to-br ${gradient} text-white w-fit mb-3 shadow-sm group-hover:scale-105 transition-transform`}>
                      <Icon size={16} />
                    </div>
                    <p className="text-2xl font-bold dark:text-neutral-100 text-neutral-900 leading-none">{value}</p>
                    <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold mt-1">{label}</p>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        <h2 className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-4 flex items-center gap-2">
          <User size={13} className="text-brand-500" /> Quick Platform Access
        </h2>
        <div className="grid sm:grid-cols-3 gap-3">
          {[
            { label: 'Start Technical Interview', icon: Brain, to: '/interview', color: 'text-brand-500', bg: 'dark:bg-brand-500/10 bg-brand-500/10 dark:border-brand-500/30 border-brand-500/30' },
            { label: 'Launch Coding Arena', icon: Code2, to: '/coding', color: 'text-amber-500', bg: 'dark:bg-amber-500/10 bg-amber-50 dark:border-amber-500/30 border-amber-200' },
            { label: 'View Leaderboard', icon: Trophy, to: '/leaderboard', color: 'text-orange-400', bg: 'dark:bg-orange-500/10 bg-orange-50 dark:border-orange-500/30 border-orange-200' },
          ].map(({ label, icon: Icon, to, color, bg }) => (
            <a
              key={to}
              href={to}
              className={`flex items-center gap-3 p-3.5 rounded-xl border transition-all group hover:scale-[1.02] ${bg}`}
            >
              <Icon size={16} className={`${color} group-hover:scale-110 transition-transform`} />
              <span className="text-xs font-semibold dark:text-neutral-100 text-neutral-900">{label}</span>
            </a>
          ))}
        </div>
      </Card>
    </div>
  )
}
