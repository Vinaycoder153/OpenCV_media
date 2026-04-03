export type ThemeMode = 'dark' | 'light';

export type NavKey = 'overview' | 'assistant' | 'content' | 'reviews' | 'reports' | 'auto';

export interface KpiMetric {
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down' | 'flat';
  hint: string;
}

export interface TrendPoint {
  label: string;
  revenue: number;
  engagement: number;
  rating: number;
  orders: number;
}

export interface ComparisonPoint {
  label: string;
  value: number;
}

export interface Insight {
  title: string;
  body: string;
  tone: 'positive' | 'warning' | 'neutral';
}

export interface PlanItem {
  title: string;
  owner: string;
  duration: string;
  status: 'ready' | 'running' | 'queued';
  impact: string;
}

export interface ActionItem {
  title: string;
  description: string;
  icon: string;
}

export interface AssistantMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  bullets?: string[];
  timestamp: string;
}

export interface ContentResult {
  post: string;
  caption: string;
  hashtags: string[];
  reelIdea: string;
}

export interface ReviewItem {
  id: string;
  author: string;
  location: string;
  rating: number;
  sentiment: 'positive' | 'neutral' | 'negative';
  review: string;
  reply: string;
}

export interface WeeklyReport {
  headline: string;
  summary: string;
  score: number;
  suggestions: string[];
}

export interface ImpactMetric {
  key: 'revenue' | 'engagement' | 'rating' | 'orders';
  label: string;
  before: number;
  after: number;
  unit: string;
}

export interface AutonomousDecision {
  step: number;
  dayLabel: string;
  action: string;
  rationale: string;
  expectedImpact: string;
  actualImpact: string;
  confidence: number;
}

export interface AutoModeResult {
  mode: 'rule+ai';
  periodLabel: string;
  summary: string;
  impact: ImpactMetric[];
  decisions: AutonomousDecision[];
}

export interface DashboardSnapshot {
  kpis: KpiMetric[];
  trend: TrendPoint[];
  comparison: ComparisonPoint[];
  plan: PlanItem[];
  quickActions: ActionItem[];
  assistantMessages: AssistantMessage[];
  contentResult: ContentResult;
  reviews: ReviewItem[];
  weeklyReport: WeeklyReport;
  autoMode: AutoModeResult;
}
