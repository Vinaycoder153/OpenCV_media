import { Component, useState, type ReactNode } from 'react';
import { motion } from 'framer-motion';
import { AppShell } from '@/components/layout/AppShell';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog';
import { ToastViewport } from '@/components/ui/toast';
import { ToastProvider, useToast } from '@/hooks/useToast';
import { useDashboardData } from '@/hooks/useDashboardData';
import { useThemeMode } from '@/hooks/useThemeMode';
import { AIAssistantPanel } from '@/pages/AIAssistantPanel';
import { DashboardOverview } from '@/pages/DashboardOverview';
import { ReportsInsights } from '@/pages/ReportsInsights';
import { ReviewAnalyzer } from '@/pages/ReviewAnalyzer';
import { SocialContentGenerator } from '@/pages/SocialContentGenerator';
import { AutonomousMode } from '@/pages/AutonomousMode';
import type { NavKey } from '@/types';

interface AppErrorBoundaryState {
  hasError: boolean;
}

class AppErrorBoundary extends Component<{ children: ReactNode }, AppErrorBoundaryState> {
  state: AppErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-background px-4 py-10 text-foreground sm:px-6 lg:px-8">
          <div className="mx-auto flex min-h-[60vh] w-full max-w-3xl flex-col justify-center gap-4 rounded-[1.75rem] border border-white/10 bg-white/5 p-8 shadow-glow backdrop-blur-xl">
            <p className="section-title">App recovery</p>
            <h1 className="headline">The dashboard hit a render error.</h1>
            <p className="max-w-2xl text-sm text-muted-foreground">
              One of the panels failed while rendering. Reloading usually restores the full dashboard.
            </p>
            <Button className="w-fit" onClick={() => window.location.reload()}>
              Reload dashboard
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

function AppContent() {
  const { theme, toggleTheme } = useThemeMode();
  const {
    snapshot,
    isInitialLoading,
    isRefreshing,
    contentResult,
    reviews,
    assistantMessages,
    weeklyReport,
    autoMode,
    contentLoading,
    reviewsLoading,
    assistantLoading,
    reportLoading,
    autoModeLoading,
    refresh,
    generateContentDraft,
    analyzeReviews,
    sendAssistantMessage,
    loadWeeklyInsight,
    runAutoMode,
  } = useDashboardData();
  const { pushToast } = useToast();

  const [activePage, setActivePage] = useState<NavKey>('overview');
  const [replyPreview, setReplyPreview] = useState('');

  let page: ReactNode = null;

  switch (activePage) {
    case 'overview':
      page = (
        <DashboardOverview
          snapshot={snapshot}
          loading={isInitialLoading}
          refreshing={isRefreshing}
          onRefresh={async () => {
            await refresh();
            pushToast({ title: 'Dashboard refreshed', description: 'Latest metrics synced successfully.', tone: 'success' });
          }}
        />
      );
      break;
    case 'assistant':
      page = (
        <AIAssistantPanel
          messages={assistantMessages}
          loading={assistantLoading}
          onSend={async (problem) => {
            await sendAssistantMessage(problem);
            pushToast({ title: 'AI response generated', description: 'Your strategy suggestion is ready.', tone: 'success' });
          }}
        />
      );
      break;
    case 'content':
      page = (
        <SocialContentGenerator
          contentResult={contentResult}
          loading={contentLoading}
          onGenerate={async (input) => {
            await generateContentDraft(input);
            pushToast({ title: 'Content generated', description: 'Fresh post assets are ready to publish.', tone: 'success' });
          }}
          onCopy={async (value, label) => {
            try {
              await navigator.clipboard.writeText(value);
              pushToast({ title: `${label} copied`, description: 'Text copied to clipboard.', tone: 'success' });
            } catch {
              pushToast({ title: 'Copy failed', description: 'Please copy manually from the card.', tone: 'error' });
            }
          }}
        />
      );
      break;
    case 'reviews':
      page = (
        <ReviewAnalyzer
          reviews={reviews}
          loading={reviewsLoading}
          onAnalyze={async () => {
            await analyzeReviews();
            pushToast({ title: 'Reviews analyzed', description: 'Sentiment and reply drafts updated.', tone: 'success' });
          }}
          onReplyPreview={(reply) => {
            setReplyPreview(reply);
          }}
        />
      );
      break;
    case 'reports':
      page = (
        <ReportsInsights
          report={weeklyReport}
          loading={reportLoading}
          onRefresh={async () => {
            await loadWeeklyInsight();
            pushToast({ title: 'Weekly report refreshed', description: 'Insights have been updated.', tone: 'success' });
          }}
        />
      );
      break;
    case 'auto':
      page = (
        <AutonomousMode
          result={autoMode}
          loading={autoModeLoading}
          onRun={async (days) => {
            await runAutoMode(days);
            pushToast({ title: 'Autonomous mode completed', description: `${days}-day simulation executed with transparent decision logs.`, tone: 'success' });
          }}
        />
      );
      break;
    default:
      page = null;
  }

  return (
    <>
      <AppShell activePage={activePage} onPageChange={setActivePage} theme={theme} onToggleTheme={toggleTheme}>
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }}>
          {page}
        </motion.div>
      </AppShell>

      {replyPreview && (
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="subtle" className="fixed bottom-24 right-4 z-40 rounded-full px-4 py-2 lg:bottom-6 lg:right-6">
              Reply Preview
            </Button>
          </DialogTrigger>
          <DialogContent>
            <h3 className="text-xl font-semibold">AI Reply Preview</h3>
            <p className="mt-3 rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-muted-foreground">
              {replyPreview}
            </p>
          </DialogContent>
        </Dialog>
      )}

      <ToastViewport />
    </>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AppErrorBoundary>
        <AppContent />
      </AppErrorBoundary>
    </ToastProvider>
  );
}
