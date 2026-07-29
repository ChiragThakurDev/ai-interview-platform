import { cn } from '@/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean
  noPad?: boolean
}

export const Card = ({ className, hover, noPad, children, ...props }: CardProps) => (
  <div
    className={cn(
      'rounded-lg border transition-all duration-150',
      'dark:bg-surface-card dark:border-surface-border',
      'bg-lsurface-card border-lsurface-border',
      !noPad && 'p-4',
      hover && [
        'cursor-pointer',
        'dark:hover:bg-surface-hover dark:hover:border-neutral-600',
        'hover:bg-lsurface-hover hover:border-neutral-300',
      ],
      className
    )}
    {...props}
  >
    {children}
  </div>
)

export const CardHeader = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('mb-4', className)} {...props}>{children}</div>
)

export const CardTitle = ({ className, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn('text-base font-semibold dark:text-neutral-100 text-neutral-800', className)} {...props}>
    {children}
  </h3>
)
