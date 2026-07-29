import { apiClient } from './client'
import type { User, RegisterRequest } from '@/types'

export const register = async (body: RegisterRequest): Promise<User> => {
  const { data } = await apiClient.post<User>('/users/register', body)
  return data
}

export const getMe = async (): Promise<User> => {
  const { data } = await apiClient.get<User>('/users/me')
  return data
}

