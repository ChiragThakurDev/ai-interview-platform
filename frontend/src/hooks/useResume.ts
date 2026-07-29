import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { uploadResume, getMyResumes, deleteResume, analyzeResume } from '@/api'
import { showToast } from '@/components/ui'

export const useMyResumes = () =>
  useQuery({
    queryKey: ['resumes'],
    queryFn: getMyResumes,
    staleTime: 5 * 60 * 1000,
  })

export const useUploadResume = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (file: File) => uploadResume(file),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['resumes'] })
      showToast.success(`"${data.filename}" uploaded successfully.`)
    },
    onError: () => showToast.error('Failed to upload resume.'),
  })
}

export const useDeleteResume = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (resumeId: number) => deleteResume(resumeId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['resumes'] })
      showToast.success('Resume deleted.')
    },
    onError: () => showToast.error('Failed to delete resume.'),
  })
}

// POST /ai/analyze/{resume_id}
export const useAnalyzeResume = (resumeId: number, enabled = false) =>
  useQuery({
    queryKey: ['resume-analysis', resumeId],
    queryFn: () => analyzeResume(resumeId),
    enabled,
    staleTime: 10 * 60 * 1000,
    retry: false,
  })

export const useTriggerAnalysis = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (resumeId: number) => analyzeResume(resumeId),
    onSuccess: (_, resumeId) => {
      qc.invalidateQueries({ queryKey: ['resume-analysis', resumeId] })
      showToast.success('AI analysis complete!')
    },
    onError: () => showToast.error('Analysis failed. Please try again.'),
  })
}
