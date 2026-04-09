import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, BrainCircuit, CheckCircle2, ChevronRight, FlaskConical, Play, RefreshCw, TrendingUp, Trophy, Zap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { SimulationResult, SimulationStep } from '@/types';

interface EnvSimulatorProps {
  loading: boolean;
  result: SimulationResult | null;
  onRun: (taskId: number, days: number) => Promise<void>;
}

const TASK_CONFIG = {
  1: {
    label: 'Task 1 — Social Media Growth',
    color: 'from-blue-600/20 to-cyan-500/10',
    accent: '#5D8CFF',
    badge: 'Easy · 10 steps',
    metricKeys: ['followers', 'engagement_rate'],
    metricLabels: { followers: 'Followers', engagement_rate: 'Engagement Rate' },
    metricFormat: { followers: (v: number) => Math.round(v).toLocaleString('en-IN'), engagement_rate: (v: number) => `${(v * 100).toFixed(1)}%` },
  },
  2: {
    label: 'Task 2 — Review Management',
    color: 'from-green-600/20 to-emerald-500/10',
    accent: '#4ADE80',
    badge: 'Medium · 12 steps',
    metricKeys: ['avg_rating', 'positive_reviews'],
    metricLabels: { avg_rating: 'Avg Rating', positive_reviews: 'Positive Reviews' },
    metricFormat: { avg_rating: (v: number) => `${v.toFixed(2)}/5`, positive_reviews: (v: number) => Math.round(v).toString() },
  },
  3: {
    label: 'Task 3 — Revenue Optimization',
    color: 'from-violet-600/20 to-purple-500/10',
    accent: '#A78BFA',
    badge: 'Hard · 15 steps',
    metricKeys: ['monthly_revenue', 'daily_orders'],
    metricLabels: { monthly_revenue: 'Monthly Revenue', daily_orders: 'Daily Orders' },
    metricFormat: { monthly_revenue: (v: number) => `₹${Math.round(v).toLocaleString('en-IN')}`, daily_orders: (v: number) => Math.round(v).toString() },
  },
} as const;

type TaskId = 1 | 2 | 3;

function ActionTag({ action }: { action: string }) {
  const colorMap: Record<string, string> = {
    generate_post: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
    add_hashtags: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    schedule_post: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
    run_ad: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    reply_review: 'bg-green-500/15 text-green-300 border-green-500/30',
    request_review: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    offer_discount: 'bg-yellow-500/15 text-yellow-300 border-yellow-500/30',
    improve_service: 'bg-teal-500/15 text-teal-300 border-teal-500/30',
    change_price: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
    add_offer: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    run_campaign: 'bg-violet-500/15 text-violet-300 border-violet-500/30',
    launch_bundle: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    no_op: 'bg-gray-500/15 text-gray-400 border-gray-500/30',
  };
  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-mono font-semibold ${colorMap[action] ?? 'bg-primary/15 text-primary border-primary/30'}`}>
      {action.replace(/_/g, ' ')}
    </span>
  );
}

function RewardBar({ reward }: { reward: number }) {
  const pct = Math.max(0, Math.min(100, (reward / 0.5) * 100));
  const color = reward >= 0.25 ? 'bg-success' : reward >= 0.1 ? 'bg-warning' : 'bg-danger';
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 flex-1 rounded-full bg-white/10">
        <motion.div
          className={`h-full rounded-full ${color}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
      <span className="w-10 text-right text-xs font-mono text-muted-foreground">{reward >= 0 ? `+${reward.toFixed(2)}` : reward.toFixed(2)}</span>
    </div>
  );
}

function MetricDelta({ label, before, after, format }: { label: string; before: number; after: number; format: (v: number) => string }) {
  const delta = after - before;
  const pct = before > 0 ? (delta / before) * 100 : 0;
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center">
      <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-xl font-bold">{format(after)}</p>
      <p className="mt-1 text-xs text-muted-foreground">was {format(before)}</p>
      <Badge variant={delta >= 0 ? 'success' : 'danger'} className="mt-2">
        {delta >= 0 ? '+' : ''}{pct.toFixed(1)}%
      </Badge>
    </div>
  );
}

