import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { CheckCircle, XCircle, Loader2, ArrowRight } from 'lucide-react'
import { verifyEmail } from '@/api/auth'
import { Button } from '@/components/ui'

export const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    if (!token) {
      setStatus('error')
      setErrorMessage('No verification token provided.')
      return
    }

    const verify = async () => {
      try {
        await verifyEmail(token)
        setStatus('success')
      } catch (err: any) {
        setStatus('error')
        setErrorMessage(err?.response?.data?.detail || 'Verification failed. The link may have expired.')
      }
    }

    verify()
  }, [token])

  return (
    <div className="text-center space-y-4">
      {status === 'loading' && (
        <>
          <Loader2 size={36} className="animate-spin text-brand-500 mx-auto" />
          <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Verifying Email...</h2>
          <p className="text-xs dark:text-neutral-500 text-neutral-500">Please wait while we verify your email address.</p>
        </>
      )}

      {status === 'success' && (
        <>
          <CheckCircle size={36} className="text-emerald-500 mx-auto" />
          <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Email Verified!</h2>
          <p className="text-xs dark:text-neutral-500 text-neutral-500">Your email has been successfully verified.</p>
          <div className="pt-2">
            <Link to="/login">
              <Button className="w-full">
                Continue to Login <ArrowRight size={14} className="ml-2" />
              </Button>
            </Link>
          </div>
        </>
      )}

      {status === 'error' && (
        <>
          <XCircle size={36} className="text-red-500 mx-auto" />
          <h2 className="text-base font-semibold dark:text-neutral-100 text-neutral-900">Verification Failed</h2>
          <p className="text-xs text-red-500/80 bg-red-500/10 px-3 py-2 rounded border border-red-500/20 mt-2 inline-block mx-auto">
            {errorMessage}
          </p>
          <div className="pt-2">
            <Link to="/login">
              <Button variant="outline" className="w-full">
                Back to Login
              </Button>
            </Link>
          </div>
        </>
      )}
    </div>
  )
}
