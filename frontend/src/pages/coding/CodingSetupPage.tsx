import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Code2, ChevronRight, Terminal } from 'lucide-react'
import { useCreateCodingInterview } from '@/hooks'
import { Card, Button, Input, Select } from '@/components/ui'

const schema = z.object({
  role: z.string().min(2, 'Role is required'),
  company: z.string().optional(),
  language: z.string().min(1, 'Select a language'),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  number_of_questions: z.coerce.number().min(1).max(10),
})
type FormValues = z.infer<typeof schema>

const LANGUAGES = [
  { value: 'python', label: 'Python (3.11)' },
  { value: 'javascript', label: 'JavaScript (Node.js)' },
  { value: 'typescript', label: 'TypeScript (v5)' },
  { value: 'java', label: 'Java (Open JDK)' },
  { value: 'cpp', label: 'C++ (GCC 12)' },
  { value: 'go', label: 'Go (v1.21)' },
  { value: 'rust', label: 'Rust (2021 Edition)' },
]

export const CodingSetupPage = () => {
  const navigate = useNavigate()
  const { mutate: create, isPending, error } = useCreateCodingInterview()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      language: 'python',
      difficulty: 'medium',
      number_of_questions: 5,
    },
  })

  const onSubmit = (data: FormValues) => {
    create(
      {
        role: data.role,
        company: data.company || undefined,
        language: data.language,
        difficulty: data.difficulty,
        number_of_questions: data.number_of_questions,
      },
      {
        onSuccess: (interview) => {
          navigate(`/coding/${interview.id}`)
        },
      }
    )
  }

  const apiError =
    (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail

  return (
    <div className="max-w-xl mx-auto space-y-6 animate-fade-in">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-semibold">
          <Code2 size={14} className="text-amber-500" />
          <span>Monaco IDE Arena</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold dark:text-neutral-100 text-neutral-900 tracking-tight">
          Coding Challenge Arena
        </h1>
        <p className="dark:text-neutral-400 text-neutral-500 text-sm max-w-md mx-auto">
          Generates algorithmic problems with live execution, test runner, and time complexity checks.
        </p>
      </div>

      <Card className="border dark:border-surface-border border-lsurface-border dark:bg-surface-card bg-lsurface-card p-6 sm:p-8 shadow-sm">
        {apiError && (
          <div className="mb-5 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
          <div className="grid sm:grid-cols-2 gap-4">
            <Input
              label="Target Role"
              placeholder="e.g. Backend Engineer"
              error={errors.role?.message}
              {...register('role')}
            />

            <Input
              label="Company Target (Optional)"
              placeholder="e.g. Meta / Google / Stripe"
              error={errors.company?.message}
              {...register('company')}
            />
          </div>

          <Select
            label="Programming Language"
            options={LANGUAGES}
            error={errors.language?.message}
            {...register('language')}
          />

          <div className="grid sm:grid-cols-2 gap-4">
            <Select
              label="Problem Difficulty"
              options={[
                { value: 'easy', label: 'Easy (Basic DSA)' },
                { value: 'medium', label: 'Medium (LeetCode Medium)' },
                { value: 'hard', label: 'Hard (Advanced Graphs & DP)' },
              ]}
              error={errors.difficulty?.message}
              {...register('difficulty')}
            />

            <Input
              label="Number of Challenges"
              type="number"
              min={1}
              max={10}
              hint="1 to 10 challenges"
              error={errors.number_of_questions?.message}
              {...register('number_of_questions')}
            />
          </div>

          <div className="pt-2">
            <Button
              type="submit"
              variant="primary"
              className="w-full justify-center text-sm py-3.5 font-semibold"
              loading={isPending}
              icon={<Terminal size={16} />}
            >
              Launch Coding Arena <ChevronRight size={16} />
            </Button>
          </div>
        </form>
      </Card>

      <Card className="dark:bg-surface-raised bg-lsurface-raised border dark:border-surface-border border-lsurface-border p-5">
        <h3 className="font-semibold dark:text-neutral-100 text-neutral-900 text-xs uppercase tracking-wider mb-3 flex items-center gap-2">
          <Terminal size={14} className="text-amber-500" />
          IDE Feature Highlights
        </h3>
        <ol className="space-y-2">
          {[
            'Full Monaco Editor workspace supporting Python, TS, Java, C++, and Go.',
            'Instant Code Execution with stdout output and time complexity analysis.',
            'Theme sync matching platform light and dark settings.',
            'Comprehensive post-session evaluation with sample solution diffs.',
          ].map((step, i) => (
            <li key={i} className="flex gap-3 text-xs font-medium dark:text-neutral-400 text-neutral-600">
              <span className="w-5 h-5 rounded-full bg-amber-500/10 text-amber-500 flex items-center justify-center text-[10px] font-semibold shrink-0 mt-0.5">
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
