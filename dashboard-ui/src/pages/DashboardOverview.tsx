import { motion } from 'framer-motion';
import { BarChart3, Calendar, ChevronRight, Sparkles, TrendingDown, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { RevenueTrendChart } from '@/components/charts/RevenueTrendChart';
import { ComparisonBarChart } from '@/components/charts/ComparisonBarChart';
import type { DashboardSnapshot, FestivalEvent, NavKey } from '@/types';

interface DashboardOverviewProps {
  snapshot: DashboardSnapshot | null;
  loading: boolean;
  refreshing: boolean;
  festivals: FestivalEvent[];
  onRefresh: () => void;
  onNavigate: (page: NavKey) => void;
}

function KpiSkeletonCard() {
  return (
    <Card className="surface-gradient">
      <CardHeader className="space-y-3">
        <Skeleton className="h-4 w-28" />
        <Skeleton className="h-9 w-32" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-4 w-24" />
      </CardContent>
    </Card>
  );
}

function FestivalBanner({ festivals }: { festivals: FestivalEvent[] }) {
  const next = festivals[0];
  if (!next) return null;
  const urgent = next.days_until <= 7;
  const soon = next.days_until <= 14;
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`flex items-start gap-3 rounded-[1.25rem] border px-4 py-3 ${
        urgent
          ? 'border-warning/40 bg-warning/10'
          : soon
          ? 'border-primary/30 bg-primary/8'
          : 'border-white/10 bg-white/5'
      }`}
    >
      <Calendar className={`mt-0.5 h-4 w-4 shrink-0 ${urgent ? 'text-warning' : 'text-primary'}`} />
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-semibold">{next.name}</span>
          <Badge variant={urgent ? 'warning' : 'outline'} className="text-xs">
            {next.days_until === 0 ? 'Today!' : next.days_until === 1 ? 'Tomorrow' : `${next.days_until} days away`}
          </Badge>
        </div>
        <p className="mt-0.5 text-xs text-muted-foreground">{next.boost}</p>
      </div>
      {festivals.length > 1 && (
        <span className="shrink-0 text-xs text-muted-foreground">+{festivals.length - 1} more</span>
      )}
    </motion.div>
  );
}

