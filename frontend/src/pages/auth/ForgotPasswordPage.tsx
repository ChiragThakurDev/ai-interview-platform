import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { CheckCircle, ArrowLeft } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import { forgotPassword } from '@/api'
import { Button, Input } from '@/components/ui'

const schema = z.object({ email: z.string().email('Enter a valid email') })
type F = z.infer<typeof schema>

export const ForgotPasswordPage = () => {
  const { mutate, isPending, isSuccess, error } = useMutation({ mutationFn: (d: F) => forgotPassword(d) })
  const { register, handleSubmit, formState: { errors } } = useForm<F>({ resolver: zodResolver(schema) })
  const apiError = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  if (isSuccess) return (
    <div className="text-center space-y-3">
      <CheckCircle size={36} className="text-green-400 mx-auto" />
      <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Check your email</h2>
      <p className="text-xs dark:text-neutral-500 text-neutral-500">We sent a reset link to your inbox.</p>
      <Link to="/login" className="inline-flex items-center gap-1.5 text-xs text-brand-500 hover:text-brand-400 mt-2">
        <ArrowLeft size={13} /> Back to login
      </Link>
    </div>
  )

  return (
    <div>
      <Link to="/login" className="inline-flex items-center gap-1.5 text-xs dark:text-neutral-400 text-neutral-600 hover:text-neutral-900 dark:hover:text-neutral-200 mb-6 transition-colors">
        <ArrowLeft size={13} /> Back to login
      </Link>
      <div className="mb-6">
        <h2 className="text-xl font-semibold dark:text-neutral-50 text-neutral-900">Reset password</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-1">Enter your email and we'll send a reset link.</p>
      </div>
      {apiError && <div className="mb-4 px-3 py-2.5 rounded-md bg-red-500/10 border border-red-500/30 text-red-400 text-xs">{apiError}</div>}
      <form onSubmit={handleSubmit(d => mutate(d))} className="space-y-3.5" noValidate>
        <Input label="Email" type="email" placeholder="you@example.com" autoComplete="email" error={errors.email?.message} {...register('email')} />
        <Button type="submit" className="w-full" size="lg" loading={isPending}>Send reset link</Button>
      </form>
    </div>
  )
}
