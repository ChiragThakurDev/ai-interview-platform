import { useState } from 'react'
import { Link, useSearchParams, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { CheckCircle, ArrowLeft } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import { resetPassword } from '@/api/auth'
import { Button, Input } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'

const schema = z.object({
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type F = z.infer<typeof schema>

export const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const navigate = useNavigate()

  const { mutate, isPending, isSuccess, error } = useMutation({ 
    mutationFn: (d: F) => resetPassword({ token: token || '', new_password: d.password })
  })

  const { register, handleSubmit, formState: { errors } } = useForm<F>({ 
    resolver: zodResolver(schema) 
  })

  const apiError = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  if (!token) {
    return (
      <div className="text-center space-y-3">
        <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Invalid Link</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500">No reset token provided in the URL.</p>
        <Link to="/forgot-password" className="inline-flex items-center gap-1.5 text-xs text-brand-500 hover:text-brand-400 mt-2">
          <ArrowLeft size={13} /> Request new link
        </Link>
      </div>
    )
  }

  if (isSuccess) {
    return (
      <div className="text-center space-y-3">
        <CheckCircle size={36} className="text-emerald-400 mx-auto" />
        <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Password Reset</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500">Your password has been changed successfully.</p>
        <Button onClick={() => navigate('/login')} className="w-full mt-4">
          Go to Login
        </Button>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold dark:text-neutral-50 text-neutral-900">Set New Password</h2>
        <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-1">Please enter your new password below.</p>
      </div>
      
      {apiError && (
        <div className="mb-4 px-3 py-2.5 rounded-md bg-red-500/10 border border-red-500/30 text-red-400 text-xs">
          {apiError}
        </div>
      )}
      
      <form onSubmit={handleSubmit(d => mutate(d))} className="space-y-4" noValidate>
        <Input 
          label="New Password" 
          type="password" 
          placeholder="••••••••" 
          error={errors.password?.message} 
          {...register('password')} 
        />
        <Input 
          label="Confirm Password" 
          type="password" 
          placeholder="••••••••" 
          error={errors.confirmPassword?.message} 
          {...register('confirmPassword')} 
        />
        <Button type="submit" className="w-full" size="lg" loading={isPending}>
          Reset Password
        </Button>
      </form>
    </div>
  )
}