export function DashboardOverview({ snapshot, loading, refreshing, festivals, onRefresh, onNavigate }: DashboardOverviewProps) {
  if (loading || !snapshot) {
    return (
      <div className="space-y-5 sm:space-y-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, idx) => (
            <KpiSkeletonCard key={idx} />
          ))}
        </div>
        <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1.6fr_1fr]">
          <Skeleton className="h-[360px] w-full rounded-[1.5rem]" />
          <Skeleton className="h-[360px] w-full rounded-[1.5rem]" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5 sm:space-y-6">
      {/* Festival banner */}
      {festivals.length > 0 && <FestivalBanner festivals={festivals} />}

      {/* KPI cards */}
      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {snapshot.kpis.map((kpi, index) => {
          const positive = kpi.trend === 'up';
          const warning = kpi.trend === 'down';
          return (
            <motion.div
              key={kpi.label}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.32, delay: index * 0.06 }}
            >
              <Card className="surface-gradient transition-transform duration-200 hover:-translate-y-1">
                <CardHeader>
                  <CardDescription>{kpi.label}</CardDescription>
                  <CardTitle className="text-3xl">{kpi.value}</CardTitle>
                </CardHeader>
                <CardContent className="flex items-center justify-between">
                  <Badge variant={positive ? 'success' : warning ? 'danger' : 'outline'}>
                    {positive ? <TrendingUp className="mr-1 h-3.5 w-3.5" /> : warning ? <TrendingDown className="mr-1 h-3.5 w-3.5" /> : <BarChart3 className="mr-1 h-3.5 w-3.5" />}
                    {kpi.change}
                  </Badge>
                  <span className="text-xs text-muted-foreground">{kpi.hint}</span>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </section>

      {/* Before vs After + Decision Transparency */}
      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[1.4fr_1fr]">
        <Card className="surface-gradient">
          <CardHeader>
            <CardTitle>Before vs After AI Impact</CardTitle>
            <CardDescription>{snapshot.autoMode.periodLabel} measured KPI movement</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {snapshot.autoMode.impact.map((item) => {
              const delta = item.after - item.before;
              const pct = item.before > 0 ? (delta / item.before) * 100 : 0;
              const barPct = Math.min(100, Math.abs(pct) * 2);
              return (
                <div key={item.key} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-semibold">{item.label}</p>
                    <Badge variant={delta >= 0 ? 'success' : 'danger'}>{`${delta >= 0 ? '+' : ''}${pct.toFixed(1)}%`}</Badge>
                  </div>
                  <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                    <motion.div
                      className={`h-full rounded-full ${delta >= 0 ? 'bg-success' : 'bg-danger'}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${barPct}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
                    />
                  </div>
                  <p className="mt-2 text-xs text-muted-foreground">
                    Before: {item.unit === 'INR' ? `₹${Math.round(item.before).toLocaleString('en-IN')}` : `${item.before}${item.unit === '%' ? '%' : ''}`}
                    {'  '}→{'  '}
                    After: {item.unit === 'INR' ? `₹${Math.round(item.after).toLocaleString('en-IN')}` : `${item.after}${item.unit === '%' ? '%' : ''}`}
                  </p>
                </div>
              );
            })}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Decision Transparency</CardTitle>
            <CardDescription>Why AI acted and what happened next</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {snapshot.autoMode.decisions.slice(0, 2).map((decision) => (
              <div key={decision.step} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                <p className="text-sm font-semibold">{decision.dayLabel}: {decision.action}</p>
                <p className="mt-1 text-xs text-muted-foreground">{decision.rationale}</p>
                <p className="mt-2 text-xs text-primary">Observed: {decision.actualImpact}</p>
              </div>
            ))}
            <Button variant="secondary" className="w-full" onClick={() => onNavigate('auto')}>
              View full autonomous log
              <ChevronRight className="h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </section>

      {/* Charts */}
      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[1.6fr_1fr]">
        <Card>
          <CardHeader className="flex flex-row items-start justify-between gap-4">
            <div>
              <CardTitle>Revenue Growth Trend</CardTitle>
              <CardDescription>AI-guided weekly growth trajectory</CardDescription>
            </div>
            <Button variant="secondary" onClick={onRefresh} disabled={refreshing}>
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </Button>
          </CardHeader>
          <CardContent>
            <RevenueTrendChart data={snapshot.trend} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Action Comparison</CardTitle>
            <CardDescription>Cross-channel delivery performance</CardDescription>
          </CardHeader>
          <CardContent>
            <ComparisonBarChart data={snapshot.comparison} />
          </CardContent>
        </Card>
      </section>

      {/* Today's Plan + Quick Actions */}
      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[1.2fr_1fr]">
        <Card className="surface-gradient">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Today&apos;s AI Plan
            </CardTitle>
            <CardDescription>Focused actions prioritized by projected lift</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {snapshot.plan.map((item) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="rounded-2xl border border-white/10 bg-white/5 p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-semibold">{item.title}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{item.owner} · {item.duration}</p>
                  </div>
                  <Badge variant={item.status === 'running' ? 'warning' : item.status === 'ready' ? 'success' : 'outline'}>
                    {item.status === 'running' && <span className="mr-1.5 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-warning" />}
                    {item.status}
                  </Badge>
                </div>
                <p className="mt-2 text-sm text-primary">Projected impact: {item.impact}</p>
              </motion.div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>High-frequency workflows for operators</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {snapshot.quickActions.map((action, idx) => {
              const targets: NavKey[] = ['content', 'reviews', 'reports'];
              return (
                <button
                  key={action.title}
                  onClick={() => onNavigate(targets[idx] ?? 'content')}
                  className="w-full rounded-2xl border border-white/10 bg-white/5 p-4 text-left transition hover:border-primary/40 hover:bg-primary/10"
                >
                  <div className="flex items-center justify-between gap-2">
                    <p className="font-semibold">{action.title}</p>
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <p className="mt-1 text-sm text-muted-foreground">{action.description}</p>
                </button>
              );
            })}
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
