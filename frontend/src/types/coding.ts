// ── Create ───────────────────────────────────────────────────────────────────
export interface CreateCodingInterviewRequest {
  role: string
  company?: string
  language: string
  difficulty: 'easy' | 'medium' | 'hard'
  number_of_questions: number
}

// ── Interview ────────────────────────────────────────────────────────────────
// Matches CodingInterviewResponse schema exactly
export interface CodingInterview {
  id: number
  user_id: number
  role: string
  company: string | null
  language: string
  difficulty: string
  status: 'pending' | 'running' | 'completed'
  score: number | null        // int | None
  created_at: string
}

// ── Question ─────────────────────────────────────────────────────────────────
// Matches CodingQuestionResponse schema exactly
export interface CodingQuestion {
  id: number
  title: string
  description: string
  starter_code: string | null
  difficulty: string
  function_name: string | null
}

// ── Submit ───────────────────────────────────────────────────────────────────
export interface SubmitCodeRequest {
  interview_id: number
  question_id: number
  language: string
  code: string
}

// Matches EvaluationResponse schema exactly
export interface EvaluationResult {
  passed: boolean
  score: number               // int 0-100
  correctness: number         // int 0-100
  code_quality: number        // int 0-100
  time_complexity: string
  space_complexity: string
  strengths: string[]
  weaknesses: string[]
  bugs: string[]
  optimization_suggestions: string[]
  feedback: string
}

// Matches SubmissionResponse schema — next_question is dict | None (not a typed object)
export interface SubmissionResponse {
  evaluation: EvaluationResult
  completed: boolean
  score: number | null
  next_question: Record<string, unknown> | null
}

// ── Results / Progress ───────────────────────────────────────────────────────
export interface CodingInterviewResultResponse {
  interview_id: number
  status: string
  score: number | null
  completed_at: string | null
}

// Matches CodingInterviewProgressResponse exactly
export interface CodingInterviewProgress {
  interview_id: number
  status: string
  total_questions: number
  answered_questions: number
  remaining_questions: number
  current_score: number       // int
  progress_percentage: number // int
}

// ── Report ───────────────────────────────────────────────────────────────────
// Matches CodingInterviewReportResponse exactly
export interface CodingInterviewReport {
  overall_score: number       // int
  technical_level: string
  strengths: string[]
  weaknesses: string[]
  recommendation: string
  summary: string
}

// ── History ──────────────────────────────────────────────────────────────────
export interface CodingInterviewHistory {
  history: CodingInterview[]
}

// ── Dashboard ────────────────────────────────────────────────────────────────
export interface DashboardLatestInterview {
  id: number
  role: string
  company: string | null
  score: number | null
  status: string
}

// Matches CodingDashboardResponse exactly
export interface CodingDashboardStats {
  total_interviews: number
  completed_interviews: number
  pending_interviews: number
  average_score: number
  best_score: number
  total_questions: number
  total_submissions: number
  passed_submissions: number
  success_rate: number
  latest_interview: DashboardLatestInterview | null
}

// ── Leaderboard ──────────────────────────────────────────────────────────────
// Matches LeaderboardEntry schema exactly
export interface LeaderboardEntry {
  user_id: number
  user_name: string
  total_interviews: number
  best_score: number          // int
  average_score: number       // float
}

export interface LeaderboardResponse {
  leaderboard: LeaderboardEntry[]
}

// ── Draft ────────────────────────────────────────────────────────────────────
export interface CodingDraft {
  id: number
  user_id: number
  question_id: number
  code: string
  language: string
  updated_at: string
}

// ── WebSocket types ──────────────────────────────────────────────────────────
export type WsEventType =
  | 'start_interview'
  | 'submit_code'
  | 'autosave'
  | 'interview_started'
  | 'submission_result'
  | 'next_question'
  | 'interview_completed'
  | 'draft_saved'
  | 'error'

export interface WsMessage {
  type: WsEventType
  [key: string]: unknown
}

export interface WsQuestionPayload {
  id: number
  title: string
  description: string
  difficulty: string
  starter_code?: string
  function_name?: string
}
