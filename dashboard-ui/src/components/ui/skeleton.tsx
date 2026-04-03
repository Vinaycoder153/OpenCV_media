import { cn } from '@/lib/utils';

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn('animate-shimmer rounded-2xl bg-gradient-to-r from-white/5 via-white/15 to-white/5 bg-[length:200%_100%]', className)} />;
}
