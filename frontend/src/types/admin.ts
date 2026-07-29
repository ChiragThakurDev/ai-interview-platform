// GET /admin/dashboard
export interface AdminDashboardStats {
  total_users: number
  active_users: number
  inactive_users: number
  total_interviews: number
  completed_interviews: number
  pending_interviews: number
  total_reports: number
  average_score: number
}

// GET /admin/activity
export interface AdminRecentUser {
  id: number
  name: string
  email: string
  created_at: string
}
export interface AdminRecentInterview {
  id: number
  role: string
  difficulty: string
  status: string
  created_at: string
}
export interface AdminRecentReport {
  id: number
  interview_id: number
  overall_score: number
  created_at: string
}
export interface AdminActivity {
  recent_users: AdminRecentUser[]
  recent_interviews: AdminRecentInterview[]
  recent_reports: AdminRecentReport[]
}

// GET /admin/users
export interface AdminUser {
  id: number
  name: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

// GET /admin/users/search
export interface AdminUserSearchResult {
  page: number
  limit: number
  total: number
  users: AdminUser[]
}

// GET /admin/analytics — actual shapes from repository layer:
// registrations  → { "Jan": 5, "Feb": 3, ... }   (dict month→count)
// interviews     → { "completed": 10, "pending": 4 }
// popular_roles  → [{ role: string, count: number }]  (the only real array)
// difficulty_distribution → { "easy": 5, "medium": 10, "hard": 3 }
// score_distribution      → { "0-20": 2, "21-40": 5, "41-60": 8, "61-80": 4, "81-100": 1 }
export interface AdminAnalytics {
  registrations: Record<string, number>
  interviews: { completed: number; pending: number }
  popular_roles: Array<{ role: string; count: number }>
  difficulty_distribution: { easy: number; medium: number; hard: number }
  score_distribution: Record<string, number>
}
