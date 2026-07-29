import { cn } from '@/utils'

interface SpinnerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg'
  className?: string
}

const sizes = { xs: 'h-3 w-3', sm: 'h-4 w-4', md: 'h-6 w-6', lg: 'h-10 w-10' }

export const Spinner = ({ size = 'md', className }: SpinnerProps) => (
  <svg
    className={cn('animate-spin text-brand-500', sizes[size], className)}
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle className="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
    <path className="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
  </svg>
)

export const PageLoader = () => (
  <div className="flex flex-col items-center justify-center min-h-screen dark:bg-surface-base bg-lsurface-base gap-3">
    <Spinner size="lg" />
    <p className="text-sm dark:text-neutral-500 text-neutral-400">Loading…</p>
  </div>
)
