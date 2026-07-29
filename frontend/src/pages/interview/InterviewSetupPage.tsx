import { useNavigate, useSearchParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Brain, ChevronRight, Sliders } from 'lucide-react'
import { useMyResumes, useCreateInterview } from '@/hooks'
import { Card, Button, Select, Input } from '@/components/ui'

const schema = z.object({
  resumeId: z.string().min(1, 'Select a resume'),
  role: z.string().min(2, 'Role is required'),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  number_of_questions: z.coerce.number().min(3).max(20),
})
type FormValues = z.infer<typeof schema>

export const InterviewSetupPage = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const defaultResumeId = searchParams.get('resumeId') ?? ''

  const { data: resumes, isLoading: loadingResumes } = useMyResumes()
  const { mutate: create, isPending, error } = useCreateInterview()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      resumeId: defaultResumeId,
      difficulty: 'medium',
      number_of_questions: 10,
    },
  })

  const onSubmit = (data: FormValues) => {
    create(
      {
        resumeId: Number(data.resumeId),
        body: {
          role: data.role,
          difficulty: data.difficulty,
          number_of_questions: data.number_of_questions,
        },
      },
      {
        onSuccess: (res) => {
          navigate(`/interview/${res.interview.id}/session`)
        },
      }
    )
  }

  const resumeOptions = resumes
    ? resumes.map((r) => ({ value: String(r.id), label: r.filename }))
    : []

  const apiError =
    (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  return (
    <div className="max-w-xl mx-auto space-y-6 animate-fade-in">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-500 text-xs font-semibold">
          <Brain size={14} className="text-brand-500" />
          <span>Technical Interview Generator</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
          Configure Mock Interview
        </h1>
        <p className="dark:text-neutral-400 text-neutral-500 text-sm max-w-md mx-auto">
          AI will parse your resume context to build a tailored role-based technical session.
        </p>
      </div>

      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-6 sm:p-8 shadow-sm">
        {apiError && (
          <div className="mb-5 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
          <Select
            label="Selected Resume"
            options={[
              { value: '', label: loadingResumes ? 'Loading candidate resumes…' : 'Select a candidate resume' },
              ...resumeOptions,
            ]}
            error={errors.resumeId?.message}
            {...register('resumeId')}
          />

          <Input
            label="Target Engineering Role"
            placeholder="e.g. Senior Full Stack Engineer / Systems Architect"
            error={errors.role?.message}
            {...register('role')}
          />

          <div className="grid sm:grid-cols-2 gap-4">
            <Select
              label="Evaluation Difficulty"
              options={[
                { value: 'easy', label: 'Easy (Junior)' },
                { value: 'medium', label: 'Medium (Mid-Level)' },
                { value: 'hard', label: 'Hard (Senior / Staff)' },
              ]}
              error={errors.difficulty?.message}
              {...register('difficulty')}
            />

            <Input
              label="Question Count"
              type="number"
              min={3}
              max={20}
              error={errors.number_of_questions?.message}
              hint="3 to 20 questions"
              {...register('number_of_questions')}
            />
          </div>

          <div className="pt-2">
            <Button
              type="submit"
              variant="primary"
              className="w-full justify-center text-sm py-3.5 font-semibold"
              loading={isPending}
              icon={<Brain size={16} />}
            >
              Generate AI Session <ChevronRight size={16} />
            </Button>
          </div>
        </form>
      </Card>

      <Card className="dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border p-5">
        <h3 className="font-semibold dark:text-neutral-100 text-neutral-900 text-xs uppercase tracking-wider mb-3 flex items-center gap-2">
          <Sliders size={14} className="text-brand-500" />
          Interactive Evaluation Flow
        </h3>
        <ol className="space-y-2">
          {[
            'AI analyzes resume skills to generate customized interview questions.',
            'Respond using text dictation or integrated voice microphone.',
            'Receive real-time feedback scores and candidate strengths analysis.',
            'View comprehensive final performance radar report.',
          ].map((step, i) => (
            <li key={i} className="flex gap-3 text-xs font-medium dark:text-neutral-400 text-neutral-600">
              <span className="w-5 h-5 rounded-full bg-brand-500/10 text-brand-500 flex items-center justify-center text-[10px] font-semibold shrink-0 mt-0.5">
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
      </Card>
    </div>
  )
}
