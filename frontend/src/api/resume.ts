import { apiClient } from './client'
import type { Resume, ResumeAnalysis } from '@/types'

// POST /resumes/upload
export const uploadResume = async (file: File): Promise<Resume> => {
  const form = new FormData()
  form.append('file', file)
  const { data } = await apiClient.post<Resume>('/resumes/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// GET /resumes/my
export const getMyResumes = async (): Promise<Resume[]> => {
  const { data } = await apiClient.get<Resume[]>('/resumes/my')
  return data
}

// DELETE /resumes/{id}
export const deleteResume = async (resumeId: number) => {
  const { data } = await apiClient.delete(`/resumes/${resumeId}`)
  return data
}

// GET /resumes/{id}/download  — used as href directly
export const downloadResumeUrl = (resumeId: number) =>
  `${import.meta.env.VITE_API_BASE_URL}/resumes/${resumeId}/download`

// POST /ai/analyze/{resume_id}  — AI resume analysis
export const analyzeResume = async (resumeId: number): Promise<ResumeAnalysis> => {
  const { data } = await apiClient.post<ResumeAnalysis>(`/ai/analyze/${resumeId}`)
  return data
}