function StepCard({ step, index, isVisible }: { step: SimulationStep; index: number; isVisible: boolean }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          key={step.step}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4, delay: index * 0.08 }}
          className="relative flex gap-4"
        >
          <div className="flex flex-col items-center">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-primary/15 text-sm font-bold text-primary">
              {step.step}
            </div>
            <div className="mt-1 w-px flex-1 bg-white/10" />
          </div>
          <div className="mb-4 flex-1 rounded-[1.25rem] border border-white/10 bg-white/5 p-4">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <ActionTag action={step.action} />
              <span className="text-xs text-muted-foreground">Day {step.day}</span>
            </div>
            <p className="mt-3 text-sm font-semibold text-foreground">{step.rationale}</p>
            <div className="mt-3 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
              <div className="rounded-xl border border-white/10 bg-background/40 p-2">
                <p className="text-muted-foreground">Expected outcome</p>
                <p className="mt-1 font-medium text-foreground">{step.expected}</p>
              </div>
              <div className="rounded-xl border border-white/10 bg-background/40 p-2">
                <p className="mb-1.5 text-muted-foreground">Reward signal</p>
                <RewardBar reward={step.reward} />
              </div>
            </div>
            {Object.keys(step.metrics).length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {Object.entries(step.metrics).map(([k, v]) => (
                  <span key={k} className="rounded-full border border-white/10 bg-white/5 px-2 py-0.5 text-xs font-mono text-muted-foreground">
                    {k}: {typeof v === 'number' && v > 1000 ? `₹${Math.round(v).toLocaleString('en-IN')}` : typeof v === 'number' && v < 1 ? `${(v * 100).toFixed(1)}%` : String(Math.round(v as number))}
                  </span>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export function EnvSimulator({ loading, result, onRun }: EnvSimulatorProps) {
  const [selectedTask, setSelectedTask] = useState<TaskId>(1);
  const [visibleSteps, setVisibleSteps] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const taskConfig = TASK_CONFIG[selectedTask];

  useEffect(() => {
    if (result && result.task_id === selectedTask) {
      setVisibleSteps(0);
      setIsPlaying(true);
    }
  }, [result, selectedTask]);

  useEffect(() => {
    if (!isPlaying || !result || result.steps.length === 0) return;
    if (visibleSteps >= result.steps.length) {
      setIsPlaying(false);
      return;
    }
    timerRef.current = setTimeout(() => {
      setVisibleSteps((n) => n + 1);
    }, 600);
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [isPlaying, visibleSteps, result]);

  const handleRun = async () => {
    setVisibleSteps(0);
    setIsPlaying(false);
    await onRun(selectedTask, 8);
  };

  const oarLabels = ['Observation', 'Action', 'Reward'];

  return (
    <div className="space-y-5">
      {/* Header */}
      <Card className="surface-gradient">
        <CardHeader className="flex flex-row flex-wrap items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FlaskConical className="h-5 w-5 text-primary" />
              OpenEnv Live Simulator
            </CardTitle>
            <CardDescription>
              Observe the Observation → Action → Reward loop executing in real time on a real business environment.
            </CardDescription>
          </div>
          <Button onClick={handleRun} disabled={loading} className="shrink-0">
            {loading ? (
              <><RefreshCw className="h-4 w-4 animate-spin" /> Running simulation…</>
            ) : (
              <><Play className="h-4 w-4" /> Run Simulation</>
            )}
          </Button>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {oarLabels.map((label) => (
              <Badge key={label} variant="outline" className="gap-1.5 text-xs">
                <Activity className="h-3 w-3 text-primary" />
                {label}
              </Badge>
            ))}
            <Badge variant="warning" className="text-xs">Deterministic seed=42</Badge>
            <Badge variant="success" className="text-xs">Rule + AI policy</Badge>
          </div>
        </CardContent>
      </Card>

      {/* Task selector */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        {([1, 2, 3] as TaskId[]).map((id) => {
          const cfg = TASK_CONFIG[id];
          const active = selectedTask === id;
          return (
            <button
              key={id}
              onClick={() => setSelectedTask(id)}
              className={`rounded-[1.25rem] border p-4 text-left transition-all duration-200 ${
                active
                  ? 'border-primary/50 bg-primary/10 shadow-glow'
                  : 'border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10'
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <BrainCircuit className={`h-4 w-4 ${active ? 'text-primary' : 'text-muted-foreground'}`} />
                <Badge variant={active ? 'success' : 'outline'} className="text-xs">{cfg.badge}</Badge>
              </div>
              <p className={`mt-2 text-sm font-semibold ${active ? 'text-foreground' : 'text-muted-foreground'}`}>{cfg.label}</p>
            </button>
          );
        })}
      </div>

      {/* Valid actions reference */}
      {result && result.task_id === selectedTask && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base">
              <Zap className="h-4 w-4 text-primary" />
              Valid Actions for Task {selectedTask}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {result.valid_actions.map((action) => (
                <ActionTag key={action} action={action} />
              ))}
            </div>
            <p className="mt-3 text-xs text-muted-foreground">{result.task_description}</p>
          </CardContent>
        </Card>
      )}

      {/* Steps timeline */}
      {result && result.task_id === selectedTask && result.steps.length > 0 ? (
        <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1.4fr_1fr]">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-primary" />
                OAR Step Timeline
              </CardTitle>
              <CardDescription>
                {isPlaying
                  ? `Executing step ${visibleSteps} of ${result.steps.length}…`
                  : `${result.steps.length} steps completed — score: ${(result.score * 100).toFixed(0)}%`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isPlaying && (
                <div className="mb-4 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-r from-primary to-accent"
                    animate={{ width: `${(visibleSteps / result.steps.length) * 100}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              )}
              <div className="max-h-[540px] overflow-y-auto pr-1">
                {result.steps.map((step, i) => (
                  <StepCard key={step.step} step={step} index={i} isVisible={i < visibleSteps || !isPlaying} />
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Impact & score panel */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Trophy className="h-4 w-4 text-warning" />
                  Episode Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col items-center py-4">
                  <div className="relative h-32 w-32">
                    <svg width="128" height="128" className="-rotate-90">
                      <circle cx="64" cy="64" r="52" stroke="rgba(148,163,184,0.15)" strokeWidth="12" fill="none" />
                      <circle
                        cx="64" cy="64" r="52"
                        stroke="url(#simGradient)"
                        strokeWidth="12"
                        fill="none"
                        strokeDasharray={2 * Math.PI * 52}
                        strokeDashoffset={!isPlaying ? (1 - result.score) * 2 * Math.PI * 52 : 2 * Math.PI * 52}
                        strokeLinecap="round"
                        style={{ transition: 'stroke-dashoffset 1.2s ease-out' }}
                      />
                      <defs>
                        <linearGradient id="simGradient" x1="0" y1="0" x2="1" y2="1">
                          <stop offset="0%" stopColor="#5D8CFF" />
                          <stop offset="100%" stopColor="#66E3FF" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <div className="text-3xl font-extrabold">{!isPlaying ? `${(result.score * 100).toFixed(0)}` : '–'}%</div>
                      <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">graded</div>
                    </div>
                  </div>
                  <p className="mt-3 text-center text-sm text-muted-foreground">
                    Deterministic grader: followers (40%) + engagement (40%) + efficiency (20%)
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-success" />
                  Before vs After
                </CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {taskConfig.metricKeys.map((k) => {
                  const fmt = (taskConfig.metricFormat as Record<string, (v: number) => string>)[k] ?? String;
                  const label = (taskConfig.metricLabels as Record<string, string>)[k] ?? k;
                  const b = result.before[k] ?? 0;
                  const a = result.after[k] ?? 0;
                  return <MetricDelta key={k} label={label} before={b} after={a} format={fmt} />;
                })}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Reward Signal Legend</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-xs">
                {[
                  { color: 'bg-success', label: '≥ 0.25', desc: 'Strong goal progress' },
                  { color: 'bg-warning', label: '0.10 – 0.25', desc: 'Moderate improvement' },
                  { color: 'bg-danger', label: '< 0.10', desc: 'Minimal / negative effect' },
                ].map((item) => (
                  <div key={item.label} className="flex items-center gap-3">
                    <div className={`h-2.5 w-2.5 rounded-full ${item.color}`} />
                    <span className="font-mono text-muted-foreground">{item.label}</span>
                    <ChevronRight className="h-3 w-3 text-muted-foreground" />
                    <span>{item.desc}</span>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16 text-center">
            {loading ? (
              <>
                <RefreshCw className="mb-4 h-10 w-10 animate-spin text-primary" />
                <p className="text-sm text-muted-foreground">Running OpenEnv simulation with deterministic rule+AI policy…</p>
              </>
            ) : (
              <>
                <FlaskConical className="mb-4 h-10 w-10 text-muted-foreground" />
                <p className="text-lg font-semibold">Select a task and click Run Simulation</p>
                <p className="mt-2 max-w-sm text-sm text-muted-foreground">
                  Watch the agent take step-by-step actions with full Observation → Action → Reward transparency.
                </p>
                <Button className="mt-6" onClick={handleRun}>
                  <Play className="h-4 w-4" />
                  Start Simulation
                </Button>
              </>
            )}
          </CardContent>
        </Card>
      )}

      {/* OAR model explainer */}
      <Card className="border-primary/20 bg-primary/5">
        <CardHeader>
          <CardTitle className="text-base">How OpenEnv Works</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 gap-4 text-sm sm:grid-cols-3">
          {[
            { icon: Activity, label: 'Observation', color: 'text-primary', desc: 'The agent reads the current business state — followers, rating, revenue, and market context including Indian festivals and seasonality.' },
            { icon: Zap, label: 'Action', color: 'text-warning', desc: 'A rule-based + AI policy selects the optimal action with transparent reasoning. Invalid or repeated actions incur a penalty reward.' },
            { icon: CheckCircle2, label: 'Reward', color: 'text-success', desc: 'Each step returns a shaped reward signal with components: progress, spam penalty, goal bonus, and efficiency shaping. A deterministic grader scores the episode.' },
          ].map(({ icon: Icon, label, color, desc }) => (
            <div key={label} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-center gap-2">
                <Icon className={`h-4 w-4 ${color}`} />
                <p className="font-semibold">{label}</p>
              </div>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{desc}</p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
