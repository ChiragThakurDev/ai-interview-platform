import { apiClient } from './client'
import type {
  CreateCodingInterviewRequest,
  CodingInterview,
  CodingQuestion,
  SubmitCodeRequest,
  SubmissionResponse,
  CodingInterviewProgress,
  CodingInterviewReport,
  CodingInterviewHistory,
  CodingDashboardStats,
  LeaderboardResponse,
  CodingInterviewResultResponse,
  CodingDraft,
} from '@/types'

// POST /coding-interview/create
export const createCodingInterview = async (
  body: CreateCodingInterviewRequest
): Promise<CodingInterview> => {
  const { data } = await apiClient.post<CodingInterview>('/coding-interview/create', body)
  return data
}

// GET /coding-interview/{id}
export const getCodingInterview = async (id: number): Promise<CodingInterview> => {
  const { data } = await apiClient.get<CodingInterview>(`/coding-interview/${id}`)
  return data
}

// GET /coding-interview/{id}/questions
export const getCodingQuestions = async (id: number): Promise<CodingQuestion[]> => {
  const { data } = await apiClient.get<CodingQuestion[]>(`/coding-interview/${id}/questions`)
  return data
}

// POST /coding-interview/submit
export const submitCode = async (body: SubmitCodeRequest): Promise<SubmissionResponse> => {
  const { data } = await apiClient.post<SubmissionResponse>('/coding-interview/submit', body)
  return data
}

// GET /coding-interview/{id}/progress
export const getCodingProgress = async (id: number): Promise<CodingInterviewProgress> => {
  const { data } = await apiClient.get<CodingInterviewProgress>(
    `/coding-interview/${id}/progress`
  )
  return data
}

// GET /coding-interview/{id}/submissions
export const getCodingSubmissions = async (id: number) => {
  const { data } = await apiClient.get(`/coding-interview/${id}/submissions`)
  return data
}

// POST /coding-interview/{id}/finish
export const finishCodingInterview = async (id: number): Promise<CodingInterviewResultResponse> => {
  const { data } = await apiClient.post<CodingInterviewResultResponse>(
    `/coding-interview/${id}/finish`
  )
  return data
}

// POST /coding-interview/{id}/report  — generate AI report (POST, not GET!)
export const generateCodingReport = async (id: number): Promise<CodingInterviewReport> => {
  const { data } = await apiClient.post<CodingInterviewReport>(
    `/coding-interview/${id}/report`
  )
  return data
}

// GET /coding-interview/history
export const getCodingHistory = async (): Promise<CodingInterviewHistory> => {
  const { data } = await apiClient.get<CodingInterviewHistory>('/coding-interview/history')
  return data
}

// GET /coding-interview/dashboard
export const getCodingDashboard = async (): Promise<CodingDashboardStats> => {
  const { data } = await apiClient.get<CodingDashboardStats>('/coding-interview/dashboard')
  return data
}

// GET /coding-interview/leaderboard
export const getLeaderboard = async (): Promise<LeaderboardResponse> => {
  const { data } = await apiClient.get<LeaderboardResponse>('/coding-interview/leaderboard')
  return data
}

// GET /coding-interview/draft/{question_id}  — get saved code draft
export const getCodingDraft = async (questionId: number): Promise<CodingDraft | null> => {
  try {
    const { data } = await apiClient.get<CodingDraft>(
      `/coding-interview/draft/${questionId}`
    )
    return data
  } catch {
    return null
  }
}
