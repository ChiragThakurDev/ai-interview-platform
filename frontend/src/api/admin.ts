import { apiClient } from './client'
import type {
  AdminDashboardStats,
  AdminActivity,
  AdminUser,
  AdminUserSearchResult,
  AdminAnalytics,
} from '@/types'

// GET /admin/dashboard
export const getAdminDashboard = async (): Promise<AdminDashboardStats> => {
  const { data } = await apiClient.get<AdminDashboardStats>('/admin/dashboard')
  return data
}

// GET /admin/activity  — returns { recent_users, recent_interviews, recent_reports }
export const getAdminActivity = async (): Promise<AdminActivity> => {
  const { data } = await apiClient.get<AdminActivity>('/admin/activity')
  return data
}

// GET /admin/users
export const getAdminUsers = async (): Promise<AdminUser[]> => {
  const { data } = await apiClient.get<AdminUser[]>('/admin/users')
  return data
}

// GET /admin/users/search
export const searchAdminUsers = async (
  page: number = 1,
  limit: number = 10,
  search: string = '',
): Promise<AdminUserSearchResult> => {
  const { data } = await apiClient.get<AdminUserSearchResult>('/admin/users/search', {
    params: { page, limit, search },
  })
  return data
}

// PATCH /admin/users/{id}/activate
export const activateUser = async (userId: number) => {
  const { data } = await apiClient.patch(`/admin/users/${userId}/activate`)
  return data
}

// PATCH /admin/users/{id}/deactivate
export const deactivateUser = async (userId: number) => {
  const { data } = await apiClient.patch(`/admin/users/${userId}/deactivate`)
  return data
}

// DELETE /admin/users/{id}
export const deleteUser = async (userId: number) => {
  const { data } = await apiClient.delete(`/admin/users/${userId}`)
  return data
}

// GET /admin/analytics
export const getAdminAnalytics = async (): Promise<AdminAnalytics> => {
  const { data } = await apiClient.get<AdminAnalytics>('/admin/analytics')
  return data
}
