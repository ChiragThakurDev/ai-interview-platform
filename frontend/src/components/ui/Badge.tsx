import { cn } from '@/utils'

type Variant = 'default' | 'success' | 'warning' | 'danger' | 'info' | 'orange' | 'purple' | 'primary' | 'secondary'
type Size = 'xs' | 'sm' | 'md'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: Variant
  size?: Size
  dot?: boolean
}

const styles: Record<Variant, string> = {
  default:   'dark:bg-neutral-800 dark:text-neutral-300 dark:border-neutral-700 bg-neutral-100 text-neutral-600 border-neutral-200',
  secondary: 'dark:bg-neutral-800 dark:text-neutral-300 dark:border-neutral-700 bg-neutral-100 text-neutral-600 border-neutral-200',
  success:   'bg-green-500/10 text-green-500 border-green-500/20',
  warning:   'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
  danger:    'bg-red-500/10 text-red-500 border-red-500/20',
  info:      'bg-blue-500/10 text-blue-400 border-blue-500/20',
  orange:    'bg-brand-500/10 text-brand-500 border-brand-500/20',
  primary:   'bg-brand-500/10 text-brand-500 border-brand-500/20',
  purple:    'bg-purple-500/10 text-purple-400 border-purple-500/20',
}

const dots: Record<Variant, string> = {
  default: 'bg-neutral-400', secondary: 'bg-neutral-400',
  success: 'bg-green-400',   warning: 'bg-yellow-400',
  danger:  'bg-red-400',     info: 'bg-blue-400',
  orange:  'bg-brand-500',   primary: 'bg-brand-500',
  purple:  'bg-purple-400',
}

const sizes: Record<Size, string> = {
  xs: 'px-1.5 py-0.5 text-2xs',
  sm: 'px-2   py-0.5 text-xs',
  md: 'px-2.5 py-1   text-sm',
}

export const Badge = ({ className, variant = 'default', size = 'sm', dot, children, ...props }: BadgeProps) => (
  <span
    className={cn(
      'inline-flex items-center gap-1.5 rounded-full border font-medium',
      styles[variant], sizes[size], className
    )}
    {...props}
  >
    {dot && <span className={cn('w-1.5 h-1.5 rounded-full shrink-0 animate-pulse-dot', dots[variant])} />}
    {children}
  </span>
)
