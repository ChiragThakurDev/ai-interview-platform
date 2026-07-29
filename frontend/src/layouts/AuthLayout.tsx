import { Outlet, Navigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap, CheckCircle } from 'lucide-react'
import { useAuthStore } from '@/store'
import { ThemeToggle } from '@/components/ui'

const FEATURES = [
  'AI-generated questions tailored to your resume and target role',
  'Real-time evaluation with score and detailed feedback per answer',
  'Full Monaco IDE with code execution for coding interviews',
  'Performance dashboard, leaderboard, and skill gap reports',
]

export const AuthLayout = () => {
  const { isAuthenticated } = useAuthStore()
  if (isAuthenticated) return <Navigate to="/dashboard" replace />

  return (
    <div className="min-h-screen dark:bg-surface-base bg-lsurface-base flex">
      {/* Theme toggle */}
      <div className="absolute top-4 right-4 z-20">
        <ThemeToggle />
      </div>

      {/* Left panel */}
      <div className="hidden lg:flex flex-col justify-between w-[45%] p-12 dark:bg-surface-card bg-white dark:border-surface-border border-lsurface-border border-r">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
            <Zap size={16} className="text-white" />
          </div>
          <span className="text-base font-bold dark:text-neutral-100 text-neutral-900">AI Interview Platform</span>
        </div>

        {/* Copy */}
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold dark:text-neutral-50 text-neutral-900 leading-tight mb-3">
              Practice. Improve.<br />
              <span className="text-brand-500">Get Hired.</span>
            </h1>
            <p className="dark:text-neutral-400 text-neutral-600 text-sm leading-relaxed">
              The AI-powered interview simulator that prepares you for real technical interviews at top companies.
            </p>
          </div>

          <ul className="space-y-3">
            {FEATURES.map(f => (
              <li key={f} className="flex items-start gap-2.5 text-sm dark:text-neutral-300 text-neutral-700">
                <CheckCircle size={15} className="text-brand-500 shrink-0 mt-0.5" />
                {f}
              </li>
            ))}
          </ul>
        </div>

        <p className="text-xs dark:text-neutral-600 text-neutral-400">
          © {new Date().getFullYear()} AI Interview Platform
        </p>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="w-full max-w-sm"
        >
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-8 lg:hidden">
            <div className="w-7 h-7 rounded-md bg-brand-500 flex items-center justify-center">
              <Zap size={14} className="text-white" />
            </div>
            <span className="text-sm font-bold dark:text-neutral-100 text-neutral-900">AI Interview Platform</span>
          </div>

          <Outlet />
        </motion.div>
      </div>
    </div>
  )
}
