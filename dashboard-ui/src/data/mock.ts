import type { DashboardSnapshot, FestivalEvent, SimulationResult } from '@/types';

export const mockDashboard: DashboardSnapshot = {
  kpis: [
    {
      label: 'Monthly Revenue',
      value: '₹12.4L',
      change: '+18.2%',
      trend: 'up',
      hint: 'vs last 30 days',
    },
    {
      label: 'Engagement Rate',
      value: '7.8%',
      change: '+1.4 pts',
      trend: 'up',
      hint: 'social growth momentum',
    },
    {
      label: 'Average Rating',
      value: '4.6',
      change: '+0.3',
      trend: 'up',
      hint: 'review quality improving',
    },
    {
      label: 'AI Actions Completed',
      value: '36',
      change: '92% on-time',
      trend: 'flat',
      hint: 'planned tasks executed',
    },
  ],
  trend: [
    { label: 'Mon', revenue: 32000, engagement: 4.2, rating: 4.1, orders: 84 },
    { label: 'Tue', revenue: 38400, engagement: 4.9, rating: 4.2, orders: 92 },
    { label: 'Wed', revenue: 41800, engagement: 5.4, rating: 4.4, orders: 105 },
    { label: 'Thu', revenue: 46600, engagement: 6.1, rating: 4.5, orders: 117 },
    { label: 'Fri', revenue: 52100, engagement: 6.9, rating: 4.6, orders: 128 },
    { label: 'Sat', revenue: 58300, engagement: 7.4, rating: 4.7, orders: 142 },
    { label: 'Sun', revenue: 61200, engagement: 7.8, rating: 4.6, orders: 137 },
  ],
  comparison: [
    { label: 'Posts Published', value: 24 },
    { label: 'Reviews Replied', value: 18 },
    { label: 'Campaign Reach', value: 86 },
    { label: 'Repeat Orders', value: 64 },
  ],
  plan: [
    {
      title: 'Launch a morning reel for peak audience',
      owner: 'AI Growth Copilot',
      duration: '15 min',
      status: 'running',
      impact: '+12% engagement',
    },
    {
      title: 'Reply to 6 high-intent reviews',
      owner: 'Review Analyzer',
      duration: '20 min',
      status: 'ready',
      impact: '+0.2 rating lift',
    },
    {
      title: 'Push weekend bundle offer',
      owner: 'Revenue Engine',
      duration: '30 min',
      status: 'queued',
      impact: '+₹18K projected',
    },
  ],
  quickActions: [
    {
      title: 'Generate post',
      description: 'Create a polished promo post in one click',
      icon: 'sparkles',
    },
    {
      title: 'Analyze reviews',
      description: 'Summarize sentiment and draft replies',
      icon: 'message-square-more',
    },
    {
      title: 'Build weekly report',
      description: 'See growth, risk, and next-best actions',
      icon: 'chart-column',
    },
  ],
  assistantMessages: [
    {
      id: 'u-1',
      role: 'user',
      content: 'How do I increase revenue this week without increasing ad spend?',
      timestamp: 'Now',
    },
    {
      id: 'a-1',
      role: 'assistant',
      content: 'Focus on conversion efficiency before spending more.',
      bullets: [
        'Bundle high-margin items with a time-bound offer.',
        'Shift social posts to the highest-performing audience slot.',
        'Reply to 5 recent reviews to strengthen purchase confidence.',
      ],
      timestamp: 'Just now',
    },
  ],
  contentResult: {
    post: 'Morning ritual, upgraded. Fresh coffee, calm music, and a workspace designed for people who move fast. Today only: order your favorite combo and get 15% off before noon.',
    caption: 'Your weekday reset starts here. Come in for the coffee, stay for the vibe. #AIBusinessGrowth #SmallBusiness #GrowthMode',
    hashtags: ['#AIBusinessGrowth', '#SmallBusiness', '#GrowthMode', '#CafeMarketing', '#LocalBusiness'],
    reelIdea: '15-second before/after reel showing the store opening, a signature drink pour, and a customer reaction with upbeat motion text.',
  },
  reviews: [
    {
      id: 'r-1',
      author: 'Ananya S.',
      location: 'Bangalore',
      rating: 5,
      sentiment: 'positive',
      review: 'The service was fast and the cappuccino was excellent. Loved the new seating area.',
      reply: 'Thanks, Ananya. We are glad you enjoyed the service and the new seating. See you again soon!',
    },
    {
      id: 'r-2',
      author: 'Rahul K.',
      location: 'Mumbai',
      rating: 4,
      sentiment: 'positive',
      review: 'Great food, but the wait time was a little longer than expected.',
      reply: 'Thanks for the honest feedback, Rahul. We are improving service speed and appreciate your patience.',
    },
    {
      id: 'r-3',
      author: 'Priya M.',
      location: 'Pune',
      rating: 3,
      sentiment: 'neutral',
      review: 'Good ambience, but the dessert selection could be better.',
      reply: 'Thanks for sharing, Priya. We are expanding the dessert menu and would love another chance to impress you.',
    },
  ],
  weeklyReport: {
    headline: 'Growth is compounding across content, reviews, and repeat orders.',
    summary: 'Revenue climbed 18.2% week-over-week while engagement crossed the 7% threshold. The fastest lift came from bundled offers and faster review response times.',
    score: 84,
    suggestions: [
      'Double down on weekday morning posts when engagement spikes.',
      'Expand high-margin bundles for the Saturday traffic window.',
      'Reply to every negative review within 2 hours to protect rating velocity.',
    ],
  },
  autoMode: {
    mode: 'rule+ai',
    periodLabel: '14-day autonomous sprint',
    summary: 'AI auto mode increased revenue while protecting ratings by sequencing low-cost local campaigns, review recovery, and offer optimization.',
    impact: [
      { key: 'revenue', label: 'Monthly Revenue', before: 1040000, after: 1240000, unit: 'INR' },
      { key: 'engagement', label: 'Engagement Rate', before: 6.2, after: 7.8, unit: '%' },
      { key: 'rating', label: 'Average Rating', before: 4.3, after: 4.6, unit: '/5' },
      { key: 'orders', label: 'Daily Orders', before: 109, after: 137, unit: 'count' },
    ],
    decisions: [
      {
        step: 1,
        dayLabel: 'Day 1',
        action: 'Localized breakfast reel + 3km radius offer push',
        rationale: 'Morning conversion was strong but underexposed among office commuters.',
        expectedImpact: '+8-10% walk-ins in weekday mornings',
        actualImpact: '+9.2% morning footfall',
        confidence: 0.88,
      },
      {
        step: 2,
        dayLabel: 'Day 4',
        action: 'Negative-review fast-response playbook with owner escalation',
        rationale: 'Sentiment dip around service-speed mentions was reducing map conversion.',
        expectedImpact: '+0.15 rating recovery and lower churn risk',
        actualImpact: '+0.18 rating recovery',
        confidence: 0.91,
      },
      {
        step: 3,
        dayLabel: 'Day 9',
        action: 'Festival-lite combo bundle with premium add-on',
        rationale: 'AOV could be lifted without discounting core menu heavily.',
        expectedImpact: '+11-14% AOV uplift',
        actualImpact: '+12.6% AOV uplift',
        confidence: 0.86,
      },
    ],
  },
};

