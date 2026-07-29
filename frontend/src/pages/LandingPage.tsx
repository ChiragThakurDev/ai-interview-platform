import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Zap, Brain, Code2, Trophy, BarChart3, FileText,
  ArrowRight, CheckCircle, Star, Play, Shield,
  MessageSquare, TrendingUp, Users, Target,
  ChevronRight, Github, Twitter,
} from 'lucide-react'
import { useAuthStore } from '@/store'

const fadeUp = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.5 } } }
const stagger = { show: { transition: { staggerChildren: 0.1 } } }

const FEATURES = [
  {
    icon: Brain, color: 'bg-purple-500/10 text-purple-400', border: 'border-purple-500/20',
    title: 'AI-Powered Behavioral Interviews',
    desc: 'Generate custom technical interviews from your resume. Get real-time AI evaluation on every answer with detailed feedback and scores.',
  },
  {
    icon: Code2, color: 'bg-brand-500/10 text-brand-400', border: 'border-brand-500/20',
    title: 'Coding Interview Simulator',
    desc: 'Solve real DSA challenges in a Monaco-powered editor. Instant test-case execution, multi-language support, and AI-driven code review.',
  },
  {
    icon: FileText, color: 'bg-emerald-500/10 text-emerald-400', border: 'border-emerald-500/20',
    title: 'Resume Analysis',
    desc: 'Upload your resume and get an AI-powered breakdown — strengths, gaps, ATS score, and tailored suggestions to stand out.',
  },
  {
    icon: BarChart3, color: 'bg-amber-500/10 text-amber-400', border: 'border-amber-500/20',
    title: 'Skill Reports & Analytics',
    desc: 'Deep-dive into your performance history. Identify weak topics, track improvement over time, and benchmark against peers.',
  },
  {
    icon: MessageSquare, color: 'bg-pink-500/10 text-pink-400', border: 'border-pink-500/20',
    title: 'AI Chat Assistant',
    desc: 'Ask anything — system design, algorithms, behavioral tips. Voice input, read-aloud responses, and quick-prompt shortcuts.',
  },
  {
    icon: TrendingUp, color: 'bg-cyan-500/10 text-cyan-400', border: 'border-cyan-500/20',
    title: 'Learning Roadmap Generator',
    desc: 'Turn your skill gaps into a week-by-week study plan. AI generates a personalized roadmap based on your actual interview results.',
  },
]

const STATS = [
  { label: 'Questions Generated', value: '50,000+', icon: Brain },
  { label: 'Interviews Conducted', value: '12,000+', icon: Target },
  { label: 'Active Users', value: '3,500+', icon: Users },
  { label: 'Avg Score Improvement', value: '+35%', icon: TrendingUp },
]

const HOW_IT_WORKS = [
  { step: '01', title: 'Upload Your Resume', desc: 'Our AI reads your experience and generates role-specific questions tailored to your background.' },
  { step: '02', title: 'Practice Interviews', desc: 'Behavioral + coding sessions with real-time AI grading, test-case runners, and instant feedback.' },
  { step: '03', title: 'Analyze Your Gaps', desc: 'Detailed skill reports reveal exactly where you need to improve across every technical topic.' },
  { step: '04', title: 'Get a Roadmap', desc: 'AI creates a week-by-week learning plan so you walk into every interview fully prepared.' },
]

const COMPANIES = ['Google', 'Meta', 'Amazon', 'Microsoft', 'Apple', 'Netflix', 'Stripe', 'Uber']

