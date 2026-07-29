import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

// Apply saved theme before first paint to avoid flash
const saved = localStorage.getItem('theme-storage')
if (saved) {
  try {
    const parsed = JSON.parse(saved)
    const theme = parsed?.state?.theme ?? 'dark'
    document.documentElement.classList.add(theme)
  } catch {
    document.documentElement.classList.add('dark')
  }
} else {
  document.documentElement.classList.add('dark')
}

const root = document.getElementById('root')
if (!root) throw new Error('Root element #root not found in index.html')

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>
)
