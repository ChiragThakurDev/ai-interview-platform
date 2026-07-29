import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/store'
import { PageLoader } from '@/components/ui'
import { useMe } from '@/hooks'

export const ProtectedRoute = () => {
  const { isAuthenticated } = useAuthStore()

  // If there's no token at all, kick to login immediately — don't even fire useMe
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return <AuthenticatedOutlet />
}

// Separate component so useMe only runs when isAuthenticated is already true.
// This prevents the hook from firing (and causing a 401 → logout loop) while
// the Zustand persist middleware is still rehydrating on first load.
const AuthenticatedOutlet = () => {
  const { isLoading, isError } = useMe()

  // If /users/me returned an error (e.g. token truly invalid) the auth:logout
  // event will have already been dispatched by the interceptor, which clears
  // the store. The parent ProtectedRoute will then re-render and redirect.
  // Show loader only on the initial fetch, not on background refetches.
  if (isLoading) return <PageLoader />
  if (isError)   return <Navigate to="/login" replace />

  return <Outlet />
}
