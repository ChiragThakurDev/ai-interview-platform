import { forwardRef } from 'react'
import { cn } from '@/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'
  size?: 'xs' | 'sm' | 'md' | 'lg'
  loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, disabled, children, ...props }, ref) => {
    const base = [
      'inline-flex items-center justify-center gap-1.5 font-medium rounded-md',
      'transition-all duration-150 ease-out',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-1',
      'dark:focus-visible:ring-offset-surface-base focus-visible:ring-offset-lsurface-base',
      'disabled:opacity-40 disabled:cursor-not-allowed',
      'active:scale-[0.98] select-none whitespace-nowrap',
    ].join(' ')

    const variants = {
      primary:   'bg-brand-500 hover:bg-brand-400 text-white dark:text-neutral-950 font-semibold',
      secondary: 'dark:bg-surface-raised dark:hover:bg-surface-muted dark:text-neutral-200 dark:border-surface-border bg-lsurface-raised hover:bg-lsurface-hover text-neutral-800 border border-lsurface-border',
      ghost:     'bg-transparent dark:hover:bg-surface-raised hover:bg-lsurface-raised dark:text-neutral-400 dark:hover:text-neutral-100 text-neutral-600 hover:text-neutral-900',
      danger:    'bg-red-600 hover:bg-red-500 text-white',
      outline:   'border dark:border-surface-border border-lsurface-border bg-transparent dark:hover:bg-surface-raised hover:bg-lsurface-raised dark:text-neutral-300 text-neutral-700',
    }

    const sizes = {
      xs: 'h-6  px-2   text-xs  rounded',
      sm: 'h-7  px-2.5 text-xs  rounded',
      md: 'h-8  px-3   text-sm  rounded-md',
      lg: 'h-10 px-4   text-sm  rounded-md font-semibold',
    }

    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], className)}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg className="animate-spin h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        )}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
