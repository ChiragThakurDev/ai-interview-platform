import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Video, Link2, Copy, Check, ArrowRight, Users, Shield,
  Hash, UserCheck, UsersRound, Globe, Lock, Eye, RefreshCw,
  Clock, LogIn, Trash2, AlertTriangle,
} from 'lucide-react'
import { useVideoRoom } from '@/hooks/useVideoRoom'
import { useRoomRegistry } from '@/hooks/useRoomRegistry'
import { useAuthStore } from '@/store'
import { Button, Card, Spinner } from '@/components/ui'
import { roomTypeFromCode, ROOM_MAX } from '@/types/livekit'
import type { RoomType, RoomVisibility, RoomListing } from '@/types/livekit'
import { cn } from '@/utils'

// ── small helpers ─────────────────────────────────────────────────────────────
const Feature = ({ icon: Icon, text }: { icon: React.ElementType; text: string }) => (
  <div className="flex items-center gap-2 text-xs dark:text-neutral-400 text-neutral-500">
    <Icon size={13} className="text-brand-500 shrink-0" />
    <span>{text}</span>
  </div>
)

const RoomTypePill = ({ type }: { type: RoomType }) => (
  <span className={cn(
    'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold border',
    type === 'single'
      ? 'bg-brand-500/10 border-brand-500/25 text-brand-400'
      : 'bg-emerald-500/10 border-emerald-500/25 text-emerald-400',
  )}>
    {type === 'single' ? <UserCheck size={9} /> : <UsersRound size={9} />}
    {type === 'single' ? 'Single · 2 max' : 'Group · 10 max'}
  </span>
)

const VisibilityPill = ({ vis }: { vis: RoomVisibility }) => (
  <span className={cn(
    'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold border',
    vis === 'public'
      ? 'bg-sky-500/10 border-sky-500/25 text-sky-400'
      : 'bg-neutral-500/10 border-neutral-500/25 dark:text-neutral-400 text-neutral-500',
  )}>
    {vis === 'public' ? <Globe size={9} /> : <Lock size={9} />}
    {vis === 'public' ? 'Public' : 'Private'}
  </span>
)

const timeAgo = (iso: string) => {
  const secs = Math.floor((Date.now() - new Date(iso).getTime()) / 1000)
  if (secs < 60)  return 'just now'
  if (secs < 3600) return `${Math.floor(secs / 60)}m ago`
  return `${Math.floor(secs / 3600)}h ago`
}

// ── Visibility toggle ─────────────────────────────────────────────────────────
const VisibilityToggle = ({
  value, onChange,
}: { value: RoomVisibility; onChange: (v: RoomVisibility) => void }) => (
  <div className="flex items-center rounded-xl overflow-hidden border dark:border-surface-border border-lsurface-border text-xs font-semibold">
    {(['private', 'public'] as RoomVisibility[]).map(v => (
      <button key={v} onClick={() => onChange(v)}
        className={cn(
          'flex items-center gap-1.5 px-3 py-1.5 transition-all',
          value === v
            ? v === 'public'
              ? 'bg-sky-500 text-white'
              : 'dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-100 text-neutral-800'
            : 'dark:text-neutral-500 text-neutral-400 dark:hover:bg-surface-raised hover:bg-lsurface-raised',
        )}>
        {v === 'public' ? <Globe size={11} /> : <Lock size={11} />}
        <span className="capitalize">{v}</span>
      </button>
    ))}
  </div>
)

// ── Create card ───────────────────────────────────────────────────────────────
interface CreateCardProps {
  roomType:  RoomType
  active:    boolean
  status:    'idle' | 'loading' | 'ready' | 'full' | 'error'
  session:   { roomCode: string; inviteLink: string; visibility: RoomVisibility } | null
  copied:    boolean
  onCreate:  (vis: RoomVisibility, title: string) => void
  onCopyLink:(link: string) => void
  onEnter:   () => void
  onReset:   () => void
}

