import { apiClient } from './client'
import type {
  GenerateInterviewRequest,
  GenerateInterviewResponse,
  Interview,
  StartInterviewResponse,
  CurrentQuestionResponse,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
  FinishInterviewResponse,
  InterviewResult,
  InterviewReport,
  SubmitInterviewAnswerRequest,
  InterviewAnswerResponse,
} from '@/types'

// POST /interview/generate/{resume_id}
export const generateInterview = async (
  resumeId: number,
  body: GenerateInterviewRequest
): Promise<GenerateInterviewResponse> => {
  const { data } = await apiClient.post<GenerateInterviewResponse>(
    `/interview/generate/${resumeId}`,
    body
  )
  return data
}

// GET /interview/my
export const getMyInterviews = async (): Promise<Interview[]> => {
  const { data } = await apiClient.get<Interview[]>('/interview/my')
  return data
}

// POST /interview/{id}/start
export const startInterview = async (id: number): Promise<StartInterviewResponse> => {
  const { data } = await apiClient.post<StartInterviewResponse>(`/interview/${id}/start`)
  return data
}

// GET /interview/{id}/current-question
export const getCurrentQuestion = async (id: number): Promise<CurrentQuestionResponse> => {
  const { data } = await apiClient.get<CurrentQuestionResponse>(`/interview/${id}/current-question`)
  return data
}

// POST /interview/{id}/answer
export const submitAnswer = async (
  id: number,
  body: SubmitAnswerRequest
): Promise<SubmitAnswerResponse> => {
  const { data } = await apiClient.post<SubmitAnswerResponse>(`/interview/${id}/answer`, body)
  return data
}

// POST /interview/{id}/finish
export const finishInterview = async (id: number): Promise<FinishInterviewResponse> => {
  const { data } = await apiClient.post<FinishInterviewResponse>(`/interview/${id}/finish`)
  return data
}

// GET /interview/{id}/results  — questions + per-question scores + inline report
export const getInterviewResults = async (id: number): Promise<InterviewResult> => {
  const { data } = await apiClient.get<InterviewResult>(`/interview/${id}/results`)
  return data
}

// GET /interview/{id}/report  — AI-generated full report (persisted)
export const getInterviewReport = async (id: number): Promise<InterviewReport> => {
  const { data } = await apiClient.get<InterviewReport>(`/interview/${id}/report`)
  return data
}

// GET /interviews/{id}/result  — from the interview_result router (separate prefix)
export const getInterviewResult = async (id: number): Promise<InterviewResult> => {
  const { data } = await apiClient.get<InterviewResult>(`/interviews/${id}/result`)
  return data
}

// POST /answers/{question_id}  — submit an answer for a specific question
export const submitInterviewAnswer = async (
  questionId: number,
  body: SubmitInterviewAnswerRequest
): Promise<InterviewAnswerResponse> => {
  const { data } = await apiClient.post<InterviewAnswerResponse>(
    `/answers/${questionId}`,
    body
  )
  return data
}

// GET /answers/{question_id}  — get the saved answer for a specific question
export const getInterviewAnswer = async (questionId: number): Promise<InterviewAnswerResponse> => {
  const { data } = await apiClient.get<InterviewAnswerResponse>(`/answers/${questionId}`)
  return data
}
