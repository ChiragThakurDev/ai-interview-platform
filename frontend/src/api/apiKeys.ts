import { apiClient } from './client'

export interface APIKeyCreate {
  name: string
  permissions?: string  // comma-separated e.g. "read,write"
}

export interface APIKeyResponse {
  id: number
  name: string
  api_key: string
  permissions: string
  is_active: boolean
  expires_at: string | null
  created_at: string
}

export interface APIKeyListResponse {
  id: number
  name: string
  permissions: string
  is_active: boolean
  expires_at: string | null
  created_at: string
}

// GET /api-keys/
export const listApiKeys = async (): Promise<APIKeyListResponse[]> => {
  const { data } = await apiClient.get<APIKeyListResponse[]>('/api-keys/')
  return data
}

// POST /api-keys/
export const createApiKey = async (body: APIKeyCreate): Promise<APIKeyResponse> => {
  const { data } = await apiClient.post<APIKeyResponse>('/api-keys/', body)
  return data
}

// GET /api-keys/{id}
export const getApiKey = async (id: number): Promise<APIKeyResponse> => {
  const { data } = await apiClient.get<APIKeyResponse>(`/api-keys/${id}`)
  return data
}

// DELETE /api-keys/{id}
export const revokeApiKey = async (id: number) => {
  const { data } = await apiClient.delete(`/api-keys/${id}`)
  return data
}

// GET /api-keys/profile  — current user's API key profile
export const getApiKeyProfile = async () => {
  const { data } = await apiClient.get('/api-keys/profile')
  return data
}
