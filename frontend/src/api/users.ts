import { apiClient } from './client'
import type { User, RegisterRequest } from '@/types'

export interface UserAdminDashboard {
  message: string
  id: number
  name: string
  email: string
  role: string
}

export const register = async (body: RegisterRequest): Promise<User> => {
  const { data } = await apiClient.post<User>('/users/register', body)
  return data
}

export const getMe = async (): Promise<User> => {
  const { data } = await apiClient.get<User>('/users/me')
  return data
}

export const getUserAdminDashboard = async (): Promise<UserAdminDashboard> => {
  const { data } = await apiClient.get<UserAdminDashboard>('/users/admin')
  return data
}

export const getAllUsers = async (): Promise<User[]> => {
  const { data } = await apiClient.get<User[]>('/users/')
  return data
}

export const activateUserAccount = async (userId: number): Promise<User> => {
  const { data } = await apiClient.patch<User>(`/users/${userId}/activate`)
  return data
}

export const deactivateUserAccount = async (userId: number): Promise<User> => {
  const { data } = await apiClient.patch<User>(`/users/${userId}/deactivate`)
  return data
}

export const deleteUserAccount = async (userId: number) => {
  const { data } = await apiClient.delete(`/users/${userId}`)
  return data
}
