import { Bot, FileText, GaugeCircle, LayoutDashboard, MessageSquareMore, Sparkles } from 'lucide-react';
import type { NavKey } from '@/types';

export const navItems: { key: NavKey; label: string; icon: typeof LayoutDashboard }[] = [
  { key: 'overview', label: 'Overview', icon: LayoutDashboard },
  { key: 'assistant', label: 'AI Assistant', icon: Bot },
  { key: 'content', label: 'Content', icon: Sparkles },
  { key: 'reviews', label: 'Reviews', icon: MessageSquareMore },
  { key: 'reports', label: 'Reports', icon: FileText },
  { key: 'auto', label: 'Auto Mode', icon: GaugeCircle },
];

export const navSummary = [
  { label: 'Today', value: '08:40' },
  { label: 'Status', value: 'Live' },
  { label: 'Confidence', value: '92%' },
  { label: 'Growth', value: '+18.2%' },
] as const;
