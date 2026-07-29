import { useEffect } from 'react'
import { RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { router } from '@/routes'
import { useThemeStore, applyTheme } from '@/store'
import { ToastProvider, AppToaster } from '@/components/ui'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,                 // never auto-retry — 401s are handled by interceptor
      refetchOnWindowFocus: false,  // prevent re-fetch loop on tab focus
      staleTime: 60_000,
    },
    mutations: { retry: 0 },
  },
})

function ThemeInitializer() {
  const { theme } = useThemeStore()
  useEffect(() => { applyTheme(theme) }, [theme])
  return null
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <ThemeInitializer />
        {/* AppToaster registers the global showToast singleton inside ToastProvider */}
        <AppToaster />
        <RouterProvider router={router} />
        {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
      </ToastProvider>
    </QueryClientProvider>
  )
}

export default App
