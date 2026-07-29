import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getAdminDashboard,
  getAdminActivity,
  getAdminUsers,
  searchAdminUsers,
  activateUser,
  deactivateUser,
  deleteUser,
  getAdminAnalytics,
} from '@/api'

export const useAdminDashboard = () =>
  useQuery({
    queryKey: ['admin-dashboard'],
    queryFn: getAdminDashboard,
    staleTime: 60 * 1000,
  })

export const useAdminActivity = () =>
  useQuery({
    queryKey: ['admin-activity'],
    queryFn: getAdminActivity,
    staleTime: 30 * 1000,
  })

export const useAdminUsers = () =>
  useQuery({
    queryKey: ['admin-users'],
    queryFn: getAdminUsers,
    staleTime: 60 * 1000,
  })

export const useAdminUserSearch = (page: number, limit: number, search: string) =>
  useQuery({
    queryKey: ['admin-users-search', page, limit, search],
    queryFn: () => searchAdminUsers(page, limit, search),
    staleTime: 30 * 1000,
  })

export const useAdminAnalytics = () =>
  useQuery({
    queryKey: ['admin-analytics'],
    queryFn: getAdminAnalytics,
    staleTime: 2 * 60 * 1000,
  })

export const useActivateUser = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: activateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      queryClient.invalidateQueries({ queryKey: ['admin-users-search'] })
      queryClient.invalidateQueries({ queryKey: ['admin-dashboard'] })
    },
  })
}

export const useDeactivateUser = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deactivateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      queryClient.invalidateQueries({ queryKey: ['admin-users-search'] })
      queryClient.invalidateQueries({ queryKey: ['admin-dashboard'] })
    },
  })
}

export const useDeleteUser = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      queryClient.invalidateQueries({ queryKey: ['admin-users-search'] })
      queryClient.invalidateQueries({ queryKey: ['admin-dashboard'] })
    },
  })
}
