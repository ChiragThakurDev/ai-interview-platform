import { apiClient } from './client'
import type { Roadmap } from '@/types'

// POST /roadmap/generate?skill_report=...  — generate a learning roadmap from a skill report text
// The backend expects skill_report as a query parameter
export const generateRoadmap = async (skillReportSummary: string): Promise<Roadmap> => {
  const { data } = await apiClient.post<Roadmap>(
    '/roadmap/generate',
    null,
    { params: { skill_report: skillReportSummary } }
  )
  return data
}
