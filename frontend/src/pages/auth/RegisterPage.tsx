import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff, CheckCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRegister } from '@/hooks'
import { Button, Input } from '@/components/ui'

const schema = z.object({
  name:            z.string().min(2, 'At least 2 characters'),
  email:           z.string().email('Enter a valid email'),
  password:        z.string().min(8, 'At least 8 characters').regex(/[A-Z]/, 'Needs uppercase').regex(/[0-9]/, 'Needs a number'),
  confirmPassword: z.string(),
}).refine(d => d.password === d.confirmPassword, { message: "Passwords don't match", path: ['confirmPassword'] })

type F = z.infer<typeof schema>

const RULES = [
  { label: '8+ chars',  test: (v: string) => v.length >= 8 },
  { label: 'Uppercase', test: (v: string) => /[A-Z]/.test(v) },
  { label: 'Number',    test: (v: string) => /[0-9]/.test(v) },
]

export const RegisterPage = () => {
  const [show, setShow] = useState(false)
  const { mutate: register, isPending, error, isSuccess } = useRegister()
  const { register: reg, handleSubmit, watch, formState: { errors } } = useForm<F>({ resolver: zodResolver(schema) })
  const pw = watch('password', '')
  const apiError = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  if (isSuccess) return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center space-y-3 py-6">
      <CheckCircle size={40} className="text-green-400 mx-auto" />
      <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Account created!</h2>
      <p className="text-xs dark:text-neutral-500 text-neutral-500">Check your email to verify, then sign in.</p>
      <Link to="/login"><Button className="mt-2" size="sm">Go to login</Button></Link>
    </motion.div>
  )

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold dark:text-neutral-50 text-neutral-900">Create account</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-1">Free forever — no credit card required</p>
      </div>

      <AnimatePresence>
        {apiError && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="mb-4 px-3 py-2.5 rounded-md bg-red-500/10 border border-red-500/30 text-red-400 text-xs">
            {apiError}
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={handleSubmit(d => register({ name: d.name, email: d.email, password: d.password }))} className="space-y-3.5" noValidate>
        <Input label="Full name"      type="text"     placeholder="Jane Smith"      autoComplete="name"           error={errors.name?.message}            {...reg('name')} />
        <Input label="Email"          type="email"    placeholder="you@example.com" autoComplete="email"          error={errors.email?.message}           {...reg('email')} />

        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium dark:text-neutral-300 text-neutral-700">Password</label>
          <div className="relative flex items-center rounded-md border transition-all dark:bg-surface-raised bg-white dark:border-surface-border border-lsurface-border">
            <input type={show ? 'text' : 'password'} placeholder="••••••••" autoComplete="new-password"
              className="flex-1 bg-transparent px-3 py-2 text-sm dark:text-neutral-100 text-neutral-900 dark:placeholder-neutral-600 placeholder-neutral-400 focus:outline-none"
              {...reg('password')} />
            <button type="button" onClick={() => setShow(v => !v)} className="pr-3 dark:text-neutral-500 text-neutral-400 hover:text-neutral-600 transition-colors"><Eye size={14} /></button>
          </div>
          {errors.password && <p className="text-xs text-red-400">{errors.password.message}</p>}
          {pw && (
            <div className="flex gap-3 mt-1">
              {RULES.map(r => (
                <span key={r.label} className={`text-2xs flex items-center gap-1 transition-colors ${r.test(pw) ? 'text-green-400' : 'dark:text-neutral-600 text-neutral-400'}`}>
                  <CheckCircle size={9} /> {r.label}
                </span>
              ))}
            </div>
          )}
        </div>

        <Input label="Confirm password" type="password" placeholder="••••••••" autoComplete="new-password" error={errors.confirmPassword?.message} {...reg('confirmPassword')} />

        <Button type="submit" className="w-full" size="lg" loading={isPending}>Create account</Button>
      </form>

      <p className="mt-5 text-center text-xs dark:text-neutral-500 text-neutral-500">
        Already have an account?{' '}
        <Link to="/login" className="text-brand-500 hover:text-brand-400 font-medium transition-colors">Sign in</Link>
      </p>
    </div>
  )
}
