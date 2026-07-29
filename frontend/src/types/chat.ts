export interface ChatSession {
  id: number
  title: string
  created_at: string
}

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ChatSessionCreate {
  title: string
}

export interface ChatMessageCreate {
  message: string
}
