import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLogin } from '@/hooks'
import { Button, Input } from '@/components/ui'

const schema = z.object({
  email:    z.string().email('Enter a valid email'),
  password: z.string().min(1, 'Password is required'),
})
type F = z.infer<typeof schema>

export const LoginPage = () => {
  const [show, setShow] = useState(false)
  const { mutate: login, isPending, error } = useLogin()
  const { register, handleSubmit, formState: { errors } } = useForm<F>({ resolver: zodResolver(schema) })

  const apiError = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold dark:text-neutral-50 text-neutral-900">Sign in</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-1">Continue your interview preparation</p>
      </div>

      <AnimatePresence>
        {apiError && (
          <motion.div
            initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="mb-4 px-3 py-2.5 rounded-md bg-red-500/10 border border-red-500/30 text-red-400 text-xs"
          >
            {apiError}
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={handleSubmit(d => login({ email: d.email, password: d.password }))} className="space-y-3.5" noValidate>
        <Input
          label="Email"
          type="email"
          placeholder="you@example.com"
          autoComplete="email"
          error={errors.email?.message}
          {...register('email')}
        />

        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium dark:text-neutral-300 text-neutral-700">Password</label>
          <div className="relative flex items-center rounded-md border transition-all duration-150 dark:bg-surface-raised bg-white dark:border-surface-border border-lsurface-border dark:hover:border-neutral-500 hover:border-neutral-400">
            <input
              type={show ? 'text' : 'password'}
              placeholder="••••••••"
              autoComplete="current-password"
              className="flex-1 bg-transparent px-3 py-2 text-sm dark:text-neutral-100 text-neutral-900 dark:placeholder-neutral-600 placeholder-neutral-400 focus:outline-none"
              {...register('password')}
            />
            <button type="button" onClick={() => setShow(v => !v)} className="pr-3 dark:text-neutral-500 text-neutral-400 dark:hover:text-neutral-300 hover:text-neutral-600 transition-colors" aria-label="Toggle password">
              {show ? <EyeOff size={14} /> : <Eye size={14} />}
            </button>
          </div>
          {errors.password && <p className="text-xs text-red-400">{errors.password.message}</p>}
        </div>

        <div className="flex justify-end">
          <Link to="/forgot-password" className="text-xs text-brand-500 hover:text-brand-400 transition-colors">Forgot password?</Link>
        </div>

        <Button type="submit" className="w-full" size="lg" loading={isPending}>Sign in</Button>
      </form>

      <p className="mt-5 text-center text-xs dark:text-neutral-500 text-neutral-500">
        Don't have an account?{' '}
        <Link to="/register" className="text-brand-500 hover:text-brand-400 font-medium transition-colors">Create one</Link>
      </p>
    </div>
  )
}
