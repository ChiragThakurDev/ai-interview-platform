import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  listApiKeys, createApiKey, revokeApiKey, getApiKey,
} from '@/api'
import type { APIKeyCreate } from '@/api/apiKeys'
import { showToast } from '@/components/ui'

export const useListApiKeys = () =>
  useQuery({
    queryKey: ['api-keys'],
    queryFn: listApiKeys,
    staleTime: 60 * 1000,
  })

export const useGetApiKey = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['api-keys', id],
    queryFn: () => getApiKey(id),
    enabled,
    staleTime: 60 * 1000,
  })

export const useCreateApiKey = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: APIKeyCreate) => createApiKey(body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['api-keys'] })
      showToast.success('API key created successfully')
    },
    onError: () => showToast.error('Failed to create API key'),
  })
}

export const useRevokeApiKey = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => revokeApiKey(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['api-keys'] })
      showToast.info('API key revoked')
    },
    onError: () => showToast.error('Failed to revoke API key'),
  })
}
