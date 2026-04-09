import { motion } from 'framer-motion';
import { BrainCircuit, CheckCircle2, Play, Sparkles, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { AutoModeResult } from '@/types';

interface AutonomousModeProps {
  result: AutoModeResult;
  loading: boolean;
  onRun: (days: number) => Promise<void>;
}

function formatImpact(before: number, after: number, unit: string) {
  const delta = after - before;
  const pct = before > 0 ? (delta / before) * 100 : 0;
  const render = (value: number) => {
    if (unit === 'INR') {
      return `₹${Math.round(value).toLocaleString('en-IN')}`;
    }
    if (unit === '%') {
      return `${value.toFixed(1)}%`;
    }
    if (unit === '/5') {
      return `${value.toFixed(2)}/5`;
    }
    return `${Math.round(value)}`;
  };

  return {
    before: render(before),
    after: render(after),
    delta: `${delta >= 0 ? '+' : ''}${pct.toFixed(1)}%`,
    positive: delta >= 0,
  };
}

export function AutonomousMode({ result, loading, onRun }: AutonomousModeProps) {
  return (
    <div className="space-y-5">
      <Card className="surface-gradient">
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <BrainCircuit className="h-5 w-5 text-primary" />
              Autonomous AI Mode
            </CardTitle>
            <CardDescription>
              Rule-based constraints + AI reasoning + transparent actions with measured impact. All 3 OpenEnv tasks run sequentially.
            </CardDescription>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button variant="secondary" onClick={() => void onRun(7)} disabled={loading}>
              7 Days
            </Button>
            <Button onClick={() => void onRun(14)} disabled={loading}>
              <Play className="h-4 w-4" />
              {loading ? 'Running...' : 'Run 14-Day Auto Mode'}
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            <Badge variant="success">{result.mode.toUpperCase()}</Badge>
            <Badge variant="outline">{result.periodLabel}</Badge>
            <Badge variant="warning">Deterministic simulation</Badge>
            <Badge variant="outline" className="gap-1">
              <CheckCircle2 className="h-3 w-3 text-success" />
              3 tasks evaluated
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground">{result.summary}</p>
        </CardContent>
      </Card>

      {/* Impact KPI grid with before/after bars */}
      <section>
        <p className="section-title mb-3">Before vs After — Aggregated Across All 3 Tasks</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {result.impact.map((metric, index) => {
            const view = formatImpact(metric.before, metric.after, metric.unit);
            const barPct = Math.min(100, Math.abs(parseFloat(view.delta)) * 2);
            return (
              <motion.div
                key={metric.key}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.08 }}
              >
                <Card className="h-full">
                  <CardHeader>
                    <CardDescription>{metric.label}</CardDescription>
                    <CardTitle className="text-2xl">{view.after}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                      <motion.div
                        className={`h-full rounded-full ${view.positive ? 'bg-success' : 'bg-danger'}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${barPct}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.5 + index * 0.1 }}
                      />
                    </div>
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-xs text-muted-foreground">was {view.before}</p>
                      <Badge variant={view.positive ? 'success' : 'danger'}>{view.delta}</Badge>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Decision transparency */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            AI Decision Transparency
          </CardTitle>
          <CardDescription>Every action includes why it was chosen and its observed effect.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {result.decisions.map((decision, index) => (
            <motion.div
              key={decision.step}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.06 }}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/15 text-xs font-bold text-primary">{decision.step}</span>
                    <p className="text-sm font-semibold">{decision.dayLabel}: {decision.action}</p>
                  </div>
                  <p className="mt-1.5 text-xs text-muted-foreground">{decision.rationale}</p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="outline">
                    <TrendingUp className="mr-1 h-3 w-3 text-success" />
                    {(decision.confidence * 100).toFixed(0)}% confidence
                  </Badge>
                </div>
              </div>
              <div className="mt-3 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-xl border border-white/10 bg-background/40 p-2">
                  <p className="text-muted-foreground">Expected outcome</p>
                  <p className="mt-1 font-medium text-foreground">{decision.expectedImpact}</p>
                </div>
                <div className="rounded-xl border border-success/25 bg-success/8 p-2">
                  <p className="text-muted-foreground">Actual result</p>
                  <p className="mt-1 font-medium text-foreground">{decision.actualImpact}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
