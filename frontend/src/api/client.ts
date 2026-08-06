import axios from 'axios'
import toast from 'react-hot-toast'
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// ── Attach access token to every request ────────────────────────────────────
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ── Tracks whether a refresh is already in-flight ───────────────────────────
let isRefreshing = false
let failedQueue: Array<{
  resolve: (token: string) => void
  reject: (err: unknown) => void
}> = []

const processQueue = (err: unknown, token: string | null) => {
  failedQueue.forEach(p => (err ? p.reject(err) : p.resolve(token!)))
  failedQueue = []
}

apiClient.interceptors.response.use(
  response => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status

    // Handle standard errors with toasts
    if (status === 403) toast.error('Access forbidden (403)')
    if (status === 404) toast.error('Resource not found (404)')
    if (status >= 500) toast.error('Internal server error (' + status + ')')

    // Don't retry the refresh endpoint itself or already-retried requests
    if (
      status !== 401 ||
      original._retry ||
      original.url?.includes('/auth/refresh')
    ) {
      // Show toast for 401 if it's a login failure or if refresh fails
      if (status === 401 && !original.url?.includes('/auth/refresh') && !original.url?.includes('/auth/login')) {
         toast.error('Session expired or unauthorized (401)')
      }
      return Promise.reject(error)
    }

    const refreshToken = localStorage.getItem('refresh_token')

    // No refresh token → clear storage and let React Router handle the redirect
    if (!refreshToken) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      // Dispatch a custom event so the Zustand store can react without a hard reload
      window.dispatchEvent(new CustomEvent('auth:logout'))
      return Promise.reject(error)
    }

    if (isRefreshing) {
      // Queue this request until the ongoing refresh finishes
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then(token => {
        original.headers.Authorization = `Bearer ${token}`
        return apiClient(original)
      })
    }

    original._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(`${BASE_URL}/auth/refresh`, {
        refresh_token: refreshToken,
      })

      const newAccess: string = data.access_token
      const newRefresh: string = data.refresh_token

      localStorage.setItem('access_token', newAccess)
      localStorage.setItem('refresh_token', newRefresh)

      apiClient.defaults.headers.common.Authorization = `Bearer ${newAccess}`
      original.headers.Authorization = `Bearer ${newAccess}`

      processQueue(null, newAccess)
      return apiClient(original)
    } catch (refreshError) {
      processQueue(refreshError, null)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.dispatchEvent(new CustomEvent('auth:logout'))
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)
