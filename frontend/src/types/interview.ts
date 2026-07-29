// ── Generate ────────────────────────────────────────────────────────────────
export interface GenerateInterviewRequest {
  role: string
  difficulty: 'easy' | 'medium' | 'hard'
  number_of_questions: number
}

// GET /interview/my  →  list[InterviewListResponse]
export interface Interview {
  id: number
  user_id: number
  resume_id: number
  title: string
  role: string
  difficulty: string
  created_at: string
}

export interface InterviewQuestion {
  question: string
}

export interface GenerateInterviewResponse {
  interview: Interview
  questions: InterviewQuestion[]
}

// ── Session ──────────────────────────────────────────────────────────────────
export interface StartInterviewResponse {
  interview_id: number
  status: string
  current_question: number
  question: string
}

export interface CurrentQuestionResponse {
  interview_id: number
  current_question: number
  total_questions: number
  question: string
}

export interface SubmitAnswerRequest {
  answer: string
}

// backend: score is int | None, feedback is str | None
export interface SubmitAnswerResponse {
  interview_completed: boolean
  current_question: number | null
  next_question: string | null
  score: number | null        // 0-100 integer
  feedback: string | null
  message: string
}

export interface FinishInterviewResponse {
  interview_id: number
  status: string
  score: number | null
  duration: number | null
  message: string
}

// ── Results  GET /interview/{id}/results ─────────────────────────────────────
export interface QuestionResultResponse {
  id: number
  question: string
  answer: string | null
  score: number | null        // float from backend
  feedback: string | null
}

export interface InterviewInfoResponse {
  id: number
  role: string
  difficulty: string
  status: string
  created_at: string
}

// Embedded report inside /results  (schema: interview_result.InterviewReportResponse)
export interface InterviewReportInResult {
  overall_score: number | null
  strengths: string | null
  weaknesses: string | null
  recommendations: string | null
  summary: string | null
}

export interface InterviewResult {
  interview: InterviewInfoResponse
  questions: QuestionResultResponse[]
  report: InterviewReportInResult | null
}

// ── Full report  GET /interview/{id}/report ───────────────────────────────────
// schema: interview_report.InterviewReportResponse — strengths/weaknesses are list[str]
export interface InterviewReport {
  id: number
  interview_id: number
  overall_score: number       // 0-100 integer
  technical_level: string
  communication: string
  strengths: string[]
  weaknesses: string[]
  recommendation: string
  summary: string
  created_at: string
  // convenience fields added by some pages (not from backend directly)
  role?: string
  difficulty?: string
}

// ── Interview Answers  /answers/{question_id} ─────────────────────────────────
export interface SubmitInterviewAnswerRequest {
  answer: string
}

export interface InterviewAnswerResponse {
  id: number
  question_id: number
  answer: string
  score: number
  feedback: string
  created_at: string
}
