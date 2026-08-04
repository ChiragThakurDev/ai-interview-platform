import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  generateInterview,
  getMyInterviews,
  startInterview,
  getCurrentQuestion,
  submitAnswer,
  finishInterview,
  getInterviewResults,
  getInterviewReport,
  submitInterviewAnswer,
  getInterviewAnswer,
} from '@/api'
import { showToast } from '@/components/ui'
import type { GenerateInterviewRequest, SubmitAnswerRequest, SubmitInterviewAnswerRequest } from '@/types'

export const useMyInterviews = () =>
  useQuery({
    queryKey: ['interviews'],
    queryFn: getMyInterviews,
    staleTime: 0,               // always re-fetch — status changes mid-session
    refetchOnWindowFocus: true,
  })

export const useCreateInterview = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ resumeId, body }: { resumeId: number; body: GenerateInterviewRequest }) =>
      generateInterview(resumeId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['interviews'] })
      showToast.success('Interview generated successfully!')
    },
    onError: () => showToast.error('Failed to create interview.'),
  })
}

export const useStartInterview = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => startInterview(id),
    onSuccess: (_, id) => {
      // Invalidate both the single interview and the full list so
      // History shows "In Progress" immediately after a session starts
      qc.invalidateQueries({ queryKey: ['interview', id] })
      qc.invalidateQueries({ queryKey: ['interviews'] })
    },
    onError: () => showToast.error('Failed to start interview.'),
  })
}

export const useCurrentQuestion = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['interview', id, 'current-question'],
    queryFn: () => getCurrentQuestion(id),
    enabled,
    staleTime: 0,
  })

export const useSubmitAnswer = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ interviewId, body }: { interviewId: number; body: SubmitAnswerRequest }) =>
      submitAnswer(interviewId, body),
    onSuccess: (data, { interviewId }) => {
      qc.invalidateQueries({ queryKey: ['interview', interviewId, 'current-question'] })
      // When the last answer is submitted the backend marks the interview
      // completed — flush the list cache so History reflects it instantly
      if (data.interview_completed) {
        qc.invalidateQueries({ queryKey: ['interviews'] })
        qc.invalidateQueries({ queryKey: ['interview', interviewId] })
      }
    },
    onError: () => showToast.error('Failed to submit answer.'),
  })
}

// POST /interview/{id}/finish
export const useFinishInterview = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => finishInterview(id),
    onSuccess: (_, id) => {
      qc.invalidateQueries({ queryKey: ['interviews'] })
      qc.invalidateQueries({ queryKey: ['interview', id] })
    },
    onError: () => showToast.error('Failed to finish interview.'),
  })
}

// GET /interview/{id}/results  — questions + per-answer scores
export const useInterviewResults = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['interview', id, 'results'],
    queryFn: () => getInterviewResults(id),
    enabled,
    staleTime: 5 * 60 * 1000,
  })

// GET /interview/{id}/report  — full AI report
export const useInterviewReport = (id: number, enabled = true) =>
  useQuery({
    queryKey: ['interview', id, 'report'],
    queryFn: () => getInterviewReport(id),
    enabled,
    staleTime: 10 * 60 * 1000,
    retry: false,
  })

// POST /answers/{question_id}  — direct answer submit with AI eval (alternative to session flow)
export const useSubmitInterviewAnswer = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ questionId, body }: { questionId: number; body: SubmitInterviewAnswerRequest }) =>
      submitInterviewAnswer(questionId, body),
    onSuccess: (_, { questionId }) => {
      qc.invalidateQueries({ queryKey: ['interview-answer', questionId] })
    },
    onError: () => showToast.error('Failed to submit answer'),
  })
}

// GET /answers/{question_id}  — fetch saved answer for a specific question
export const useInterviewAnswer = (questionId: number, enabled = true) =>
  useQuery({
    queryKey: ['interview-answer', questionId],
    queryFn: () => getInterviewAnswer(questionId),
    enabled,
    staleTime: 5 * 60 * 1000,
    retry: false,   // 404 is expected when no answer saved yet
  })
