import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Key, Plus, Trash2, Eye, EyeOff, Copy, Check,
  Shield, AlertTriangle, RefreshCw, Lock, Unlock,
} from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useListApiKeys, useCreateApiKey, useRevokeApiKey } from '@/hooks'
import { Card, Button, Badge, Spinner, EmptyState, Input } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'
import type { APIKeyResponse } from '@/api/apiKeys'

const createSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(64),
  permissions: z.string().default('read'),
})
type CreateForm = z.infer<typeof createSchema>

const PERMISSION_OPTIONS = [
  { value: 'read', label: 'Read Only', desc: 'Can read data from the API', color: 'text-emerald-400', icon: Unlock },
  { value: 'read,write', label: 'Read + Write', desc: 'Can read and write data', color: 'text-amber-400', icon: Lock },
]

// Newly-created key card — shows the raw key once, then hides it
const NewKeyReveal = ({ apiKey, onDone }: { apiKey: APIKeyResponse; onDone: () => void }) => {
  const [copied, setCopied] = useState(false)

  const copy = () => {
    navigator.clipboard.writeText(apiKey.api_key)
    setCopied(true)
    setTimeout(() => setCopied(false), 2500)
    showToast.success('API key copied to clipboard')
  }

  return (
    <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
      className="p-5 rounded-2xl border border-emerald-500/30 bg-emerald-500/5 space-y-4">
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-xl bg-emerald-500/10 shrink-0">
          <Key size={16} className="text-emerald-400" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold dark:text-neutral-100 text-neutral-900">{apiKey.name}</p>
          <p className="text-xs text-amber-400 font-semibold mt-1 flex items-center gap-1.5">
            <AlertTriangle size={11} />
            Copy this key now — it won't be shown again
          </p>
        </div>
        <Button variant="ghost" size="xs" onClick={onDone}>Dismiss</Button>
      </div>
      <div className="flex items-center gap-2">
        <code className="flex-1 text-xs font-mono dark:bg-surface-base bg-neutral-100 dark:text-emerald-300 text-emerald-700 px-3 py-2.5 rounded-xl border dark:border-surface-border border-lsurface-border truncate select-all">
          {apiKey.api_key}
        </code>
        <button onClick={copy}
          className="shrink-0 p-2 rounded-xl dark:bg-surface-raised bg-neutral-100 dark:text-neutral-300 text-neutral-600 hover:text-emerald-400 transition-colors border dark:border-surface-border border-lsurface-border">
          {copied ? <Check size={15} className="text-emerald-400" /> : <Copy size={15} />}
        </button>
      </div>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="dark:text-neutral-400 text-neutral-500">
          Permissions: <span className="font-semibold dark:text-neutral-200 text-neutral-700">{apiKey.permissions}</span>
        </div>
        <div className="dark:text-neutral-400 text-neutral-500 text-right">
          Expires: <span className="font-semibold dark:text-neutral-200 text-neutral-700">
            {apiKey.expires_at ? new Date(apiKey.expires_at).toLocaleDateString() : 'Never'}
          </span>
        </div>
      </div>
    </motion.div>
  )
}

// Masked key row in the list
const KeyRow = ({ k, onRevoke }: { k: { id: number; name: string; permissions: string; is_active: boolean; expires_at: string | null; created_at: string }; onRevoke: (id: number) => void }) => {
  const [confirm, setConfirm] = useState(false)

  const permColor = k.permissions.includes('write') ? 'warning' : 'success'
  const isExpired = k.expires_at && new Date(k.expires_at) < new Date()

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
      className="flex items-center gap-4 px-5 py-4 dark:hover:bg-surface-hover hover:bg-lsurface-hover transition-colors">
      <div className="p-2 rounded-xl dark:bg-surface-raised bg-neutral-100 shrink-0">
        <Key size={14} className={k.is_active && !isExpired ? 'text-brand-500' : 'dark:text-neutral-500 text-neutral-400'} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold dark:text-neutral-100 text-neutral-900">{k.name}</p>
        <p className="text-xs dark:text-neutral-500 text-neutral-400 mt-0.5">
          Created {new Date(k.created_at).toLocaleDateString()}
          {k.expires_at && ` · Expires ${new Date(k.expires_at).toLocaleDateString()}`}
        </p>
      </div>
      <code className="text-xs font-mono dark:text-neutral-500 text-neutral-400 hidden sm:block">
        ••••••••••••••••
      </code>
      <Badge variant={permColor} size="xs">{k.permissions}</Badge>
      <Badge variant={!k.is_active || isExpired ? 'danger' : 'success'} size="xs">
        {!k.is_active ? 'Revoked' : isExpired ? 'Expired' : 'Active'}
      </Badge>
      {confirm ? (
        <div className="flex items-center gap-1 shrink-0">
          <button onClick={() => onRevoke(k.id)}
            className="px-2 py-1 text-xs font-bold rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors">
            Confirm
          </button>
          <button onClick={() => setConfirm(false)}
            className="px-2 py-1 text-xs rounded-lg dark:text-neutral-400 text-neutral-500 dark:hover:bg-surface-raised hover:bg-neutral-100 transition-colors">
            Cancel
          </button>
        </div>
      ) : (
        <button onClick={() => setConfirm(true)} disabled={!k.is_active}
          className="shrink-0 p-1.5 rounded-lg hover:bg-red-500/10 text-red-400 disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
          <Trash2 size={14} />
        </button>
      )}
    </motion.div>
  )
}

