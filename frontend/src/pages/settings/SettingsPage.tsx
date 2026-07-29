import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation } from '@tanstack/react-query'
import { Settings, Bell, Shield, User, Save, CheckCircle2, Moon, Sun } from 'lucide-react'
import { useAuthStore, useThemeStore } from '@/store'
import { apiClient } from '@/api'
import { Card, Button, Input } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { cn } from '@/utils'

const passwordSchema = z
  .object({
    current_password: z.string().min(1, 'Current password is required'),
    new_password: z.string().min(8, 'Minimum 8 characters'),
    confirm_password: z.string(),
  })
  .refine((d) => d.new_password === d.confirm_password, {
    message: 'Passwords do not match',
    path: ['confirm_password'],
  })
type PasswordForm = z.infer<typeof passwordSchema>

type SectionKey = 'account' | 'security' | 'preferences'

export const SettingsPage = () => {
  const { user } = useAuthStore()
  const { theme, toggleTheme } = useThemeStore()
  const [activeSection, setActiveSection] = useState<SectionKey>('account')
  const [saved, setSaved] = useState(false)

  const { mutate: changePassword, isPending, error: pwError } = useMutation({
    mutationFn: (data: PasswordForm) =>
      apiClient.post('/users/change-password', data).then((r) => r.data),
    onSuccess: () => {
      setSaved(true)
      showToast('success', 'Password updated successfully!')
      setTimeout(() => setSaved(false), 3000)
      reset()
    },
    onError: () => {
      showToast('error', 'Failed to update password. Verify current password.')
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PasswordForm>({ resolver: zodResolver(passwordSchema) })

  const pwApiError =
    (pwError as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  const sections: { key: SectionKey; label: string; icon: React.ElementType; desc: string }[] = [
    { key: 'account', label: 'Account Profile', icon: User, desc: 'View your account information' },
    { key: 'security', label: 'Security', icon: Shield, desc: 'Manage password & auth' },
    { key: 'preferences', label: 'Preferences', icon: Bell, desc: 'Theme & notification settings' },
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-brand-500 text-white">
          <Settings size={18} />
        </div>
        <div>
          <h1 className="text-xl sm:text-2xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
            Platform Settings
          </h1>
          <p className="text-xs dark:text-neutral-400 text-neutral-500 font-medium">Manage your account, security, and preferences</p>
        </div>
      </div>

      <div className="flex gap-6 flex-col md:flex-row">
        {/* Navigation Sidebar */}
        <nav className="md:w-60 shrink-0">
          <ul className="space-y-1.5">
            {sections.map(({ key, label, icon: Icon, desc }) => (
              <li key={key}>
                <button
                  onClick={() => setActiveSection(key)}
                  className={cn(
                    'w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-left border transition-all group',
                    activeSection === key
                      ? 'dark:bg-brand-500/10 bg-brand-500/10 dark:border-brand-500/30 border-brand-500/30'
                      : 'dark:border-surface-border border-lsurface-border dark:hover:bg-surface-hover hover:bg-lsurface-hover border-transparent'
                  )}
                >
                  <div className={cn(
                    'p-1.5 rounded-lg transition-all shrink-0',
                    activeSection === key
                      ? 'dark:bg-brand-500/20 bg-brand-500/10 text-brand-500'
                      : 'dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-400 text-neutral-500 group-hover:text-brand-500'
                  )}>
                    <Icon size={14} />
                  </div>
                  <div>
                    <p className={cn(
                      'text-xs font-semibold leading-tight',
                      activeSection === key ? 'dark:text-neutral-100 text-neutral-900' : 'dark:text-neutral-300 text-neutral-700'
                    )}>
                      {label}
                    </p>
                    <p className="text-[10px] dark:text-neutral-500 text-neutral-400 font-medium">{desc}</p>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </nav>

        {/* Section Content */}
        <div className="flex-1 min-w-0 space-y-4">
          {activeSection === 'account' && (
            <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
              <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <User size={14} className="text-brand-500" /> Account Details
              </h2>
              <div className="grid sm:grid-cols-2 gap-3">
                {[
                  { label: 'Full Name', value: user?.name, icon: User },
                  { label: 'Email Address', value: user?.email, icon: User },
                  { label: 'Account Role', value: user?.role, icon: Shield },
                  { label: 'Account Status', value: user?.is_active ? 'Active & Verified' : 'Inactive', highlight: user?.is_active },
                ].map(({ label, value, highlight }) => (
                  <div key={label} className="p-3.5 rounded-xl dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                    <p className="text-[10px] font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-1">{label}</p>
                    <p className={cn(
                      'text-sm font-semibold capitalize',
                      highlight === true ? 'text-emerald-400' : 'dark:text-neutral-100 text-neutral-900'
                    )}>
                      {value}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {activeSection === 'security' && (
            <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
              <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Shield size={14} className="text-brand-500" /> Change Account Password
              </h2>

              {saved && (
                <div className="mb-4 flex items-center gap-2 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
                  <CheckCircle2 size={16} /> Password updated successfully.
                </div>
              )}
              {pwApiError && (
                <div className="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold">
                  {pwApiError}
                </div>
              )}

              <form
                onSubmit={handleSubmit((d) => changePassword(d))}
                className="space-y-4"
                noValidate
              >
                <Input
                  label="Current Password"
                  type="password"
                  autoComplete="current-password"
                  error={errors.current_password?.message}
                  {...register('current_password')}
                />
                <Input
                  label="New Password"
                  type="password"
                  autoComplete="new-password"
                  hint="Minimum 8 characters"
                  error={errors.new_password?.message}
                  {...register('new_password')}
                />
                <Input
                  label="Confirm New Password"
                  type="password"
                  autoComplete="new-password"
                  error={errors.confirm_password?.message}
                  {...register('confirm_password')}
                />
                <div className="pt-2">
                  <Button type="submit" loading={isPending} variant="primary" icon={<Save size={14} />}>
                    Update Password
                  </Button>
                </div>
              </form>
            </Card>
          )}

          {activeSection === 'preferences' && (
            <div className="space-y-4">
              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Sun size={14} className="text-brand-500" /> Theme & Appearance
                </h2>
                <div className="flex items-center justify-between p-4 rounded-xl dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      'p-2 rounded-xl',
                      theme === 'dark' ? 'dark:bg-brand-500/10 bg-brand-500/10 text-brand-500' : 'bg-amber-100 text-amber-500'
                    )}>
                      {theme === 'dark' ? <Moon size={16} /> : <Sun size={16} />}
                    </div>
                    <div>
                      <p className="text-sm font-semibold dark:text-neutral-100 text-neutral-900 capitalize">{theme} Mode Active</p>
                      <p className="text-xs dark:text-neutral-400 text-neutral-500 font-medium">Toggle platform interface theme</p>
                    </div>
                  </div>
                  <Button size="xs" variant="secondary" onClick={toggleTheme}>
                    Switch to {theme === 'dark' ? 'Light' : 'Dark'}
                  </Button>
                </div>
              </Card>

              <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                <h2 className="text-xs font-semibold dark:text-neutral-100 text-neutral-900 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Bell size={14} className="text-brand-500" /> Notification Preferences
                </h2>
                <div className="space-y-3">
                  {[
                    { label: 'Email on interview completion', description: 'Receive an automated evaluation breakdown via email.', defaultChecked: true },
                    { label: 'AI Study Reminders', description: 'Daily prompts to maintain your practice streak.', defaultChecked: true },
                    { label: 'Leaderboard Updates', description: 'Get notified when your global rank changes.', defaultChecked: false },
                  ].map((pref) => (
                    <div key={pref.label} className="flex items-center justify-between p-3.5 rounded-xl dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border">
                      <div>
                        <p className="text-xs font-semibold dark:text-neutral-100 text-neutral-900">{pref.label}</p>
                        <p className="text-[11px] dark:text-neutral-400 text-neutral-500 font-medium mt-0.5">{pref.description}</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer shrink-0 ml-4">
                        <input
                          type="checkbox"
                          className="sr-only peer"
                          defaultChecked={pref.defaultChecked}
                          aria-label={pref.label}
                        />
                        <div className="w-9 h-5 dark:bg-surface-border bg-neutral-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand-500" />
                      </label>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
