import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  createChatSession,
  getChatSessions,
  getChatMessages,
  sendMessage,
  deleteChatSession,
} from '@/api'
import type { ChatSessionCreate, ChatMessageCreate } from '@/types'

export const useChatSessions = () =>
  useQuery({
    queryKey: ['chat-sessions'],
    queryFn: getChatSessions,
    staleTime: 60 * 1000,
  })

export const useChatMessages = (sessionId: number, enabled = true) =>
  useQuery({
    queryKey: ['chat-messages', sessionId],
    queryFn: () => getChatMessages(sessionId),
    enabled,
    staleTime: 30 * 1000,
  })

export const useCreateChatSession = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (body: ChatSessionCreate) => createChatSession(body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-sessions'] })
    },
  })
}

export const useSendMessage = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ sessionId, body }: { sessionId: number; body: ChatMessageCreate }) =>
      sendMessage(sessionId, body),
    onSuccess: (_, { sessionId }) => {
      queryClient.invalidateQueries({ queryKey: ['chat-messages', sessionId] })
    },
  })
}

export const useDeleteChatSession = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (sessionId: number) => deleteChatSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-sessions'] })
    },
  })
}
