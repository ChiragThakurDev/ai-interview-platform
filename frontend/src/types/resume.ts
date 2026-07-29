export interface Resume {
  id: number
  filename: string
  file_path: string
  file_size: number
  content_type: string
  uploaded_at: string
  user_id: number
}

// POST /ai/analyze/{resume_id}
// Matches backend ResumeAnalysis model exactly
export interface ResumeAnalysis {
  id: number
  resume_id: number
  overall_score: number
  strengths: string[]
  weaknesses: string[]
  suggestions: string[]
  recommended_roles: string[]
  summary: string
  created_at: string
}

// POST /roadmap/generate  →  LearningRoadmapResponse
export interface WeeklyPlan {
  week: number
  focus: string
  topics: string[]
}
export interface Roadmap {
  title: string
  duration: string
  weekly_plan: WeeklyPlan[]
}
