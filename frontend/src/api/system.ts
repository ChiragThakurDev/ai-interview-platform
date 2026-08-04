import { apiClient } from './client'

export interface RootResponse {
  message: string
}

export interface HealthResponse {
  status: string
  database: string
  redis: string
}

// GET /
export const getRoot = async (): Promise<RootResponse> => {
  const { data } = await apiClient.get<RootResponse>('/')
  return data
}

// GET /health
export const getHealth = async (): Promise<HealthResponse> => {
  const { data } = await apiClient.get<HealthResponse>('/health')
  return data
}