export const ApiKeysPage = () => {
  const [showCreate, setShowCreate] = useState(false)
  const [newKey, setNewKey] = useState<APIKeyResponse | null>(null)

  const { data: keys, isLoading } = useListApiKeys()
  const { mutate: create, isPending: creating } = useCreateApiKey()
  const { mutate: revoke } = useRevokeApiKey()

  const { register, handleSubmit, reset, watch, setValue, formState: { errors } } = useForm<CreateForm>({
    resolver: zodResolver(createSchema),
    defaultValues: { name: '', permissions: 'read' },
  })
  const selectedPerms = watch('permissions')

  const onSubmit = (data: CreateForm) => {
    create(data, {
      onSuccess: (key) => {
        setNewKey(key)
        setShowCreate(false)
        reset()
      },
    })
  }

  const activeCount = keys?.filter(k => k.is_active).length ?? 0

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">

      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-bold mb-2">
            <Shield size={11} /> Developer Access
          </div>
          <h1 className="text-2xl font-black dark:text-neutral-50 text-neutral-900">API Keys</h1>
          <p className="text-sm dark:text-neutral-400 text-neutral-500 mt-1">
            Manage keys for programmatic access to the platform API.
          </p>
        </div>
        <Button variant="primary" size="sm" icon={<Plus size={14} />} onClick={() => setShowCreate(v => !v)}>
          New Key
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Total Keys', value: keys?.length ?? 0, color: 'text-brand-500' },
          { label: 'Active', value: activeCount, color: 'text-emerald-400' },
          { label: 'Revoked', value: (keys?.length ?? 0) - activeCount, color: 'text-red-400' },
        ].map(s => (
          <Card key={s.label} className="p-4 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card text-center">
            <p className={cn('text-2xl font-black tabular-nums', s.color)}>{s.value}</p>
            <p className="text-xs dark:text-neutral-500 text-neutral-400 font-semibold mt-0.5">{s.label}</p>
          </Card>
        ))}
      </div>

      {/* Newly created key reveal */}
      <AnimatePresence>
        {newKey && <NewKeyReveal apiKey={newKey} onDone={() => setNewKey(null)} />}
      </AnimatePresence>

      {/* Create form */}
      <AnimatePresence>
        {showCreate && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}>
            <Card className="border dark:border-brand-500/25 border-brand-500/20 dark:bg-surface-card bg-lsurface-card space-y-5">
              <div className="flex items-center gap-2">
                <Plus size={15} className="text-brand-500" />
                <h2 className="text-sm font-bold dark:text-neutral-100 text-neutral-900">Create New API Key</h2>
              </div>

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                <Input
                  label="Key Name"
                  placeholder="e.g. Production App, CI/CD Pipeline"
                  error={errors.name?.message}
                  {...register('name')}
                />

                <div>
                  <p className="text-xs font-semibold dark:text-neutral-300 text-neutral-700 mb-2">Permissions</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {PERMISSION_OPTIONS.map(opt => (
                      <button key={opt.value} type="button"
                        onClick={() => setValue('permissions', opt.value)}
                        className={cn(
                          'p-4 rounded-xl border text-left transition-all',
                          selectedPerms === opt.value
                            ? 'border-brand-500/50 dark:bg-brand-500/10 bg-brand-50'
                            : 'dark:border-surface-border border-lsurface-border dark:bg-surface-raised bg-neutral-50 hover:border-brand-500/30'
                        )}>
                        <div className="flex items-center gap-2 mb-1.5">
                          <opt.icon size={14} className={opt.color} />
                          <span className="text-xs font-bold dark:text-neutral-100 text-neutral-900">{opt.label}</span>
                          {selectedPerms === opt.value && (
                            <Check size={12} className="text-brand-500 ml-auto" />
                          )}
                        </div>
                        <p className="text-xs dark:text-neutral-400 text-neutral-500">{opt.desc}</p>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-1">
                  <Button variant="ghost" type="button" onClick={() => { setShowCreate(false); reset() }}>
                    Cancel
                  </Button>
                  <Button variant="primary" type="submit" loading={creating} icon={<Key size={14} />}>
                    Generate Key
                  </Button>
                </div>
              </form>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Keys list */}
      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-0 overflow-hidden">
        <div className="px-5 py-4 border-b dark:border-surface-border border-lsurface-border flex items-center gap-2">
          <Key size={14} className="text-brand-500" />
          <h2 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider">Your API Keys</h2>
          <span className="ml-auto text-xs dark:text-neutral-500 text-neutral-400 font-semibold">{keys?.length ?? 0} total</span>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-16"><Spinner size="lg" /></div>
        ) : !keys || keys.length === 0 ? (
          <EmptyState icon={<Key size={32} />} title="No API keys yet"
            description="Create your first API key to access the platform programmatically."
            action={<Button variant="primary" size="sm" icon={<Plus size={13} />} onClick={() => setShowCreate(true)}>Create Key</Button>}
            className="py-16" />
        ) : (
          <div className="divide-y dark:divide-surface-border divide-lsurface-border">
            {keys.map(k => (
              <KeyRow key={k.id} k={k} onRevoke={revoke} />
            ))}
          </div>
        )}
      </Card>

      {/* Usage notes */}
      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-5 space-y-3">
        <h3 className="text-xs font-bold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider flex items-center gap-2">
          <Shield size={13} className="text-brand-500" /> How to Use
        </h3>
        <div className="space-y-2">
          {[
            { label: 'Authorization header', code: 'X-API-Key: your_api_key_here' },
            { label: 'cURL example', code: 'curl -H "X-API-Key: your_key" http://127.0.0.1:5000/api-keys/profile' },
          ].map(ex => (
            <div key={ex.label}>
              <p className="text-xs dark:text-neutral-400 text-neutral-500 mb-1">{ex.label}</p>
              <code className="block text-xs font-mono dark:bg-surface-base bg-neutral-100 dark:text-neutral-300 text-neutral-700 px-3 py-2 rounded-lg border dark:border-surface-border border-lsurface-border break-all">
                {ex.code}
              </code>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