export const LandingPage = () => {
  const { isAuthenticated } = useAuthStore()

  return (
    <div className="min-h-screen dark:bg-[#0a0a0f] bg-gray-50 text-sm overflow-x-hidden">

      {/* ── Navbar ─────────────────────────────────────────────────── */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b dark:border-white/5 border-black/5 dark:bg-[#0a0a0f]/90 bg-white/90 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 md:px-8 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
              <Zap size={14} className="text-white" />
            </div>
            <span className="font-bold dark:text-white text-neutral-900 text-[15px]">InterviewAI</span>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-xs font-semibold dark:text-neutral-400 text-neutral-500">
            <a href="#features" className="hover:dark:text-white hover:text-neutral-900 transition-colors">Features</a>
            <a href="#how" className="hover:dark:text-white hover:text-neutral-900 transition-colors">How It Works</a>
            <a href="#stats" className="hover:dark:text-white hover:text-neutral-900 transition-colors">Stats</a>
          </nav>
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <Link to="/dashboard"
                className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand-500 text-white text-xs font-bold hover:bg-brand-600 transition-colors">
                Go to App <ArrowRight size={12} />
              </Link>
            ) : (
              <>
                <Link to="/login" className="text-xs font-semibold dark:text-neutral-300 text-neutral-600 hover:dark:text-white hover:text-neutral-900 transition-colors">
                  Log In
                </Link>
                <Link to="/register"
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-brand-500 text-white text-xs font-bold hover:bg-brand-600 transition-colors">
                  Get Started <ArrowRight size={12} />
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* ── Hero ───────────────────────────────────────────────────── */}
      <section className="relative pt-32 pb-24 px-4 md:px-8 overflow-hidden">
        {/* Background glow */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] rounded-full bg-brand-500/10 blur-[120px]" />
          <div className="absolute top-20 left-1/4 w-64 h-64 rounded-full bg-purple-600/8 blur-[80px]" />
        </div>

        <div className="relative max-w-5xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border dark:border-brand-500/30 border-brand-500/30 dark:bg-brand-500/5 bg-brand-500/5 text-brand-500 text-xs font-semibold mb-6">
              <Zap size={11} /> AI-Powered Interview Preparation Platform
            </div>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl sm:text-5xl md:text-6xl font-black dark:text-white text-neutral-900 leading-[1.1] tracking-tight mb-6"
          >
            Land your dream{' '}
            <span className="bg-gradient-to-r from-brand-500 to-purple-500 bg-clip-text text-transparent">
              tech job
            </span>
            <br className="hidden sm:block" /> with AI-driven practice
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}
            className="text-base dark:text-neutral-400 text-neutral-600 max-w-2xl mx-auto leading-relaxed mb-10"
          >
            Practice behavioral and coding interviews with AI that gives you real feedback,
            tracks your progress, and builds a personalized learning roadmap — exactly like FAANG interviewers expect.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-3"
          >
            <Link to={isAuthenticated ? '/dashboard' : '/register'}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-sm transition-all hover:scale-105 hover:shadow-lg hover:shadow-brand-500/25">
              Start Practicing Free <ArrowRight size={16} />
            </Link>
            <a href="#how"
              className="flex items-center gap-2 px-6 py-3 rounded-xl border dark:border-surface-border border-lsurface-border dark:text-neutral-300 text-neutral-600 font-semibold text-sm hover:dark:border-neutral-500 hover:border-neutral-400 transition-all">
              <Play size={14} /> See How It Works
            </a>
          </motion.div>

          {/* Company logos */}
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
            className="mt-14"
          >
            <p className="text-xs dark:text-neutral-500 text-neutral-400 font-semibold uppercase tracking-widest mb-4">
              Prepare for interviews at
            </p>
            <div className="flex flex-wrap justify-center gap-x-8 gap-y-2">
              {COMPANIES.map(c => (
                <span key={c} className="text-sm font-bold dark:text-neutral-600 text-neutral-400">{c}</span>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Stats ──────────────────────────────────────────────────── */}
      <section id="stats" className="py-16 px-4 md:px-8 border-y dark:border-white/5 border-black/5 dark:bg-white/[0.02] bg-white">
        <div className="max-w-5xl mx-auto">
          <motion.div variants={stagger} initial="hidden" whileInView="show" viewport={{ once: true }}
            className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {STATS.map(s => (
              <motion.div key={s.label} variants={fadeUp} className="text-center">
                <s.icon size={20} className="text-brand-500 mx-auto mb-2" />
                <p className="text-3xl font-black dark:text-white text-neutral-900 tabular-nums">{s.value}</p>
                <p className="text-xs dark:text-neutral-400 text-neutral-500 font-semibold mt-1">{s.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── Features ───────────────────────────────────────────────── */}
      <section id="features" className="py-24 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="text-center mb-14">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border dark:border-purple-500/30 border-purple-500/20 dark:bg-purple-500/5 bg-purple-50 text-purple-500 text-xs font-semibold mb-4">
              <Star size={11} /> Everything you need to succeed
            </div>
            <h2 className="text-3xl md:text-4xl font-black dark:text-white text-neutral-900 tracking-tight mb-4">
              A complete interview prep toolkit
            </h2>
            <p className="dark:text-neutral-400 text-neutral-600 max-w-xl mx-auto">
              From resume to offer letter — every tool you need is here, powered by the same AI used by top engineering teams.
            </p>
          </motion.div>

          <motion.div variants={stagger} initial="hidden" whileInView="show" viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURES.map((f) => (
              <motion.div key={f.title} variants={fadeUp}
                className={`group p-6 rounded-2xl border dark:bg-white/[0.02] bg-white hover:dark:bg-white/[0.04] hover:bg-gray-50 transition-all cursor-default dark:border-white/5 ${f.border}`}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${f.color}`}>
                  <f.icon size={18} />
                </div>
                <h3 className="font-bold dark:text-white text-neutral-900 mb-2">{f.title}</h3>
                <p className="text-xs dark:text-neutral-400 text-neutral-600 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── How It Works ───────────────────────────────────────────── */}
      <section id="how" className="py-24 px-4 md:px-8 dark:bg-white/[0.02] bg-white border-y dark:border-white/5 border-black/5">
        <div className="max-w-5xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="text-center mb-14">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border dark:border-emerald-500/30 border-emerald-500/20 dark:bg-emerald-500/5 bg-emerald-50 text-emerald-500 text-xs font-semibold mb-4">
              <CheckCircle size={11} /> Simple & effective
            </div>
            <h2 className="text-3xl md:text-4xl font-black dark:text-white text-neutral-900 tracking-tight mb-4">
              From zero to interview-ready in 4 steps
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {HOW_IT_WORKS.map((step, i) => (
              <motion.div key={step.step}
                initial={{ opacity: 0, x: i % 2 === 0 ? -16 : 16 }} whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }} transition={{ delay: i * 0.1 }}
                className="flex gap-5 p-6 rounded-2xl border dark:border-white/5 border-black/5 dark:bg-white/[0.02] bg-white">
                <span className="text-3xl font-black text-brand-500/20 shrink-0 leading-none font-mono">{step.step}</span>
                <div>
                  <h3 className="font-bold dark:text-white text-neutral-900 mb-1.5">{step.title}</h3>
                  <p className="text-xs dark:text-neutral-400 text-neutral-600 leading-relaxed">{step.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Leaderboard preview / Social proof ─────────────────────── */}
      <section className="py-24 px-4 md:px-8">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="rounded-3xl border dark:border-brand-500/20 border-brand-500/15 dark:bg-brand-500/5 bg-brand-50/50 overflow-hidden">
            <div className="p-8 md:p-12 flex flex-col md:flex-row items-center gap-8">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-4">
                  <Trophy size={20} className="text-amber-400" />
                  <span className="text-xs font-bold dark:text-neutral-300 text-neutral-600 uppercase tracking-widest">Global Leaderboard</span>
                </div>
                <h2 className="text-2xl md:text-3xl font-black dark:text-white text-neutral-900 mb-4 leading-tight">
                  See where you rank among thousands of candidates worldwide
                </h2>
                <p className="dark:text-neutral-400 text-neutral-600 text-xs leading-relaxed mb-6">
                  Our real-time leaderboard ranks candidates across all difficulty levels. Compete, improve, and see your score climb.
                </p>
                <Link to={isAuthenticated ? '/leaderboard' : '/register'}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-500 text-white text-xs font-bold hover:bg-brand-600 transition-all">
                  View Leaderboard <ChevronRight size={14} />
                </Link>
              </div>
              {/* Mock leaderboard preview */}
              <div className="w-full md:w-72 shrink-0">
                <div className="rounded-2xl border dark:border-white/10 border-black/5 dark:bg-[#0a0a0f]/60 bg-white overflow-hidden">
                  {[
                    { rank: 1, name: 'Arjun Mehta', score: 9.8, color: 'from-amber-500 to-orange-500' },
                    { rank: 2, name: 'Priya Sharma', score: 9.5, color: 'from-slate-500 to-slate-400' },
                    { rank: 3, name: 'Wei Chen', score: 9.2, color: 'from-orange-600 to-amber-600' },
                    { rank: 4, name: 'Alex Johnson', score: 8.9, color: 'from-brand-500 to-purple-600' },
                    { rank: 5, name: 'Sam Torres', score: 8.7, color: 'from-brand-500 to-purple-600' },
                  ].map(e => (
                    <div key={e.rank} className={`flex items-center gap-3 px-4 py-2.5 ${e.rank < 5 ? 'border-b dark:border-white/5 border-black/5' : ''}`}>
                      <span className="text-xs font-bold dark:text-neutral-500 text-neutral-400 w-5 text-center">#{e.rank}</span>
                      <div className={`w-7 h-7 rounded-lg bg-gradient-to-br ${e.color} flex items-center justify-center text-xs font-bold text-white shrink-0`}>
                        {e.name.slice(0, 2)}
                      </div>
                      <span className="flex-1 text-xs font-semibold dark:text-neutral-200 text-neutral-700 truncate">{e.name}</span>
                      <span className="text-xs font-bold text-brand-500 tabular-nums">{e.score}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── CTA ────────────────────────────────────────────────────── */}
      <section className="py-24 px-4 md:px-8 relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] rounded-full bg-brand-500/10 blur-[100px]" />
        </div>
        <div className="relative max-w-3xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border dark:border-amber-500/30 border-amber-500/20 dark:bg-amber-500/5 bg-amber-50 text-amber-500 text-xs font-semibold mb-6">
              <Shield size={11} /> Free to get started · No credit card
            </div>
            <h2 className="text-4xl md:text-5xl font-black dark:text-white text-neutral-900 tracking-tight mb-6">
              Ready to ace your<br />
              <span className="bg-gradient-to-r from-brand-500 to-purple-500 bg-clip-text text-transparent">next interview?</span>
            </h2>
            <p className="dark:text-neutral-400 text-neutral-600 text-base mb-10 max-w-xl mx-auto leading-relaxed">
              Join thousands of engineers who used InterviewAI to land offers at top tech companies.
              Start practicing in under 60 seconds.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link to={isAuthenticated ? '/dashboard' : '/register'}
                className="flex items-center gap-2 px-7 py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-sm transition-all hover:scale-105 hover:shadow-xl hover:shadow-brand-500/30">
                Start for Free <ArrowRight size={16} />
              </Link>
              <Link to="/login"
                className="flex items-center gap-2 px-7 py-3.5 rounded-xl border dark:border-white/10 border-black/10 dark:text-neutral-300 text-neutral-600 font-semibold text-sm hover:dark:border-white/20 transition-all">
                Already have an account
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────────────────── */}
      <footer className="border-t dark:border-white/5 border-black/5 py-8 px-4 md:px-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-brand-500 flex items-center justify-center">
              <Zap size={12} className="text-white" />
            </div>
            <span className="font-bold dark:text-white text-neutral-900 text-sm">InterviewAI</span>
          </div>
          <p className="text-xs dark:text-neutral-500 text-neutral-400">
            © {new Date().getFullYear()} InterviewAI Platform. All rights reserved.
          </p>
          <div className="flex items-center gap-4 dark:text-neutral-500 text-neutral-400">
            <a href="#" className="hover:dark:text-white hover:text-neutral-700 transition-colors"><Github size={16} /></a>
            <a href="#" className="hover:dark:text-white hover:text-neutral-700 transition-colors"><Twitter size={16} /></a>
            <Link to="/login" className="text-xs font-semibold hover:dark:text-white hover:text-neutral-700 transition-colors">Sign In</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
