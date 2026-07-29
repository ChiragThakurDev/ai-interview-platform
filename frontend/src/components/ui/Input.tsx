import { forwardRef, useState } from 'react'
import { cn } from '@/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, id, leftIcon, rightIcon, ...props }, ref) => {
    const [focused, setFocused] = useState(false)
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-')

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-medium dark:text-neutral-300 text-neutral-700"
          >
            {label}
          </label>
        )}

        <div
          className={cn(
            'relative flex items-center rounded-md border transition-all duration-150',
            'dark:bg-surface-raised bg-white',
            focused
              ? 'border-brand-500 ring-1 ring-brand-500/40'
              : error
                ? 'border-red-500 ring-1 ring-red-500/20'
                : 'dark:border-surface-border border-lsurface-border dark:hover:border-neutral-500 hover:border-neutral-400',
          )}
        >
          {leftIcon && (
            <span className="pl-2.5 dark:text-neutral-500 text-neutral-400 shrink-0 text-xs">
              {leftIcon}
            </span>
          )}
          <input
            ref={ref}
            id={inputId}
            onFocus={(e) => { setFocused(true); props.onFocus?.(e) }}
            onBlur={(e)  => { setFocused(false); props.onBlur?.(e) }}
            className={cn(
              'flex-1 bg-transparent py-2 text-sm',
              leftIcon ? 'pl-1.5 pr-3' : 'px-3',
              rightIcon && 'pr-1',
              'dark:text-neutral-100 text-neutral-900',
              'dark:placeholder-neutral-600 placeholder-neutral-400',
              'focus:outline-none',
              className
            )}
            {...props}
          />
          {rightIcon && (
            <span className="pr-2.5 dark:text-neutral-500 text-neutral-400 shrink-0">
              {rightIcon}
            </span>
          )}
        </div>

        {hint && !error && <p className="text-xs dark:text-neutral-600 text-neutral-400">{hint}</p>}
        {error          && <p className="text-xs text-red-400">{error}</p>}
      </div>
    )
  }
)

Input.displayName = 'Input'
