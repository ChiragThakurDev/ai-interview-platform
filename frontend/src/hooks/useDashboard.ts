import { useQuery } from '@tanstack/react-query'
import {
  getDashboard,
  getPerformanceHistory,
  getSkillReport,
  getProgress,
  getAnalytics,
  getTopicAnalysis,
} from '@/api'

export const useDashboard = () =>
  useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboard,
    staleTime: 2 * 60 * 1000,
  })

export const usePerformanceHistory = () =>
  useQuery({
    queryKey: ['performance-history'],
    queryFn: getPerformanceHistory,
    staleTime: 5 * 60 * 1000,
    retry: false,
  })

// GET /dashboard/skills — AI skill report
export const useSkillReport = () =>
  useQuery({
    queryKey: ['skill-report'],
    queryFn: getSkillReport,
    staleTime: 10 * 60 * 1000,
    retry: false, // returns 404 when no interviews done yet
  })

export const useProgress = () =>
  useQuery({
    queryKey: ['progress'],
    queryFn: getProgress,
    staleTime: 2 * 60 * 1000,
    retry: false,
  })

export const useAnalytics = () =>
  useQuery({
    queryKey: ['analytics'],
    queryFn: getAnalytics,
    staleTime: 5 * 60 * 1000,
    retry: false,
  })

export const useTopicAnalysis = () =>
  useQuery({
    queryKey: ['topic-analysis'],
    queryFn: getTopicAnalysis,
    staleTime: 5 * 60 * 1000,
    retry: false,
  })
