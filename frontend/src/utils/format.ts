export const formatDate = (d: string | null | undefined) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

export const formatDateTime = (d: string | null | undefined) => {
  if (!d) return '—'
  return new Date(d).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

export const formatDuration = (s: number | null | undefined) => {
  if (!s) return '—'
  return `${Math.floor(s / 60)}m ${s % 60}s`
}

export const formatScore = (s: number | null | undefined) => s == null ? '—' : `${s}/100`

export const scoreColor = (s: number | null | undefined) => {
  if (s == null) return 'dark:text-neutral-500 text-neutral-400'
  if (s >= 80)   return 'text-green-400'
  if (s >= 60)   return 'text-yellow-500'
  return 'text-red-400'
}

export const difficultyColor = (d: string) => {
  switch (d?.toLowerCase()) {
    case 'easy':   return 'text-green-400 bg-green-500/10'
    case 'medium': return 'text-yellow-500 bg-yellow-500/10'
    case 'hard':   return 'text-red-400 bg-red-500/10'
    default:       return 'dark:text-neutral-500 dark:bg-surface-raised text-neutral-500 bg-lsurface-raised'
  }
}

export const statusColor = (s: string) => {
  switch (s?.toLowerCase()) {
    case 'completed': return 'text-green-400 bg-green-500/10'
    case 'running':   return 'text-blue-400 bg-blue-500/10'
    case 'pending':   return 'text-yellow-500 bg-yellow-500/10'
    default:          return 'dark:text-neutral-500 dark:bg-surface-raised text-neutral-500 bg-lsurface-raised'
  }
}

export const fileSizeLabel = (b: number) => {
  if (b < 1024)         return `${b} B`
  if (b < 1024 * 1024)  return `${(b / 1024).toFixed(1)} KB`
  return `${(b / (1024 * 1024)).toFixed(1)} MB`
}


