import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  createCodingInterview,
  getCodingInterview,
  getCodingQuestions,
  submitCode,
  getCodingProgress,
  getCodingSubmissions,
  finishCodingInterview,
  generateCodingReport,
  getCodingHistory,
  getCodingDashboard,
  getLeaderboard,
  getCodingDraft,
} from '@/api'
import { showToast } from '@/components/ui'
import type { CreateCodingInterviewRequest, SubmitCodeRequest } from '@/types'

export const useCreateCodingInterview = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: CreateCodingInterviewRequest) => createCodingInterview(body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['coding-history'] })
      qc.invalidateQueries({ queryKey: ['coding-dashboard'] })
    },
    onError: () => showToast.error('Failed to create coding interview.'),
  })
}

export const useCodingInterview = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['coding-interview', id],
    queryFn: () => getCodingInterview(id),
    enabled,
    staleTime: 30 * 1000,
  })

export const useCodingQuestions = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['coding-interview', id, 'questions'],
    queryFn: () => getCodingQuestions(id),
    enabled,
    staleTime: 5 * 60 * 1000,
  })

export const useSubmitCode = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: SubmitCodeRequest) => submitCode(body),
    onSuccess: (data, { interview_id }) => {
      qc.invalidateQueries({ queryKey: ['coding-interview', interview_id, 'progress'] })
      if (data.evaluation.passed) {
        showToast.success(`All tests passed! Score: ${data.evaluation.score}/100`)
      } else {
        showToast.info(`Score: ${data.evaluation.score}/100 — check evaluation tab.`)
      }
    },
    onError: () => showToast.error('Code submission failed.'),
  })
}

export const useCodingProgress = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['coding-interview', id, 'progress'],
    queryFn: () => getCodingProgress(id),
    enabled,
    refetchInterval: enabled ? 10_000 : false,
  })

export const useCodingSubmissions = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['coding-interview', id, 'submissions'],
    queryFn: () => getCodingSubmissions(id),
    enabled,
    staleTime: 30 * 1000,
  })

export const useFinishCodingInterview = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => finishCodingInterview(id),
    onSuccess: (_, id) => {
      qc.invalidateQueries({ queryKey: ['coding-interview', id] })
      qc.invalidateQueries({ queryKey: ['coding-history'] })
      qc.invalidateQueries({ queryKey: ['coding-dashboard'] })
      showToast.success('Interview finished! Generating report…')
    },
    onError: () => showToast.error('Failed to finish interview.'),
  })
}

// POST /coding-interview/{id}/report  — generate AI report (this is a POST!)
export const useCodingReport = (id: number) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: () => generateCodingReport(id),
    onSuccess: (data) => {
      qc.setQueryData(['coding-report', id], data)
    },
    onError: () => showToast.error('Failed to generate report.'),
  })
}

// Cached coding report data
export const useCodingReportData = (id: number) =>
  useQuery({
    queryKey: ['coding-report', id],
    queryFn: () => generateCodingReport(id),
    staleTime: 30 * 60 * 1000,
    retry: false,
  })

export const useCodingHistory = () =>
  useQuery({
    queryKey: ['coding-history'],
    queryFn: getCodingHistory,
    staleTime: 2 * 60 * 1000,
  })

export const useCodingDashboard = () =>
  useQuery({
    queryKey: ['coding-dashboard'],
    queryFn: getCodingDashboard,
    staleTime: 2 * 60 * 1000,
  })

export const useLeaderboard = () =>
  useQuery({
    queryKey: ['leaderboard'],
    queryFn: getLeaderboard,
    staleTime: 5 * 60 * 1000,
  })

// GET /coding-interview/draft/{question_id}  — autosaved code draft
export const useCodingDraft = (questionId: number, enabled = true) =>
  useQuery({
    queryKey: ['coding-draft', questionId],
    queryFn: () => getCodingDraft(questionId),
    enabled,
    staleTime: 0,
  })
