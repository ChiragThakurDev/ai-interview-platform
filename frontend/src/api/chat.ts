import { apiClient } from './client'
import type { ChatSession, ChatMessage, ChatSessionCreate, ChatMessageCreate } from '@/types'

export const createChatSession = async (body: ChatSessionCreate): Promise<ChatSession> => {
  const { data } = await apiClient.post<ChatSession>('/chat/sessions', body)
  return data
}

export const getChatSessions = async (): Promise<ChatSession[]> => {
  const { data } = await apiClient.get<ChatSession[]>('/chat/sessions')
  return data
}

export const getChatMessages = async (sessionId: number): Promise<ChatMessage[]> => {
  const { data } = await apiClient.get<ChatMessage[]>(`/chat/sessions/${sessionId}/messages`)
  return data
}

export const sendMessage = async (
  sessionId: number,
  body: ChatMessageCreate
): Promise<ChatMessage> => {
  const { data } = await apiClient.post<ChatMessage>(
    `/chat/sessions/${sessionId}/message`,
    body
  )
  return data
}

export const deleteChatSession = async (sessionId: number) => {
  const { data } = await apiClient.delete(`/chat/sessions/${sessionId}`)
  return data
}
