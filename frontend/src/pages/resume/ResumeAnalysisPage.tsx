import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Brain, Map, CheckCircle, XCircle, Lightbulb, RefreshCw, Sparkles, Target } from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { analyzeResume, generateRoadmap } from '@/api'
import { useSkillReport } from '@/hooks'
import { Card, Button, Spinner, Badge, EmptyState } from '@/components/ui'
import { showToast } from '@/components/ui/Toast'
import type { ResumeAnalysis, Roadmap } from '@/types'

export const ResumeAnalysisPage = () => {
  const { resumeId } = useParams<{ resumeId: string }>()
  const qc = useQueryClient()

  // POST /ai/analyze/{resume_id}  — trigger analysis
  const {
    data: analysis,
    isLoading: loadingAnalysis,
    error: analysisError,
  } = useQuery({
    queryKey: ['resume-analysis', resumeId],
    queryFn: () => analyzeResume(Number(resumeId)),
    enabled: !!resumeId,
    staleTime: 10 * 60 * 1000,
    retry: false,
  })

  const { mutate: reanalyze, isPending: reanalyzing } = useMutation({
    mutationFn: () => analyzeResume(Number(resumeId)),
    onSuccess: (data) => {
      qc.setQueryData(['resume-analysis', resumeId], data)
      showToast.success('Resume re-analyzed!')
    },
    onError: () => showToast.error('Analysis failed.'),
  })

  // GET /dashboard/skills  — skill report based on interview history
  const { data: skillReport, isLoading: loadingSkillReport } = useSkillReport()

  // POST /roadmap/generate  — generate a roadmap from skill summary
  const {
    data: roadmap,
    mutate: generateRoadmapMutation,
    isPending: generatingRoadmap,
  } = useMutation({
    mutationFn: (summary: string) => generateRoadmap(summary),
    onSuccess: () => showToast.success('Learning roadmap generated!'),
    onError:   () => showToast.error('Failed to generate roadmap.'),
  })

  const buildRoadmapSource = () => {
    if (skillReport) {
      return [
        skillReport.summary,
        `Weak skills: ${skillReport.weak_skills.join(', ')}`,
        `Recommended topics: ${skillReport.recommended_topics.join(', ')}`,
      ].filter(Boolean).join('\n')
    }

    if (analysis) {
      return [
        analysis.summary,
        `Weaknesses: ${analysis.weaknesses.join(', ')}`,
        `Suggestions: ${analysis.suggestions.join(', ')}`,
        `Target roles: ${analysis.recommended_roles.join(', ')}`,
      ].filter(Boolean).join('\n')
    }

    return ''
  }

  const handleGenerateRoadmap = () => {
    const source = buildRoadmapSource()

    if (!source) {
      showToast.error('Run resume analysis first.')
      return
    }

    generateRoadmapMutation(source)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link to="/resume">
            <Button variant="ghost" size="sm"><ArrowLeft size={14} /> Back</Button>
          </Link>
          <div>
            <h1 className="text-lg font-semibold dark:text-neutral-100 text-neutral-900">Resume Analysis</h1>
            <p className="text-xs dark:text-neutral-500 text-neutral-500 mt-0.5">AI-powered resume parsing and skill breakdown</p>
          </div>
        </div>
        <Button
          variant="secondary"
          size="sm"
          onClick={() => reanalyze()}
          loading={reanalyzing}
        >
          <RefreshCw size={13} /> Re-analyze
        </Button>
      </div>

      {/* ── AI Resume Analysis ─────────────────────────── */}
      <section>
        <h2 className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <Brain size={13} className="text-brand-500" /> Resume Content Analysis
        </h2>

        {loadingAnalysis && <div className="flex justify-center py-10"><Spinner /></div>}

        {analysisError && (
          <Card className="text-center py-8">
            <EmptyState
              icon={<Brain size={28} />}
              title="No analysis yet"
              description="Click 'Re-analyze' to run AI parsing on your resume."
              action={
                <Button size="sm" loading={reanalyzing} onClick={() => reanalyze()}>
                  Run Analysis
                </Button>
              }
              className="py-4"
            />
          </Card>
        )}

        {analysis && (
          <div className="space-y-4">
            {/* Summary */}
            {analysis.summary && (
              <Card>
                <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-2">Summary</p>
                <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{analysis.summary}</p>
              </Card>
            )}

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Skills */}
              {analysis.skills?.length > 0 && (
                <Card>
                  <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3">Skills</p>
                  <div className="flex flex-wrap gap-1.5">
                    {analysis.skills.map((s) => (
                      <Badge key={s} variant="info" size="xs">{s}</Badge>
                    ))}
                  </div>
                </Card>
              )}

              {/* Languages */}
              {analysis.languages?.length > 0 && (
                <Card>
                  <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3">Languages</p>
                  <div className="flex flex-wrap gap-1.5">
                    {analysis.languages.map((l) => (
                      <Badge key={l} variant="success" size="xs">{l}</Badge>
                    ))}
                  </div>
                </Card>
              )}

              {/* Certifications */}
              {analysis.certifications?.length > 0 && (
                <Card>
                  <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3">Certifications</p>
                  <div className="flex flex-wrap gap-1.5">
                    {analysis.certifications.map((c) => (
                      <Badge key={c} variant="orange" size="xs">{c}</Badge>
                    ))}
                  </div>
                </Card>
              )}
            </div>

            {/* Experience & Education */}
            {(analysis.experience || analysis.education) && (
              <div className="grid sm:grid-cols-2 gap-4">
                {analysis.experience && (
                  <Card>
                    <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-2">Experience</p>
                    <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{analysis.experience}</p>
                  </Card>
                )}
                {analysis.education && (
                  <Card>
                    <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-2">Education</p>
                    <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed">{analysis.education}</p>
                  </Card>
                )}
              </div>
            )}

            {/* Projects */}
            {analysis.projects?.length > 0 && (
              <Card>
                <p className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3">Projects</p>
                <ul className="space-y-1.5">
                  {analysis.projects.map((p, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm dark:text-neutral-300 text-neutral-700">
                      <span className="w-1 h-1 rounded-full bg-brand-500 mt-2 shrink-0" />
                      {p}
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* CTA to start interview */}
            <div className="flex flex-wrap gap-2">
              <Link to={`/interview?resumeId=${resumeId}`}>
                <Button size="sm"><Brain size={13} /> Practice Interview</Button>
              </Link>
            </div>

            <Card className="overflow-hidden border-0 dark:bg-gradient-to-br dark:from-surface-card dark:via-surface-raised dark:to-brand-950/30 bg-gradient-to-br from-white via-lsurface-raised to-brand-50 shadow-lg">
              <div className="flex flex-col lg:flex-row lg:items-center gap-5">
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-11 h-11 rounded-2xl bg-brand-500 text-white flex items-center justify-center shadow-lg shadow-brand-500/25 shrink-0">
                    <Map size={21} />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <p className="text-sm font-bold dark:text-neutral-100 text-neutral-900">Learning Roadmap</p>
                      <Badge variant="info" size="xs">AI Plan</Badge>
                    </div>
                    <p className="text-sm dark:text-neutral-300 text-neutral-600 leading-relaxed">
                      Turn this analysis into a focused weekly plan with topics, weak areas, and interview prep milestones.
                    </p>
                    <div className="grid sm:grid-cols-3 gap-2 mt-4">
                      {[
                        { icon: Target, label: 'Targets gaps' },
                        { icon: Sparkles, label: 'Weekly focus' },
                        { icon: CheckCircle, label: 'Prep ready' },
                      ].map((item) => (
                        <div key={item.label} className="flex items-center gap-2 rounded-lg dark:bg-surface-base/70 bg-white/75 px-3 py-2 text-xs font-semibold dark:text-neutral-300 text-neutral-700 border dark:border-surface-border border-lsurface-border">
                          <item.icon size={13} className="text-brand-500" />
                          {item.label}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <Button
                  variant="primary"
                  size="sm"
                  loading={generatingRoadmap}
                  onClick={handleGenerateRoadmap}
                  className="lg:self-center"
                >
                  <Sparkles size={13} /> Generate Roadmap
                </Button>
              </div>
            </Card>
          </div>
        )}
      </section>

      {/* ── Skill Report (from interviews) ─────────────── */}
      <section>
        <h2 className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <CheckCircle size={13} className="text-green-500" /> Skill Report (based on interview history)
        </h2>

        {loadingSkillReport && <div className="flex justify-center py-8"><Spinner size="sm" /></div>}

        {!loadingSkillReport && !skillReport && (
          <Card className="text-center py-8">
            <EmptyState
              title="No skill report yet"
              description="Complete at least one technical interview to generate your skill report."
              action={<Link to="/interview"><Button size="sm">Start Interview</Button></Link>}
              className="py-4"
            />
          </Card>
        )}

        {skillReport && (
          <div className="space-y-4">
            <Card>
              <p className="text-sm dark:text-neutral-300 text-neutral-700 leading-relaxed mb-4">{skillReport.summary}</p>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs font-semibold text-green-500 mb-2 flex items-center gap-1.5">
                    <CheckCircle size={12} /> Strong Skills
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {skillReport.strong_skills.map((s) => (
                      <Badge key={s} variant="success" size="xs">{s}</Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-xs font-semibold text-red-400 mb-2 flex items-center gap-1.5">
                    <XCircle size={12} /> Weak Skills
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {skillReport.weak_skills.map((s) => (
                      <Badge key={s} variant="danger" size="xs">{s}</Badge>
                    ))}
                  </div>
                </div>
              </div>
              {skillReport.recommended_topics?.length > 0 && (
                <div className="mt-4 pt-4 border-t dark:border-surface-border border-lsurface-border">
                  <p className="text-xs font-semibold text-yellow-500 mb-2 flex items-center gap-1.5">
                    <Lightbulb size={12} /> Recommended Topics
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {skillReport.recommended_topics.map((t) => (
                      <Badge key={t} variant="warning" size="xs">{t}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {!roadmap && (
              <Card className="dark:bg-surface-raised bg-lsurface-raised">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <p className="text-sm font-bold dark:text-neutral-100 text-neutral-900">Build a roadmap from this skill report</p>
                    <p className="text-xs dark:text-neutral-400 text-neutral-500 mt-1">
                      Uses weak skills and recommended topics for a more personalized plan.
                    </p>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    loading={generatingRoadmap}
                    onClick={handleGenerateRoadmap}
                  >
                    <Map size={13} /> Generate
                  </Button>
                </div>
              </Card>
            )}
          </div>
        )}
      </section>

      {/* ── Learning Roadmap ────────────────────────────── */}
      {roadmap && (
        <section>
          <h2 className="text-xs font-semibold dark:text-neutral-400 text-neutral-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <Map size={13} className="text-brand-500" /> Learning Roadmap — {roadmap.title}
            <span className="ml-1 dark:text-neutral-600 text-neutral-400">({roadmap.duration})</span>
          </h2>
          <div className="space-y-2">
            {roadmap.weekly_plan.map((week) => (
              <motion.div
                key={week.week}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: week.week * 0.05 }}
              >
                <Card className="p-3">
                  <div className="flex items-start gap-3">
                    <span className="w-6 h-6 rounded-md bg-brand-500/10 text-brand-500 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                      {week.week}
                    </span>
                    <div className="flex-1">
                      <p className="text-sm font-medium dark:text-neutral-200 text-neutral-800 mb-2">{week.focus}</p>
                      <div className="flex flex-wrap gap-1.5">
                        {week.topics.map((t) => (
                          <span key={t} className="text-xs px-2 py-0.5 rounded dark:bg-surface-raised bg-lsurface-raised dark:text-neutral-400 text-neutral-600">
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
