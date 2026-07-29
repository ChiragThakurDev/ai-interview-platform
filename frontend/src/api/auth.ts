import { apiClient } from './client'
import type {
  TokenResponse,
  RefreshTokenRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
} from '@/types'

// Login uses OAuth2PasswordRequestForm (form-encoded, not JSON)
export const login = async (email: string, password: string): Promise<TokenResponse> => {
  const params = new URLSearchParams()
  params.append('username', email)
  params.append('password', password)

  const { data } = await apiClient.post<TokenResponse>('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export const refreshToken = async (body: RefreshTokenRequest): Promise<TokenResponse> => {
  const { data } = await apiClient.post<TokenResponse>('/auth/refresh', body)
  return data
}

export const forgotPassword = async (body: ForgotPasswordRequest) => {
  const { data } = await apiClient.post('/auth/forgot-password', body)
  return data
}

export const resetPassword = async (body: ResetPasswordRequest) => {
  const { data } = await apiClient.post('/auth/reset-password', body)
  return data
}

export const logout = async () => {
  const { data } = await apiClient.post('/auth/logout')
  return data
}

export const verifyEmail = async (token: string) => {
  const { data } = await apiClient.get(`/auth/verify-email?token=${token}`)
  return data
}
