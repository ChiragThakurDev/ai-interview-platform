import { forwardRef } from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/utils'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: { value: string; label: string }[]
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, options, id, ...props }, ref) => {
    const selectId = id ?? label?.toLowerCase().replace(/\s+/g, '-')

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label htmlFor={selectId} className="text-xs font-medium dark:text-neutral-300 text-neutral-700">
            {label}
          </label>
        )}
        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            className={cn(
              'w-full rounded-md border py-2 pl-3 pr-8 text-sm appearance-none cursor-pointer',
              'dark:bg-surface-raised dark:text-neutral-100 dark:border-surface-border',
              'bg-white text-neutral-900 border-lsurface-border',
              'transition-all duration-150',
              'focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500',
              'dark:hover:border-neutral-500 hover:border-neutral-400',
              error ? 'border-red-500' : '',
              className
            )}
            {...props}
          >
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}
                className="dark:bg-surface-card bg-white">
                {opt.label}
              </option>
            ))}
          </select>
          <ChevronDown
            size={13}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 dark:text-neutral-500 text-neutral-400 pointer-events-none"
          />
        </div>
        {error && <p className="text-xs text-red-400">{error}</p>}
      </div>
    )
  }
)

Select.displayName = 'Select'
