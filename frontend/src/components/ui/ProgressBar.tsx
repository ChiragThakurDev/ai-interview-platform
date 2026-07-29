import { motion } from 'framer-motion'
import { cn } from '@/utils'

interface ProgressBarProps {
  value: number
  max?: number
  color?: 'brand' | 'green' | 'yellow' | 'red' | 'blue'
  showLabel?: boolean
  label?: string
  size?: 'xs' | 'sm' | 'md'
  animate?: boolean
  className?: string
}

export const ProgressBar = ({
  value, max = 100, color = 'brand', showLabel, label, size = 'sm', animate = true, className,
}: ProgressBarProps) => {
  const pct = Math.min(100, Math.max(0, Math.round((value / max) * 100)))

  const tracks  = { brand: 'dark:bg-neutral-800 bg-neutral-200', green: 'dark:bg-green-900/30 bg-green-100', yellow: 'dark:bg-yellow-900/30 bg-yellow-100', red: 'dark:bg-red-900/30 bg-red-100', blue: 'dark:bg-blue-900/30 bg-blue-100' }
  const fills   = { brand: 'bg-brand-500', green: 'bg-green-500', yellow: 'bg-yellow-500', red: 'bg-red-500', blue: 'bg-blue-500' }
  const heights = { xs: 'h-1', sm: 'h-1.5', md: 'h-2' }

  return (
    <div className={cn('w-full', className)}>
      {(showLabel || label) && (
        <div className="flex justify-between text-xs dark:text-neutral-500 text-neutral-500 mb-1">
          <span>{label ?? 'Progress'}</span>
          <span className="font-medium dark:text-neutral-300 text-neutral-600">{pct}%</span>
        </div>
      )}
      <div className={cn('w-full rounded-full overflow-hidden', heights[size], tracks[color])}>
        <motion.div
          className={cn('h-full rounded-full', fills[color])}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: animate ? 0.6 : 0, ease: 'easeOut' }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  )
}
