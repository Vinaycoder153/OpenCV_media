import { FileText, RefreshCcw } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CircularProgress } from '@/components/charts/CircularProgress';
import type { WeeklyReport } from '@/types';

interface ReportsInsightsProps {
  report: WeeklyReport;
  loading: boolean;
  onRefresh: () => Promise<void>;
}

export function ReportsInsights({ report, loading, onRefresh }: ReportsInsightsProps) {
  return (
    <div className="space-y-5">
      <Card className="surface-gradient">
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              Reports & Insights
            </CardTitle>
            <CardDescription>Weekly operating summary generated from performance and AI actions.</CardDescription>
          </div>
          <Button onClick={onRefresh} disabled={loading}>
            <RefreshCcw className="h-4 w-4" />
            {loading ? 'Refreshing...' : 'Refresh Report'}
          </Button>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-[1.6fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Weekly Report Card</CardTitle>
            <CardDescription>{report.headline}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm leading-relaxed text-muted-foreground">{report.summary}</p>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-success/30 bg-success/10 p-3">
                <p className="text-xs uppercase tracking-[0.2em] text-success">Positive</p>
                <p className="mt-2 text-lg font-semibold">Growth velocity is healthy</p>
              </div>
              <div className="rounded-2xl border border-warning/30 bg-warning/10 p-3">
                <p className="text-xs uppercase tracking-[0.2em] text-warning">Warning</p>
                <p className="mt-2 text-lg font-semibold">Keep service consistency high</p>
              </div>
              <div className="rounded-2xl border border-danger/30 bg-danger/10 p-3">
                <p className="text-xs uppercase tracking-[0.2em] text-danger">Risk</p>
                <p className="mt-2 text-lg font-semibold">Delayed review replies reduce trust</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <CircularProgress value={report.score} label="Weekly Growth Score" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Growth Suggestions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {report.suggestions.map((suggestion, idx) => (
            <div key={suggestion} className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/5 p-3">
              <Badge variant="outline">{idx + 1}</Badge>
              <p className="text-sm text-muted-foreground">{suggestion}</p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