// ── Simulation mock data ─────────────────────────────────────────────────────

const _simulationData: Record<number, SimulationResult> = {
  1: {
    task_id: 1,
    task_description: 'Social Media Growth — grow followers to 1,000+ and engagement to 5%+',
    valid_actions: ['generate_post', 'add_hashtags', 'schedule_post', 'run_ad'],
    steps: [
      { step: 1, day: 1, action: 'schedule_post', rationale: 'Engagement below 4.5% threshold — peak-hour scheduling maximizes content reach before volume investment.', expected: '+8% engagement from timing optimization', reward: 0.18, metrics: { followers: 545, engagement_rate: 0.028 } },
      { step: 2, day: 2, action: 'add_hashtags', rationale: 'Hashtag quality score 0.5 — niche + trending tag mix improves organic discovery by 2.4x.', expected: '+12% reach expansion from hashtag quality improvement', reward: 0.12, metrics: { followers: 590, engagement_rate: 0.031 } },
      { step: 3, day: 3, action: 'generate_post', rationale: 'Timing and hashtags optimized — high-quality content now compounds retention and shares.', expected: 'Sustained engagement and organic follower growth', reward: 0.22, metrics: { followers: 650, engagement_rate: 0.036 } },
      { step: 4, day: 5, action: 'run_ad', rationale: 'Follower growth lagging target pace — controlled ₹1,500 ad spend accelerates discovery at ₹7.5 per follower.', expected: 'Faster reach and follower acquisition (+200 followers)', reward: 0.28, metrics: { followers: 780, engagement_rate: 0.041 } },
      { step: 5, day: 7, action: 'generate_post', rationale: 'Ad created momentum — quality content sustains algorithmic boost and converts reach to followers.', expected: '+15% organic follower growth from content-ad synergy', reward: 0.31, metrics: { followers: 900, engagement_rate: 0.048 } },
      { step: 6, day: 9, action: 'schedule_post', rationale: 'Near 1,000 followers — final timing push to cross 5% engagement threshold and complete goal.', expected: 'Cross 5% engagement and 1,000 follower targets', reward: 0.35, metrics: { followers: 980, engagement_rate: 0.052 } },
    ],
    before: { followers: 500, engagement_rate: 0.02 },
    after: { followers: 980, engagement_rate: 0.052 },
    score: 0.82,
    period_days: 10,
  },
  2: {
    task_id: 2,
    task_description: 'Review Management — raise average rating to 4.0+ and positive sentiment to 65%+',
    valid_actions: ['reply_review', 'request_review', 'offer_discount', 'improve_service'],
    steps: [
      { step: 1, day: 1, action: 'improve_service', rationale: 'Rating at 3.1 — service quality improvements create durable lift vs. superficial review tactics.', expected: '+0.3 rating improvement from root-cause service fixes', reward: 0.20, metrics: { avg_rating: 3.3, positive_reviews: 8 } },
      { step: 2, day: 2, action: 'reply_review', rationale: 'Public responses to all reviews show responsiveness — converts neutral audience to loyal customers.', expected: '+0.1 rating from enhanced trust signals', reward: 0.15, metrics: { avg_rating: 3.5, positive_reviews: 10 } },
      { step: 3, day: 4, action: 'request_review', rationale: 'Positive review share below 55% — in-person review requests post-service achieve 40% conversion rate.', expected: '+3 new positive reviews this week', reward: 0.18, metrics: { avg_rating: 3.7, positive_reviews: 13 } },
      { step: 4, day: 6, action: 'reply_review', rationale: 'Sustained professional responses protect trust velocity and future platform conversion rate.', expected: '+0.2 sentiment velocity improvement', reward: 0.22, metrics: { avg_rating: 3.9, positive_reviews: 15 } },
      { step: 5, day: 8, action: 'request_review', rationale: 'Above 3.8 rating — requesting reviews now achieves higher acceptance from satisfied customers.', expected: '+5 new reviews from recently satisfied customers', reward: 0.25, metrics: { avg_rating: 4.1, positive_reviews: 19 } },
    ],
    before: { avg_rating: 3.1, positive_reviews: 6, total_reviews: 12 },
    after: { avg_rating: 4.1, positive_reviews: 19, total_reviews: 26 },
    score: 0.78,
    period_days: 10,
  },
  3: {
    task_id: 3,
    task_description: 'Revenue Optimization — grow monthly revenue to ₹1,20,000+ while keeping satisfaction ≥ 0.7',
    valid_actions: ['change_price', 'add_offer', 'run_campaign', 'launch_bundle'],
    steps: [
      { step: 1, day: 1, action: 'run_campaign', rationale: 'Revenue ₹80K vs target ₹1.2L — social campaign delivers fastest measurable demand lift at 3.5x ROI.', expected: '+₹14,000 revenue from ₹4,000 social campaign spend', reward: 0.24, metrics: { monthly_revenue: 94000, daily_orders: 28 } },
      { step: 2, day: 3, action: 'launch_bundle', rationale: 'AOV at ₹120 — coffee+snack bundle at ₹220 raises basket size 18% without heavy discount dependency.', expected: '+12% AOV uplift from bundle adoption', reward: 0.28, metrics: { monthly_revenue: 101000, daily_orders: 30 } },
      { step: 3, day: 5, action: 'add_offer', rationale: 'Light 10% offer stimulates conversion in off-peak windows while preserving 90% of margin.', expected: '+₹8,000 revenue from targeted offer campaign', reward: 0.19, metrics: { monthly_revenue: 108000, daily_orders: 33 } },
      { step: 4, day: 8, action: 'run_campaign', rationale: 'Email retargeting targets existing customer base at ₹400 CPM vs ₹2,400 for cold audiences.', expected: '+₹12,000 from high-conversion retention campaign', reward: 0.30, metrics: { monthly_revenue: 116000, daily_orders: 36 } },
      { step: 5, day: 10, action: 'launch_bundle', rationale: 'Premium weekend bundle compounds AOV gains — targets high-value Saturday traffic for final revenue push.', expected: 'Cross ₹1,20,000 revenue threshold and complete task', reward: 0.38, metrics: { monthly_revenue: 124000, daily_orders: 39 } },
    ],
    before: { monthly_revenue: 80000, daily_orders: 25, avg_order_value: 120.0 },
    after: { monthly_revenue: 124000, daily_orders: 39, avg_order_value: 142.0 },
    score: 0.86,
    period_days: 10,
  },
};

export function mockSimulation(taskId: number, days: number): SimulationResult {
  const base = _simulationData[taskId] ?? _simulationData[1];
  return {
    ...base,
    steps: base.steps.slice(0, days),
    period_days: days,
  };
}

// ── Festival mock data ───────────────────────────────────────────────────────

export const mockFestivals: FestivalEvent[] = [
  { name: 'Diwali', month: 10, day: 20, boost: 'HIGHEST traffic week — gift hampers, premium offers, loyalty rewards', date: '2025-10-20', days_until: 14 },
  { name: 'Bhai Dooj', month: 10, day: 22, boost: 'Sibling combos, gifting push, sweet specials', date: '2025-10-22', days_until: 16 },
  { name: 'Christmas', month: 12, day: 25, boost: 'Premium gifting, year-end celebration, party packages', date: '2025-12-25', days_until: 80 },
  { name: 'Makar Sankranti', month: 1, day: 14, boost: 'Sweets, til-gur, kite themes; family gifting window', date: '2026-01-14', days_until: 100 },
  { name: 'Holi', month: 3, day: 25, boost: 'Colour-themed menus, festive reels, family group visits', date: '2026-03-25', days_until: 170 },
];