const CreateCard = ({ roomType, active, status, session, copied, onCreate, onCopyLink, onEnter, onReset }: CreateCardProps) => {
  const isGroup   = roomType === 'group'
  const cardState = active ? status : 'idle'
  const [vis,   setVis]   = useState<RoomVisibility>('private')
  const [title, setTitle] = useState('')

  return (
    <Card className="flex flex-col gap-4">
      <div className="flex items-center gap-3">
        <div className={cn('p-2.5 rounded-xl text-white shrink-0', isGroup ? 'bg-emerald-500' : 'bg-brand-500')}>
          {isGroup ? <UsersRound size={16} /> : <UserCheck size={16} />}
        </div>
        <div>
          <h2 className="text-sm font-bold dark:text-neutral-100 text-neutral-900">
            {isGroup ? 'Group Room' : 'Single Room'}
          </h2>
          <p className="text-xs dark:text-neutral-400 text-neutral-500">
            {isGroup ? 'Up to 10 participants' : '1-on-1 · 2 people only'}
          </p>
        </div>
      </div>

      <div className="space-y-2">
        <Feature icon={Shield}  text="Encrypted via LiveKit" />
        <Feature icon={Users}   text={isGroup ? 'Up to 10 participants' : '2 participants max'} />
        <Feature icon={Link2}   text="Shareable invite link" />
      </div>

      <AnimatePresence mode="wait">
        {cardState === 'idle' && (
          <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
            {/* Visibility toggle */}
            <div className="space-y-1.5">
              <p className="text-[11px] font-semibold uppercase tracking-wider dark:text-neutral-500 text-neutral-400">
                Visibility
              </p>
              <VisibilityToggle value={vis} onChange={setVis} />
              <p className="text-[11px] dark:text-neutral-500 text-neutral-400">
                {vis === 'public'
                  ? 'Listed in the lobby — anyone can browse and join.'
                  : 'Invite-only — only people with the link or code can join.'}
              </p>
            </div>

            {/* Optional title (only for public) */}
            {vis === 'public' && (
              <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}>
                <input
                  type="text"
                  value={title}
                  onChange={e => setTitle(e.target.value)}
                  placeholder={`e.g. "Frontend Interview Practice"`}
                  maxLength={60}
                  className="w-full px-3 py-2 rounded-xl text-xs border dark:border-surface-border border-lsurface-border dark:bg-surface-base bg-lsurface-base dark:text-neutral-100 text-neutral-900 placeholder:dark:text-neutral-600 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all"
                />
              </motion.div>
            )}

            <Button
              variant={isGroup ? 'secondary' : 'primary'}
              size="md" className="w-full"
              onClick={() => onCreate(vis, title)}
              icon={vis === 'public' ? <Globe size={13} /> : <Video size={13} />}
            >
              Create {vis === 'public' ? 'Public' : 'Private'} {isGroup ? 'Group' : 'Single'} Room
            </Button>
          </motion.div>
        )}

        {cardState === 'loading' && (
          <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="flex items-center justify-center gap-2 py-2">
            <Spinner size="sm" />
            <span className="text-xs dark:text-neutral-400 text-neutral-500">Setting up room…</span>
          </motion.div>
        )}

        {cardState === 'ready' && session && (
          <motion.div key="ready" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-brand-500/10 border border-brand-500/20 flex-wrap">
              <Hash size={13} className="text-brand-400 shrink-0" />
              <span className="text-sm font-bold font-mono text-brand-400 tracking-widest flex-1 min-w-0 truncate">
                {session.roomCode}
              </span>
              <div className="flex items-center gap-1.5 shrink-0">
                <RoomTypePill type={roomType} />
                <VisibilityPill vis={session.visibility} />
              </div>
            </div>

            {session.visibility === 'public' && (
              <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-sky-500/5 border border-sky-500/15 text-xs dark:text-sky-400 text-sky-600">
                <Eye size={12} className="shrink-0" />
                <span>Room is listed in the public lobby — anyone can find and join it.</span>
              </div>
            )}

            <div className="rounded-xl border dark:border-surface-border border-lsurface-border dark:bg-surface-base bg-lsurface-base p-3 space-y-2">
              <p className="text-[11px] font-semibold uppercase tracking-wider dark:text-neutral-500 text-neutral-400">Invite Link</p>
              <p className="text-xs dark:text-neutral-200 text-neutral-800 font-mono break-all leading-relaxed">{session.inviteLink}</p>
              <button onClick={() => onCopyLink(session.inviteLink)}
                className={cn('flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border transition-all',
                  copied
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    : 'dark:bg-surface-raised bg-lsurface-raised dark:border-surface-border border-lsurface-border dark:text-neutral-300 text-neutral-700 hover:border-brand-500')}>
                {copied ? <Check size={12} /> : <Copy size={12} />}
                {copied ? 'Copied!' : 'Copy Link'}
              </button>
            </div>

            <div className="flex gap-2">
              <Button variant="secondary" size="sm" className="flex-1" onClick={onReset}>New Room</Button>
              <Button variant="primary"   size="sm" className="flex-1" onClick={onEnter} icon={<ArrowRight size={13} />}>Enter Room</Button>
            </div>
          </motion.div>
        )}

        {cardState === 'error' && (
          <motion.div key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
            <p className="text-xs text-red-400">Failed to create room. Please try again.</p>
            <Button variant="secondary" size="sm" className="w-full" onClick={onReset}>Try Again</Button>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  )
}

// ── Public room listing row ───────────────────────────────────────────────────
const PublicRoomRow = ({
  room, currentUserName, onJoin, onDelete,
}: {
  room: RoomListing
  currentUserName: string
  onJoin: () => void
  onDelete: () => void
}) => {
  const max       = ROOM_MAX[room.roomType]
  const full      = room.participantCount >= max
  const isCreator = room.hostName === currentUserName
  const [confirmDelete, setConfirmDelete] = useState(false)

  return (
    <AnimatePresence mode="wait">
      {confirmDelete ? (
        /* ── Confirm delete inline ── */
        <motion.div key="confirm"
          initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
          className="flex items-center gap-3 px-4 py-3 rounded-xl border border-red-500/30 bg-red-500/5">
          <AlertTriangle size={15} className="text-red-400 shrink-0" />
          <p className="text-xs dark:text-neutral-200 text-neutral-800 flex-1">
            Remove <span className="font-semibold">{room.title || room.hostName + "'s room"}</span> from the public listing?
          </p>
          <div className="flex items-center gap-2 shrink-0">
            <Button variant="secondary" size="xs" onClick={() => setConfirmDelete(false)}>Cancel</Button>
            <Button variant="danger"    size="xs" onClick={onDelete}>Remove</Button>
          </div>
        </motion.div>
      ) : (
        /* ── Normal row ── */
        <motion.div key="row"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          className="flex items-center gap-3 px-4 py-3 rounded-xl border dark:border-surface-border border-lsurface-border dark:bg-surface-base bg-lsurface-base hover:border-brand-500/40 transition-all group">

          {/* Type icon */}
          <div className={cn('p-2 rounded-lg shrink-0',
            room.roomType === 'group' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-brand-500/10 text-brand-400')}>
            {room.roomType === 'group' ? <UsersRound size={15} /> : <UserCheck size={15} />}
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <p className="text-xs font-bold dark:text-neutral-100 text-neutral-900 truncate">
              {room.title || `${room.hostName}'s room`}
            </p>
            <div className="flex items-center gap-2 mt-0.5 flex-wrap">
              <span className="text-[10px] dark:text-neutral-500 text-neutral-400 font-mono">{room.roomCode}</span>
              <RoomTypePill type={room.roomType} />
              <span className={cn('text-[10px] font-semibold flex items-center gap-0.5',
                full ? 'text-red-400' : 'dark:text-neutral-400 text-neutral-500')}>
                <Users size={9} /> {room.participantCount}/{max}{full ? ' · Full' : ''}
              </span>
              <span className="text-[10px] dark:text-neutral-600 text-neutral-400 flex items-center gap-0.5">
                <Clock size={9} /> {timeAgo(room.createdAt)}
              </span>
              {isCreator && (
                <span className="text-[10px] font-semibold text-sky-400">· Your room</span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 shrink-0">
            {/* Delete — only visible to creator */}
            {isCreator && (
              <button
                onClick={() => setConfirmDelete(true)}
                title="Remove from public listing"
                className="p-1.5 rounded-lg text-red-400/60 hover:text-red-400 hover:bg-red-500/10 opacity-0 group-hover:opacity-100 transition-all"
              >
                <Trash2 size={13} />
              </button>
            )}
            <Button variant="primary" size="xs" onClick={onJoin} disabled={full} icon={<LogIn size={11} />}>
              {full ? 'Full' : 'Join'}
            </Button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────────────────
export const VideoRoomLobbyPage = () => {
  const navigate  = useNavigate()
  const { user }  = useAuthStore()
  const { status, session, copied, createRoom, copyInviteLink, reset } = useVideoRoom()
  const { publicRooms, reload, removeRoom } = useRoomRegistry()

  const [creatingType,  setCreatingType]  = useState<RoomType | null>(null)
  const [joinCode,      setJoinCode]      = useState('')
  const [joinCodeError, setJoinCodeError] = useState('')
  const [joinRoomType,  setJoinRoomType]  = useState<RoomType | null>(null)

  const handleCreate = (type: RoomType, vis: RoomVisibility, title: string) => {
    setCreatingType(type)
    createRoom(type, vis, title, user?.name ?? 'Host')
  }

  const handleReset = () => { setCreatingType(null); reset() }

  const handleEnterRoom = () => { if (session) navigate(`/room/${session.roomCode}`) }

  const handleJoinByCode = () => {
    const code = joinCode.trim().toLowerCase()
    if (!code) { setJoinCodeError('Please enter a Room Code.'); return }
    setJoinCodeError('')
    navigate(`/room/${code}`)
  }

  const handleJoinCodeChange = (val: string) => {
    setJoinCode(val)
    setJoinCodeError('')
    const code = val.trim().toLowerCase()
    setJoinRoomType(code.length >= 2 ? roomTypeFromCode(code) : null)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-4">

      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-xl font-bold dark:text-neutral-100 text-neutral-900">Video Interview Room</h1>
          <p className="text-sm dark:text-neutral-400 text-neutral-500 mt-1">
            Create a public or private room, or browse open rooms to join.
          </p>
        </div>
        <div className="p-3 rounded-2xl bg-brand-500/10 text-brand-400 border border-brand-500/20 shrink-0">
          <Video size={24} />
        </div>
      </div>

      {/* Create cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <CreateCard
          roomType="single" active={creatingType === 'single'}
          status={status} session={session} copied={copied}
          onCreate={(vis, title) => handleCreate('single', vis, title)}
          onCopyLink={copyInviteLink} onEnter={handleEnterRoom} onReset={handleReset}
        />
        <CreateCard
          roomType="group" active={creatingType === 'group'}
          status={status} session={session} copied={copied}
          onCreate={(vis, title) => handleCreate('group', vis, title)}
          onCopyLink={copyInviteLink} onEnter={handleEnterRoom} onReset={handleReset}
        />
      </div>

      {/* Public rooms browser */}
      <Card className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 shrink-0">
              <Globe size={16} />
            </div>
            <div>
              <h2 className="text-sm font-bold dark:text-neutral-100 text-neutral-900">Public Rooms</h2>
              <p className="text-xs dark:text-neutral-400 text-neutral-500">Open rooms anyone can join</p>
            </div>
          </div>
          <button onClick={reload}
            className="p-1.5 rounded-lg dark:text-neutral-500 text-neutral-400 dark:hover:bg-surface-raised hover:bg-lsurface-raised transition-colors"
            title="Refresh">
            <RefreshCw size={13} />
          </button>
        </div>

        {publicRooms.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-8 text-center dark:bg-surface-base bg-lsurface-base rounded-xl border dark:border-surface-border border-lsurface-border">
            <Globe size={24} className="dark:text-neutral-600 text-neutral-300" />
            <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500">No public rooms right now</p>
            <p className="text-[11px] dark:text-neutral-600 text-neutral-400">Create one above with "Public" visibility.</p>
          </div>
        ) : (
          <div className="space-y-2">
            {publicRooms.map(room => (
              <PublicRoomRow
                key={room.roomCode}
                room={room}
                currentUserName={user?.name ?? ''}
                onJoin={() => navigate(`/room/${room.roomCode}`)}
                onDelete={() => removeRoom(room.roomCode)}
              />
            ))}
          </div>
        )}
      </Card>

      {/* Join by code */}
      <Card className="flex flex-col gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 shrink-0">
            <Hash size={16} />
          </div>
          <div>
            <h2 className="text-sm font-bold dark:text-neutral-100 text-neutral-900">Join by Code</h2>
            <p className="text-xs dark:text-neutral-400 text-neutral-500">Enter a room code or paste the invite link</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 items-start">
          <div className="flex-1 space-y-1.5 w-full">
            <label className="text-xs font-semibold uppercase tracking-wider dark:text-neutral-400 text-neutral-500">Room Code</label>
            <div className="relative">
              <input
                type="text"
                value={joinCode}
                onChange={e => handleJoinCodeChange(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleJoinByCode()}
                placeholder="e.g. s-k7m2xq  ·  g-abc123  ·  pub-g-xyz789"
                autoComplete="off" spellCheck={false}
                className={cn(
                  'w-full px-3 py-2.5 rounded-xl text-sm font-mono border transition-colors',
                  'dark:bg-surface-base bg-lsurface-base dark:text-neutral-100 text-neutral-900',
                  'placeholder:dark:text-neutral-600 placeholder:text-neutral-400',
                  'focus:outline-none focus:ring-2 focus:ring-brand-500/30',
                  joinCodeError
                    ? 'border-red-500/50 focus:border-red-500'
                    : 'dark:border-surface-border border-lsurface-border focus:border-brand-500',
                )}
              />
              {joinRoomType && (
                <div className="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1">
                  <RoomTypePill type={joinRoomType} />
                </div>
              )}
            </div>
            {joinCodeError && <p className="text-[11px] text-red-400">{joinCodeError}</p>}
            <p className="text-[11px] dark:text-neutral-500 text-neutral-400">
              <span className="font-mono">s-</span> private single ·{' '}
              <span className="font-mono">g-</span> private group ·{' '}
              <span className="font-mono">pub-s-</span> public single ·{' '}
              <span className="font-mono">pub-g-</span> public group
            </p>
          </div>
          <Button variant="secondary" size="md" className="shrink-0 sm:mt-6"
            onClick={handleJoinByCode} icon={<ArrowRight size={14} />} disabled={!joinCode.trim()}>
            Join Room
          </Button>
        </div>
      </Card>

      {/* How it works */}
      <Card className="dark:bg-surface-raised/50 bg-lsurface-raised/50">
        <h3 className="text-xs font-bold uppercase tracking-wider dark:text-neutral-400 text-neutral-500 mb-4">How it works</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { n:'1', title:'Choose type & visibility', desc:'Single or Group. Public rooms appear in the lobby; private rooms are invite-only.' },
            { n:'2', title:'Create & get code',        desc:'A prefixed code (pub-s-, pub-g-, s-, g-) is generated instantly.' },
            { n:'3', title:'Share or list',            desc:'Public rooms show in the lobby. Private rooms need the invite link.' },
            { n:'4', title:'Everyone joins',           desc:'Camera and mic activate. The room enforces the participant limit.' },
          ].map(({ n, title, desc }) => (
            <div key={n} className="flex items-start gap-3">
              <span className="w-6 h-6 rounded-full bg-brand-500 text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">{n}</span>
              <div>
                <p className="text-xs font-semibold dark:text-neutral-200 text-neutral-800">{title}</p>
                <p className="text-[11px] dark:text-neutral-500 text-neutral-400 mt-0.5 leading-relaxed">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
