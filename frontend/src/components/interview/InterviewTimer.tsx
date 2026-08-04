import { useState, useEffect, useRef } from 'react'
import { Clock } from 'lucide-react'
import { cn } from '@/utils'

interface InterviewTimerProps {
  /** If true the timer runs; if false it pauses */
  running: boolean
  className?: string
}

export const InterviewTimer = ({ running, className }: InterviewTimerProps) => {
  const [elapsed, setElapsed] = useState(0) // seconds
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => {
        setElapsed((prev) => prev + 1)
      }, 1000)
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [running])

  const hh = String(Math.floor(elapsed / 3600)).padStart(2, '0')
  const mm = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0')
  const ss = String(elapsed % 60).padStart(2, '0')

  return (
    <div
      className={cn(
        'flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold border',
        'dark:bg-surface-raised bg-lsurface-raised',
        'dark:border-surface-border border-lsurface-border',
        'dark:text-neutral-300 text-neutral-700',
        className
      )}
      aria-label="Interview elapsed time"
    >
      <Clock size={13} className="shrink-0" />
      <span className="tabular-nums tracking-widest">
        {hh}:{mm}:{ss}
      </span>
    </div>
  )
}
