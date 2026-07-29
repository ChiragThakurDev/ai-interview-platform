import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui'
import { Home } from 'lucide-react'

export const NotFoundPage = () => (
  <div className="flex flex-col items-center justify-center min-h-screen dark:bg-surface-base bg-lsurface-base text-center p-6">
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <p className="text-7xl font-bold text-brand-500">404</p>
      <h1 className="text-xl font-semibold dark:text-neutral-100 text-neutral-900">Page not found</h1>
      <p className="text-sm dark:text-neutral-500 text-neutral-500 max-w-xs">The page you're looking for doesn't exist or has been moved.</p>
      <Link to="/dashboard">
        <Button className="mt-2"><Home size={14} /> Back to Dashboard</Button>
      </Link>
    </motion.div>
  </div>
)
