import * as React from 'react';
import { cn } from '@/lib/utils';

export const Textarea = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => (
    <textarea
      ref={ref}
      className={cn(
        'min-h-[120px] w-full rounded-2xl border border-border bg-background/70 px-4 py-3 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/30 disabled:cursor-not-allowed disabled:opacity-50',
        className,
      )}
      {...props}
    />
  ),
);
Textarea.displayName = 'Textarea';
