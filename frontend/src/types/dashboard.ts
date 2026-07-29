// GET /dashboard  →  DashboardResponse
export interface DashboardStats {
  total_interviews: number
  average_score: number
  highest_score: number
  total_questions_answered: number
  recent_interviews: RecentInterview[]
}

export interface RecentInterview {
  id: number
  role: string
  difficulty: string
  score: number | null
  created_at: string
}

// GET /dashboard/performance-history  →  { history: [...] }
export interface PerformanceHistory {
  interview_id: number
  role: string
  difficulty: string
  score: number
  date: string
}
export interface PerformanceHistoryResponse {
  history: PerformanceHistory[]
}

// GET /dashboard/progress  →  ProgressResponse
export interface ProgressStats {
  current_score: number
  previous_score: number | null
  improvement: number
  // backend values: improving | declining | no_change | no_interviews | first_interview
  trend: string
}

// GET /dashboard/skills  →  SkillReportResponse
export interface SkillReport {
  id: number
  user_id: number
  strong_skills: string[]
  weak_skills: string[]
  recommended_topics: string[]
  summary: string
  created_at: string
}

// GET /dashboard/analytics  →  AnalyticsResponse
// difficulty_stats values are AVERAGE SCORES, not counts
export interface DifficultyStats {
  easy: number
  medium: number
  hard: number
}
export interface AnalyticsStats {
  score_distribution: Record<string, number>  // e.g. { "0-20": 3, "21-40": 5, ... }
  difficulty_stats: DifficultyStats            // average score per difficulty
  role_stats: Record<string, number>           // role → interview count
}

// GET /dashboard/topics  →  TopicAnalysisResponse  →  { topics: [...] }
export interface TopicItem {
  topic: string
  average_score: number
  total_questions: number
}
export interface TopicAnalysis {
  topics: TopicItem[]
}
