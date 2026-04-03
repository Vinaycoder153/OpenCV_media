import { BrainCircuit, Play, Sparkles } from 'lucide-react';
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
              Rule-based constraints + AI reasoning + transparent actions with measured impact.
            </CardDescription>
          </div>
          <div className="flex gap-2">
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
          </div>
          <p className="text-sm text-muted-foreground">{result.summary}</p>
        </CardContent>
      </Card>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {result.impact.map((metric) => {
          const view = formatImpact(metric.before, metric.after, metric.unit);
          return (
            <Card key={metric.key}>
              <CardHeader>
                <CardDescription>{metric.label}</CardDescription>
                <CardTitle>{view.after}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <p className="text-xs text-muted-foreground">Before: {view.before}</p>
                <Badge variant="success">{view.delta}</Badge>
              </CardContent>
            </Card>
          );
        })}
      </section>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            AI Decision Transparency
          </CardTitle>
          <CardDescription>Every action includes why it was chosen and its observed effect.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {result.decisions.map((decision) => (
            <div key={decision.step} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <p className="text-sm font-semibold">{decision.dayLabel}: {decision.action}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{decision.rationale}</p>
                </div>
                <Badge variant="outline">Confidence {(decision.confidence * 100).toFixed(0)}%</Badge>
              </div>
              <div className="mt-3 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
                <div className="rounded-xl border border-white/10 bg-background/40 p-2">
                  <p className="text-muted-foreground">Expected</p>
                  <p className="mt-1 text-foreground">{decision.expectedImpact}</p>
                </div>
                <div className="rounded-xl border border-success/20 bg-success/10 p-2">
                  <p className="text-muted-foreground">Actual</p>
                  <p className="mt-1 text-foreground">{decision.actualImpact}</p>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
