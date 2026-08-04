import { Mic, MicOff, Video, VideoOff, PhoneOff } from 'lucide-react'
import { cn } from '@/utils'

interface InterviewControlsProps {
  micEnabled: boolean
  cameraEnabled: boolean
  onToggleMic: () => void
  onToggleCamera: () => void
  onLeave: () => void
  disabled?: boolean
}

interface ControlButtonProps {
  onClick: () => void
  active: boolean
  activeClass: string
  inactiveClass: string
  icon: React.ReactNode
  inactiveIcon: React.ReactNode
  label: string
  disabled?: boolean
}

const ControlButton = ({
  onClick,
  active,
  activeClass,
  inactiveClass,
  icon,
  inactiveIcon,
  label,
  disabled,
}: ControlButtonProps) => (
  <button
    onClick={onClick}
    disabled={disabled}
    aria-label={label}
    title={label}
    className={cn(
      'flex flex-col items-center gap-1.5 px-4 py-2.5 rounded-2xl',
      'transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500',
      'disabled:opacity-40 disabled:cursor-not-allowed',
      active ? activeClass : inactiveClass
    )}
  >
    {active ? icon : inactiveIcon}
    <span className="text-[10px] font-semibold leading-none select-none">
      {label}
    </span>
  </button>
)

export const InterviewControls = ({
  micEnabled,
  cameraEnabled,
  onToggleMic,
  onToggleCamera,
  onLeave,
  disabled = false,
}: InterviewControlsProps) => {
  return (
    <div className="flex items-center justify-center gap-3 px-6 py-4 rounded-2xl border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card shadow-lg">
      {/* Microphone */}
      <ControlButton
        onClick={onToggleMic}
        active={micEnabled}
        activeClass="dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-200 text-neutral-800 dark:hover:bg-surface-hover hover:bg-lsurface-hover"
        inactiveClass="bg-red-500/15 text-red-400 hover:bg-red-500/25 border border-red-500/30"
        icon={<Mic size={20} />}
        inactiveIcon={<MicOff size={20} />}
        label={micEnabled ? 'Mute' : 'Unmute'}
        disabled={disabled}
      />

      {/* Camera */}
      <ControlButton
        onClick={onToggleCamera}
        active={cameraEnabled}
        activeClass="dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-200 text-neutral-800 dark:hover:bg-surface-hover hover:bg-lsurface-hover"
        inactiveClass="bg-red-500/15 text-red-400 hover:bg-red-500/25 border border-red-500/30"
        icon={<Video size={20} />}
        inactiveIcon={<VideoOff size={20} />}
        label={cameraEnabled ? 'Stop Video' : 'Start Video'}
        disabled={disabled}
      />

      {/* Divider */}
      <div className="w-px h-10 dark:bg-surface-border bg-lsurface-border mx-1" />

      {/* Leave */}
      <button
        onClick={onLeave}
        disabled={disabled}
        aria-label="Leave interview"
        title="Leave interview"
        className={cn(
          'flex flex-col items-center gap-1.5 px-5 py-2.5 rounded-2xl',
          'bg-red-600 hover:bg-red-700 text-white',
          'transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500',
          'disabled:opacity-40 disabled:cursor-not-allowed'
        )}
      >
        <PhoneOff size={20} />
        <span className="text-[10px] font-semibold leading-none select-none">Leave</span>
      </button>
    </div>
  )
}
