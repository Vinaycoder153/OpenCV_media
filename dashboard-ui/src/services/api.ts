import axios from 'axios';
import { mockDashboard, mockSimulation, mockFestivals } from '@/data/mock';
import type { AssistantMessage, AutoModeResult, ContentResult, DashboardSnapshot, FestivalEvent, ImpactMetric, ReviewItem, SimulationResult, WeeklyReport } from '@/types';

const baseURL = import.meta.env.VITE_API_BASE_URL ?? '/api';

export const api = axios.create({
  baseURL,
  timeout: 12000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function normalizeDashboardSnapshot(value: unknown): DashboardSnapshot {
  if (!isRecord(value)) {
    return mockDashboard;
  }

  return {
    ...mockDashboard,
    ...value,
    kpis: Array.isArray(value.kpis) ? value.kpis : mockDashboard.kpis,
    trend: Array.isArray(value.trend) ? value.trend : mockDashboard.trend,
    comparison: Array.isArray(value.comparison) ? value.comparison : mockDashboard.comparison,
    plan: Array.isArray(value.plan) ? value.plan : mockDashboard.plan,
    quickActions: Array.isArray(value.quickActions) ? value.quickActions : mockDashboard.quickActions,
    assistantMessages: Array.isArray(value.assistantMessages) ? value.assistantMessages : mockDashboard.assistantMessages,
    contentResult: isRecord(value.contentResult) ? { ...mockDashboard.contentResult, ...value.contentResult } : mockDashboard.contentResult,
    reviews: Array.isArray(value.reviews) ? value.reviews : mockDashboard.reviews,
    weeklyReport: isRecord(value.weeklyReport) ? { ...mockDashboard.weeklyReport, ...value.weeklyReport } : mockDashboard.weeklyReport,
    autoMode: isRecord(value.autoMode) ? normalizeAutoModeResult(value.autoMode) : mockDashboard.autoMode,
  };
}

function normalizeImpactMetric(value: unknown, fallback: ImpactMetric): ImpactMetric {
  if (!isRecord(value)) {
    return fallback;
  }

  return {
    key: value.key === 'engagement' || value.key === 'rating' || value.key === 'orders' ? value.key : 'revenue',
    label: typeof value.label === 'string' ? value.label : fallback.label,
    before: typeof value.before === 'number' ? value.before : fallback.before,
    after: typeof value.after === 'number' ? value.after : fallback.after,
    unit: typeof value.unit === 'string' ? value.unit : fallback.unit,
  };
}

function normalizeAutoModeResult(value: unknown): AutoModeResult {
  if (!isRecord(value)) {
    return mockDashboard.autoMode;
  }

  const impact = Array.isArray(value.impact)
    ? value.impact.map((item, index) => normalizeImpactMetric(item, mockDashboard.autoMode.impact[index] ?? mockDashboard.autoMode.impact[0]))
    : mockDashboard.autoMode.impact;

  const decisions = Array.isArray(value.decisions)
    ? value.decisions
      .filter(isRecord)
      .map((item, index) => ({
        step: typeof item.step === 'number' ? item.step : index + 1,
        dayLabel: typeof item.dayLabel === 'string' ? item.dayLabel : `Day ${index + 1}`,
        action: typeof item.action === 'string' ? item.action : 'No action',
        rationale: typeof item.rationale === 'string' ? item.rationale : 'No rationale available.',
        expectedImpact: typeof item.expectedImpact === 'string' ? item.expectedImpact : 'Not estimated',
        actualImpact: typeof item.actualImpact === 'string' ? item.actualImpact : 'Not recorded',
        confidence: typeof item.confidence === 'number' ? Math.min(1, Math.max(0, item.confidence)) : 0.5,
      }))
    : mockDashboard.autoMode.decisions;

  return {
    mode: 'rule+ai',
    periodLabel: typeof value.periodLabel === 'string' ? value.periodLabel : mockDashboard.autoMode.periodLabel,
    summary: typeof value.summary === 'string' ? value.summary : mockDashboard.autoMode.summary,
    impact,
    decisions,
  };
}

function normalizeContentResult(value: unknown): ContentResult {
  if (!isRecord(value)) {
    return mockDashboard.contentResult;
  }

  const hashtags = Array.isArray(value.hashtags) ? value.hashtags.filter((item): item is string => typeof item === 'string') : mockDashboard.contentResult.hashtags;

  return {
    ...mockDashboard.contentResult,
    ...value,
    hashtags,
  };
}

function normalizeAssistantMessage(value: unknown): AssistantMessage {
  if (!isRecord(value)) {
    return createAssistantResponse('');
  }

  return {
    id: typeof value.id === 'string' ? value.id : `a-${Date.now()}`,
    role: value.role === 'user' ? 'user' : 'assistant',
    content: typeof value.content === 'string' ? value.content : '',
    bullets: Array.isArray(value.bullets) ? value.bullets.filter((item): item is string => typeof item === 'string') : undefined,
    timestamp: typeof value.timestamp === 'string' ? value.timestamp : 'Just now',
  };
}

function normalizeReview(value: unknown, fallback: ReviewItem): ReviewItem {
  if (!isRecord(value)) {
    return fallback;
  }

  return {
    id: typeof value.id === 'string' ? value.id : fallback.id,
    author: typeof value.author === 'string' ? value.author : fallback.author,
    location: typeof value.location === 'string' ? value.location : fallback.location,
    rating: typeof value.rating === 'number' ? value.rating : fallback.rating,
    sentiment: value.sentiment === 'positive' || value.sentiment === 'neutral' || value.sentiment === 'negative' ? value.sentiment : fallback.sentiment,
    review: typeof value.review === 'string' ? value.review : fallback.review,
    reply: typeof value.reply === 'string' ? value.reply : fallback.reply,
  };
}

function normalizeWeeklyReport(value: unknown): WeeklyReport {
  if (!isRecord(value)) {
    return mockDashboard.weeklyReport;
  }

  return {
    ...mockDashboard.weeklyReport,
    ...value,
    headline: typeof value.headline === 'string' ? value.headline : mockDashboard.weeklyReport.headline,
    summary: typeof value.summary === 'string' ? value.summary : mockDashboard.weeklyReport.summary,
    score: typeof value.score === 'number' ? value.score : mockDashboard.weeklyReport.score,
    suggestions: Array.isArray(value.suggestions) ? value.suggestions.filter((item): item is string => typeof item === 'string') : mockDashboard.weeklyReport.suggestions,
  };
}

function normalizeHashtags(values: string[]) {
  return values
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => (item.startsWith('#') ? item : `#${item.replace(/^#+/, '')}`));
}

function createContentResult(input: { businessType: string; audience: string; tone: string; platform?: string }): ContentResult {
  const businessType = input.businessType?.toLowerCase() || 'business';
  const audience = input.audience?.toLowerCase() || 'customers';
  const tone = input.tone?.toLowerCase() || 'confident';
  const platform = input.platform?.toLowerCase() || 'instagram';

  const platformTag = platform === 'whatsapp' ? '#WhatsAppBusiness' : platform === 'facebook' ? '#FacebookMarketing' : platform === 'reels' ? '#InstagramReels' : '#InstagramMarketing';

  return {
    post: `A better ${businessType} experience starts with knowing what ${audience} actually care about. We built today's offer around speed, quality, and a smoother visit.`,
    caption: `Built for ${audience} who want a smarter ${businessType} moment. ${tone === 'premium' ? 'Premium service, clean execution, and a sharp offer.' : 'Fast, simple, and designed to convert.'} ${platform === 'reels' ? '🎬 Swipe for the full story.' : ''}`,
    hashtags: normalizeHashtags([
      '#AIBusinessGrowth',
      '#SmallBusiness',
      `#${businessType.replace(/\s+/g, '')}`,
      '#LocalBusiness',
      '#IndiaStartup',
      platformTag,
    ]),
    reelIdea: `Show a ${businessType} transformation in 3 scenes: before, process, and the customer reaction. Close with a strong CTA for ${audience}. Optimized for ${platform}.`,
  };
}

function createAssistantResponse(problem: string): AssistantMessage {
  const base = problem.trim() || 'How do I grow revenue with limited budget?';
  const normalized = base.toLowerCase();
  const isReview = normalized.includes('review') || normalized.includes('rating');
  const isContent = normalized.includes('post') || normalized.includes('content') || normalized.includes('social');
  const isRevenue = normalized.includes('revenue') || normalized.includes('sales') || normalized.includes('orders');

  const bullets = isReview
    ? [
        'Respond to recent negative reviews first to protect public perception.',
        'Use one clear service recovery template, then personalize each reply.',
        'Follow up with satisfied customers for fresh positive ratings.',
      ]
    : isContent
      ? [
          'Lead with one sharp value proposition in the first line.',
          'Use a clear offer, a visible deadline, and a specific CTA.',
          'Mix proof content with lifestyle content to avoid fatigue.',
        ]
      : isRevenue
        ? [
            'Increase average order value through bundles before increasing spend.',
            'Shift promotions to the highest-converting time windows.',
            'Protect margin by pairing a premium upsell with every campaign.',
          ]
        : [
            'Clarify the one metric that matters most this week.',
            'Pick one high-leverage action and execute it consistently.',
            'Review the outcome after 48 hours and adjust fast.',
          ];

  return {
    id: `a-${Date.now()}`,
    role: 'assistant',
    content: `I analyzed your problem: ${base}. The fastest path is to focus on leverage, not more activity.`,
    bullets,
    timestamp: 'Just now',
  };
}

function createReviewReplies(reviews: ReviewItem[]): ReviewItem[] {
  return reviews.map((review, index) => ({
    ...review,
    reply:
      review.sentiment === 'negative'
        ? `Thanks for the feedback, ${review.author.split(' ')[0]}. We are sorry the experience missed the mark and will address this right away.`
        : review.reply ||
          `Thanks, ${review.author.split(' ')[0]}. We appreciate your support and look forward to welcoming you again.`,
    sentiment: review.sentiment,
    id: `${review.id}-${index}`,
  }));
}

function simulateImpactMetric(metric: ImpactMetric, aggressiveness: number): ImpactMetric {
  const deltaMap = {
    revenue: 0.06,
    engagement: 0.09,
    rating: 0.05,
    orders: 0.08,
  } as const;

  const scale = deltaMap[metric.key] * aggressiveness;
  const after = metric.key === 'rating'
    ? Math.min(5, metric.before * (1 + scale))
    : metric.before * (1 + scale);

  return {
    ...metric,
    after: Number(after.toFixed(metric.key === 'rating' ? 2 : 0)),
  };
}

function createAutoModeSimulation(days = 14): AutoModeResult {
  const baseline = mockDashboard.autoMode;
  const aggressiveness = Math.min(1.35, Math.max(0.8, days / 14));
  const impact = baseline.impact.map((metric) => simulateImpactMetric(metric, aggressiveness));

  const decisions = baseline.decisions.map((decision, index) => {
    const step = index + 1;
    const confidence = Math.min(0.98, decision.confidence + (aggressiveness - 1) * 0.05);
    return {
      ...decision,
      step,
      dayLabel: `Day ${Math.min(days, step * Math.max(1, Math.floor(days / 3)))}`,
      confidence: Number(confidence.toFixed(2)),
    };
  });

  return {
    mode: 'rule+ai',
    periodLabel: `${days}-day autonomous sprint`,
    summary: `Autonomous mode executed ${decisions.length} high-leverage actions using rule checks + AI reasoning and produced measurable KPI lift.`,
    impact,
    decisions,
  };
}

async function fallbackSnapshot(): Promise<DashboardSnapshot> {
  await delay(450);
  return mockDashboard;
}

export async function fetchDashboardSnapshot(): Promise<DashboardSnapshot> {
  try {
    const response = await api.get('/dashboard');
    return normalizeDashboardSnapshot(response.data);
  } catch {
    return fallbackSnapshot();
  }
}

export async function generateContent(input: { businessType: string; audience: string; tone: string; platform?: string }): Promise<ContentResult> {
  try {
    const response = await api.post('/content/generate', input);
    return normalizeContentResult(response.data);
  } catch {
    await delay(700);
    return createContentResult(input);
  }
}

export async function analyzeReviewBatch(reviews: ReviewItem[]): Promise<ReviewItem[]> {
  try {
    const response = await api.post('/reviews/analyze', { reviews });
    return Array.isArray(response.data)
      ? response.data.map((review, index) => normalizeReview(review, reviews[index] ?? reviews[0]))
      : createReviewReplies(reviews);
  } catch {
    await delay(650);
    return createReviewReplies(reviews);
  }
}

export async function askAssistant(problem: string): Promise<AssistantMessage> {
  try {
    const response = await api.post('/assistant', { problem });
    return normalizeAssistantMessage(response.data);
  } catch {
    await delay(550);
    return createAssistantResponse(problem);
  }
}

export async function fetchWeeklyReport(): Promise<WeeklyReport> {
  try {
    const response = await api.get('/reports/weekly');
    return normalizeWeeklyReport(response.data);
  } catch {
    await delay(600);
    return mockDashboard.weeklyReport;
  }
}

export async function runAutonomousMode(input?: { days?: number }): Promise<AutoModeResult> {
  try {
    const response = await api.post('/auto-mode/run', input ?? {});
    return normalizeAutoModeResult(response.data);
  } catch {
    await delay(850);
    return createAutoModeSimulation(input?.days ?? 14);
  }
}

export async function runSimulation(input: { task_id: number; days: number }): Promise<SimulationResult> {
  try {
    const response = await api.post('/simulate/run', input);
    const data = response.data;
    if (typeof data === 'object' && data !== null && 'task_id' in data) {
      return data as SimulationResult;
    }
    return mockSimulation(input.task_id, input.days);
  } catch {
    await delay(800);
    return mockSimulation(input.task_id, input.days);
  }
}

export async function fetchFestivals(): Promise<FestivalEvent[]> {
  try {
    const response = await api.get('/festivals');
    return Array.isArray(response.data) ? response.data : mockFestivals;
  } catch {
    return mockFestivals;
  }
}
