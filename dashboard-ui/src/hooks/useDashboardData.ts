import { useCallback, useEffect, useMemo, useState } from 'react';
import { fetchDashboardSnapshot, generateContent, askAssistant, analyzeReviewBatch, fetchWeeklyReport, runAutonomousMode } from '@/services/api';
import { mockDashboard } from '@/data/mock';
import type { AssistantMessage, AutoModeResult, ContentResult, DashboardSnapshot, ReviewItem, WeeklyReport } from '@/types';

export interface GenerateContentInput {
  businessType: string;
  audience: string;
  tone: string;
}

export function useDashboardData() {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(mockDashboard);
  const [isInitialLoading, setIsInitialLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [contentLoading, setContentLoading] = useState(false);
  const [reviewsLoading, setReviewsLoading] = useState(false);
  const [assistantLoading, setAssistantLoading] = useState(false);
  const [reportLoading, setReportLoading] = useState(false);
  const [autoModeLoading, setAutoModeLoading] = useState(false);

  const loadSnapshot = useCallback(async (mode: 'initial' | 'refresh' = 'initial') => {
    mode === 'initial' ? setIsInitialLoading(true) : setIsRefreshing(true);
    try {
      const result = await fetchDashboardSnapshot();
      setSnapshot(result);
    } finally {
      mode === 'initial' ? setIsInitialLoading(false) : setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void loadSnapshot('refresh');
  }, [loadSnapshot]);

  const contentResult = snapshot?.contentResult ?? mockDashboard.contentResult;
  const reviews = snapshot?.reviews ?? mockDashboard.reviews;
  const assistantMessages = snapshot?.assistantMessages ?? mockDashboard.assistantMessages;
  const weeklyReport = snapshot?.weeklyReport ?? mockDashboard.weeklyReport;
  const autoMode = snapshot?.autoMode ?? mockDashboard.autoMode;

  const updateSnapshot = useCallback((updater: (current: DashboardSnapshot) => DashboardSnapshot) => {
    setSnapshot((current) => updater(current ?? mockDashboard));
  }, []);

  const generateContentDraft = useCallback(async (input: GenerateContentInput): Promise<ContentResult> => {
    setContentLoading(true);
    try {
      const result = await generateContent(input);
      updateSnapshot((current) => ({ ...current, contentResult: result }));
      return result;
    } finally {
      setContentLoading(false);
    }
  }, [updateSnapshot]);

  const analyzeReviews = useCallback(async (reviewBatch?: ReviewItem[]): Promise<ReviewItem[]> => {
    setReviewsLoading(true);
    try {
      const result = await analyzeReviewBatch(reviewBatch ?? reviews);
      updateSnapshot((current) => ({ ...current, reviews: result }));
      return result;
    } finally {
      setReviewsLoading(false);
    }
  }, [reviews, updateSnapshot]);

  const sendAssistantMessage = useCallback(async (problem: string): Promise<AssistantMessage> => {
    setAssistantLoading(true);
    try {
      const response = await askAssistant(problem);
      updateSnapshot((current) => ({ ...current, assistantMessages: [...current.assistantMessages, { id: `u-${Date.now()}`, role: 'user', content: problem, timestamp: 'Now' }, response] }));
      return response;
    } finally {
      setAssistantLoading(false);
    }
  }, [updateSnapshot]);

  const loadWeeklyInsight = useCallback(async (): Promise<WeeklyReport> => {
    setReportLoading(true);
    try {
      const result = await fetchWeeklyReport();
      updateSnapshot((current) => ({ ...current, weeklyReport: result }));
      return result;
    } finally {
      setReportLoading(false);
    }
  }, [updateSnapshot]);

  const runAutoMode = useCallback(async (days = 14): Promise<AutoModeResult> => {
    setAutoModeLoading(true);
    try {
      const result = await runAutonomousMode({ days });
      updateSnapshot((current) => ({ ...current, autoMode: result }));
      return result;
    } finally {
      setAutoModeLoading(false);
    }
  }, [updateSnapshot]);

  const refresh = useCallback(async () => {
    await loadSnapshot('refresh');
  }, [loadSnapshot]);

  return useMemo(() => ({
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
  }), [assistantLoading, assistantMessages, autoMode, autoModeLoading, contentLoading, contentResult, generateContentDraft, isInitialLoading, isRefreshing, loadWeeklyInsight, refresh, reportLoading, reviews, reviewsLoading, runAutoMode, sendAssistantMessage, snapshot, weeklyReport, analyzeReviews]);
}
