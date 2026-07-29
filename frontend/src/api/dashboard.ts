import { apiClient } from './client'
import type {
  DashboardStats,
  PerformanceHistoryResponse,
  ProgressStats,
  SkillReport,
  AnalyticsStats,
  TopicAnalysis,
} from '@/types'

// GET /dashboard
export const getDashboard = async (): Promise<DashboardStats> => {
  const { data } = await apiClient.get<DashboardStats>('/dashboard')
  return data
}

// GET /dashboard/performance-history
export const getPerformanceHistory = async (): Promise<PerformanceHistoryResponse> => {
  const { data } = await apiClient.get<PerformanceHistoryResponse>('/dashboard/performance-history')
  return data
}

// GET /dashboard/skills  — AI skill report from interview history
export const getSkillReport = async (): Promise<SkillReport> => {
  const { data } = await apiClient.get<SkillReport>('/dashboard/skills')
  return data
}

// GET /dashboard/progress
export const getProgress = async (): Promise<ProgressStats> => {
  const { data } = await apiClient.get<ProgressStats>('/dashboard/progress')
  return data
}

// GET /dashboard/analytics
export const getAnalytics = async (): Promise<AnalyticsStats> => {
  const { data } = await apiClient.get<AnalyticsStats>('/dashboard/analytics')
  return data
}

// GET /dashboard/topics
export const getTopicAnalysis = async (): Promise<TopicAnalysis> => {
  const { data } = await apiClient.get<TopicAnalysis>('/dashboard/topics')
  return data
}
