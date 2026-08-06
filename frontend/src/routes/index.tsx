import { createBrowserRouter, Navigate } from 'react-router-dom'

import { AppLayout } from '@/layouts/AppLayout'
import { AuthLayout } from '@/layouts/AuthLayout'
import { ProtectedRoute } from '@/layouts/ProtectedRoute'

import { LoginPage } from '@/pages/auth/LoginPage'
import { RegisterPage } from '@/pages/auth/RegisterPage'
import { ForgotPasswordPage } from '@/pages/auth/ForgotPasswordPage'
import { VerifyEmailPage } from '@/pages/auth/VerifyEmailPage'
import { ResetPasswordPage } from '@/pages/auth/ResetPasswordPage'

import { LandingPage } from '@/pages/LandingPage'

import { DashboardPage } from '@/pages/dashboard/DashboardPage'

import { ResumePage } from '@/pages/resume/ResumePage'
import { ResumeAnalysisPage } from '@/pages/resume/ResumeAnalysisPage'

import { InterviewSetupPage } from '@/pages/interview/InterviewSetupPage'
import { InterviewSessionPage } from '@/pages/interview/InterviewSessionPage'
import { InterviewReportPage } from '@/pages/interview/InterviewReportPage'
import { LiveInterviewPage } from '@/pages/interview/LiveInterviewPage'

import { VideoRoomLobbyPage } from '@/pages/video-room/VideoRoomLobbyPage'
import { VideoRoomSessionPage } from '@/pages/video-room/VideoRoomSessionPage'

import { CodingSetupPage } from '@/pages/coding/CodingSetupPage'
import { CodingSessionPage } from '@/pages/coding/CodingSessionPage'
import { CodingReportPage } from '@/pages/coding/CodingReportPage'

import { HistoryPage } from '@/pages/history/HistoryPage'
import { LeaderboardPage } from '@/pages/leaderboard/LeaderboardPage'
import { ProfilePage } from '@/pages/profile/ProfilePage'
import { SettingsPage } from '@/pages/settings/SettingsPage'
import { ApiKeysPage } from '@/pages/settings/ApiKeysPage'
import { ChatPage } from '@/pages/chat/ChatPage'
import { AdminDashboardPage } from '@/pages/admin/AdminDashboardPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

export const router = createBrowserRouter([
  // ─── Public landing ────────────────────────────────────────────
  { path: '/', element: <LandingPage /> },

  // ─── Public auth routes ────────────────────────────────────────
  {
    element: <AuthLayout />,
    children: [
      { path: '/login', element: <LoginPage /> },
      { path: '/register', element: <RegisterPage /> },
      { path: '/forgot-password', element: <ForgotPasswordPage /> },
      { path: '/verify-email', element: <VerifyEmailPage /> },
      { path: '/reset-password', element: <ResetPasswordPage /> },
    ],
  },

  // ─── Protected app routes ─────────────────────────────────────
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          // Default redirect after login
          { path: '/home', element: <Navigate to="/dashboard" replace /> },

          // Dashboard
          { path: '/dashboard', element: <DashboardPage /> },

          // Resume
          { path: '/resume', element: <ResumePage /> },
          { path: '/resume/:resumeId/analysis', element: <ResumeAnalysisPage /> },

          // Technical interview
          { path: '/interview', element: <InterviewSetupPage /> },
          { path: '/interview/:interviewId/session', element: <InterviewSessionPage /> },
          { path: '/results/:interviewId', element: <InterviewReportPage /> },
          { path: '/interview/:id/live', element: <LiveInterviewPage /> },

          // Standalone two-person video rooms
          { path: '/video-room', element: <VideoRoomLobbyPage /> },
          { path: '/room/:roomId', element: <VideoRoomSessionPage /> },

          // Coding interview
          { path: '/coding', element: <CodingSetupPage /> },
          { path: '/coding/:interviewId', element: <CodingSessionPage /> },
          { path: '/coding/:interviewId/report', element: <CodingReportPage /> },

          // AI Chat Assistant
          { path: '/chat', element: <ChatPage /> },

          // Other pages
          { path: '/history', element: <HistoryPage /> },
          { path: '/leaderboard', element: <LeaderboardPage /> },
          { path: '/profile', element: <ProfilePage /> },
          { path: '/settings', element: <SettingsPage /> },
          { path: '/settings/api-keys', element: <ApiKeysPage /> },

          // Admin
          { path: '/admin', element: <AdminDashboardPage /> },
        ],
      },
    ],
  },

  // ─── 404 ──────────────────────────────────────────────────────
  { path: '*', element: <NotFoundPage /> },
])
