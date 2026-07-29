export interface User {
  id: number
  name: string
  email: string
  role: string
  is_active: boolean
  is_verified?: boolean
  created_at?: string
}
