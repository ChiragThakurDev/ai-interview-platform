import { useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Upload,
  FileText,
  Trash2,
  Download,
  Brain,
  AlertCircle,
  File,
  CheckCircle2,
} from 'lucide-react'
import { useMyResumes, useUploadResume, useDeleteResume } from '@/hooks'
import { Card, Button, Spinner, EmptyState, Modal, Badge } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import { formatDate, fileSizeLabel, cn } from '@/utils'
import { downloadResumeUrl } from '@/api'

export const ResumePage = () => {
  const { data: resumes, isLoading } = useMyResumes()
  const { mutate: upload, isPending: uploading, error: uploadError } = useUploadResume()
  const { mutate: deleteResume, isPending: deleting } = useDeleteResume()

  const inputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<number | null>(null)

  const handleFiles = (files: FileList | null) => {
    if (!files?.length) return
    const file = files[0]
    if (file.type !== 'application/pdf') {
      showToast('error', 'Only PDF files are supported.')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      showToast('error', 'File size must be under 5 MB.')
      return
    }

    upload(file, {
      onSuccess: () => showToast('success', 'Resume uploaded & analyzed successfully!'),
      onError: () => showToast('error', 'Failed to upload resume.'),
    })
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    handleFiles(e.dataTransfer.files)
  }

  const apiError =
    (uploadError as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* ── Header ────────────────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold dark:text-neutral-100 text-neutral-900 flex items-center gap-2.5">
            Resume Intelligence
          </h1>
          <p className="dark:text-neutral-400 text-neutral-600 mt-1 text-sm">
            Upload your resume for AI ATS parsing, skill gap analysis, and tailored interview recommendations.
          </p>
        </div>
      </div>

      {/* ── Upload Area ───────────────────────────────────────────────── */}
      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={cn(
            'border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center gap-4 cursor-pointer transition-all duration-300',
            dragOver
              ? 'border-brand-500 bg-brand-500/10 ring-4 ring-brand-500/20 scale-[1.01]'
              : 'dark:border-surface-border border-neutral-300 dark:hover:border-brand-500/50 hover:border-brand-500/40 dark:hover:bg-surface-hover hover:bg-lsurface-hover'
          )}
        >
          <div className={cn(
            'p-4 rounded-2xl transition-all duration-300',
            dragOver ? 'bg-brand-500 text-white' : 'dark:bg-surface-raised bg-lsurface-raised text-brand-500'
          )}>
            <Upload size={28} />
          </div>
          <div className="text-center">
            <p className="font-bold dark:text-neutral-100 text-neutral-900 text-base">
              {dragOver ? 'Drop PDF here to parse' : 'Click or Drag & Drop your Resume'}
            </p>
            <p className="text-xs dark:text-neutral-400 text-neutral-500 mt-1 font-medium">
              Supported format: PDF only (Max file size 5MB)
            </p>
          </div>

          {uploading && (
            <div className="flex items-center gap-2 text-brand-500 text-xs font-semibold bg-brand-500/10 px-4 py-2 rounded-xl">
              <Spinner size="xs" /> Extracting skills & parsing structure...
            </div>
          )}
        </div>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
          aria-label="Upload resume PDF"
        />

        {apiError && (
          <div className="mt-4 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold flex items-center gap-2">
            <AlertCircle size={15} /> {apiError}
          </div>
        )}
      </Card>

      {/* ── Resumes List ──────────────────────────────────────────────── */}
      <div className="space-y-4">
        <h2 className="text-xs font-semibold uppercase tracking-wider dark:text-neutral-400 text-neutral-500">
          Saved Resumes & Scorecards
        </h2>

        {isLoading && (
          <div className="flex justify-center py-12">
            <Spinner size="md" />
          </div>
        )}

        {!isLoading && (!resumes || resumes.length === 0) && (
          <EmptyState
            icon={<FileText size={36} />}
            title="No resumes uploaded yet"
            description="Upload your resume above to start your AI technical diagnosis."
          />
        )}

        {resumes && resumes.length > 0 && (
          <div className="space-y-3">
            {resumes.map((resume, i) => (
              <motion.div
                key={resume.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card">
                  <div className="flex items-center gap-3.5 min-w-0">
                    <div className="p-3 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 text-emerald-400 shrink-0 border border-emerald-500/20">
                      <File size={22} />
                    </div>
                    <div className="min-w-0">
                      <p className="font-bold dark:text-neutral-100 text-neutral-900 text-sm truncate">{resume.filename}</p>
                      <p className="text-xs dark:text-neutral-400 text-neutral-500 mt-0.5 font-medium">
                        {fileSizeLabel(resume.file_size)} · Uploaded {formatDate(resume.uploaded_at)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 flex-wrap shrink-0">
                    <Link to={`/resume/${resume.id}/analysis`}>
                      <Button size="xs" variant="primary" icon={<Brain size={14} />}>
                        AI Analysis
                      </Button>
                    </Link>
                    <Link to={`/interview?resumeId=${resume.id}`}>
                      <Button size="xs" variant="primary">
                        Practice Questions
                      </Button>
                    </Link>
                    <a
                      href={downloadResumeUrl(resume.id)}
                      target="_blank"
                      rel="noreferrer"
                      aria-label="Download resume"
                    >
                      <Button size="xs" variant="outline" icon={<Download size={13} />}>
                        PDF
                      </Button>
                    </a>
                    <Button
                      size="xs"
                      variant="danger"
                      onClick={() => setDeleteTarget(resume.id)}
                      aria-label="Delete resume"
                      icon={<Trash2 size={13} />}
                    />
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* ── Confirm Delete Modal ─────────────────────────────────────── */}
      <Modal
        open={deleteTarget !== null}
        onClose={() => setDeleteTarget(null)}
        title="Delete Resume?"
      >
        <p className="dark:text-neutral-300 text-neutral-600 text-sm mb-6 leading-relaxed">
          Are you sure you want to remove this resume? This will also remove the associated AI analysis and practice suggestions.
        </p>
        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={() => setDeleteTarget(null)}>
            Cancel
          </Button>
          <Button
            variant="danger"
            loading={deleting}
            onClick={() => {
              if (deleteTarget !== null) {
                deleteResume(deleteTarget, {
                  onSuccess: () => {
                    setDeleteTarget(null)
                    showToast('info', 'Resume removed')
                  },
                })
              }
            }}
          >
            Delete Resume
          </Button>
        </div>
      </Modal>
    </div>
  )
}
