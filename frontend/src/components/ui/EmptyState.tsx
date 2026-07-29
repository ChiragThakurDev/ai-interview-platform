import { cn } from '@/utils'

interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
  className?: string
}

export const EmptyState = ({ icon, title, description, action, className }: EmptyStateProps) => (
  <div className={cn('flex flex-col items-center justify-center py-12 text-center', className)}>
    {icon && (
      <div className="mb-3 dark:text-neutral-600 text-neutral-400">{icon}</div>
    )}
    <p className="text-sm font-medium dark:text-neutral-300 text-neutral-700 mb-1">{title}</p>
    {description && (
      <p className="text-xs dark:text-neutral-500 text-neutral-500 max-w-xs mb-4 leading-relaxed">{description}</p>
    )}
    {action}
  </div>
)
