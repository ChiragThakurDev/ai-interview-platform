import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useLocation } from 'react-router-dom'
import { login as apiLogin, logout as apiLogout } from '@/api/auth'
import { register as apiRegister, getMe } from '@/api/users'
import { useAuthStore } from '@/store'
import { showToast } from '@/components/ui'
import type { RegisterRequest } from '@/types'

export const useLogin = () => {
  const { setTokens, setUser } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      apiLogin(email, password),
    onSuccess: async (data) => {
      setTokens(data.access_token, data.refresh_token)
      try {
        const user = await getMe()
        setUser(user)
        showToast.success(`Welcome back, ${user.name.split(' ')[0]}!`)
      } catch {
        showToast.success('Logged in successfully!')
      }
      queryClient.invalidateQueries({ queryKey: ['me'] })
      // Redirect back to wherever the user was trying to go (e.g. /room/lrbiku)
      const from = (location.state as { from?: { pathname: string; search?: string } })?.from
      const destination = from ? `${from.pathname}${from.search ?? ''}` : '/dashboard'
      navigate(destination, { replace: true })
    },
    onError: (err: { response?: { data?: { detail?: string } } }) => {
      showToast.error(err?.response?.data?.detail ?? 'Login failed. Please try again.')
    },
  })
}

export const useRegister = () => {
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (body: RegisterRequest) => apiRegister(body),
    onSuccess: () => {
      showToast.success('Account created! Check your email to verify.')
      navigate('/login')
    },
    onError: (err: { response?: { data?: { detail?: string } } }) => {
      showToast.error(err?.response?.data?.detail ?? 'Registration failed.')
    },
  })
}

export const useLogout = () => {
  const { logout } = useAuthStore()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: apiLogout,
    onSettled: () => {
      logout()
      queryClient.clear()
      showToast.info('Logged out successfully.')
      navigate('/login')
    },
  })
}

export const useMe = () => {
  const { isAuthenticated, setUser } = useAuthStore()

  return useQuery({
    queryKey: ['me'],
    queryFn: async () => {
      const user = await getMe()
      setUser(user)
      return user
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
    retry: false,                  // don't retry on 401 — the interceptor handles it
    refetchOnWindowFocus: false,   // don't re-fire every time the tab regains focus
  })
}
