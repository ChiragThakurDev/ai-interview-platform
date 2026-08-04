import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/store'
import { PageLoader } from '@/components/ui'
import { useMe } from '@/hooks'

export const ProtectedRoute = () => {
  const { isAuthenticated } = useAuthStore()
  const location = useLocation()

  // Not logged in → send to /login, remembering where they wanted to go
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <AuthenticatedOutlet />
}

const AuthenticatedOutlet = () => {
  const { isLoading, isError } = useMe()

  if (isLoading) return <PageLoader />
  if (isError)   return <Navigate to="/login" replace />

  return <Outlet />
}
