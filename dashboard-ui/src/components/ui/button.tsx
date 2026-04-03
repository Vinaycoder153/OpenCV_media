import * as React from 'react';
import { cn } from '@/lib/utils';

const buttonVariants = {
  default: 'bg-primary text-primary-foreground shadow-lg shadow-primary/20 hover:translate-y-[-1px] hover:shadow-primary/30',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
  ghost: 'bg-transparent text-foreground hover:bg-white/5',
  outline: 'border border-border bg-transparent text-foreground hover:bg-white/5',
  subtle: 'bg-white/5 text-foreground hover:bg-white/10',
};

const buttonSizes = {
  sm: 'h-9 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
  lg: 'h-11 px-5 text-sm',
  icon: 'h-10 w-10',
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof buttonSizes;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-2xl font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50',
        buttonVariants[variant],
        buttonSizes[size],
        className,
      )}
      {...props}
    />
  ),
);
Button.displayName = 'Button';
