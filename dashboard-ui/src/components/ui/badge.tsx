import * as React from 'react';
import { cn } from '@/lib/utils';

const badgeVariants = {
  default: 'bg-white/10 text-foreground',
  success: 'bg-success/15 text-success',
  warning: 'bg-warning/15 text-warning',
  danger: 'bg-danger/15 text-danger',
  outline: 'border border-border bg-transparent text-muted-foreground',
};

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: keyof typeof badgeVariants;
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wide',
        badgeVariants[variant],
        className,
      )}
      {...props}
    />
  );
}
