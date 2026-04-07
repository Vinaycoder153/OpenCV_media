import { useMemo } from 'react';
import { BarChart3, MoonStar, SunMedium, Sparkles, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Switch } from '@/components/ui/switch';
import { cn } from '@/lib/utils';
import type { NavKey, ThemeMode } from '@/types';
import { navItems, navSummary } from './navigation';

interface AppShellProps {
  activePage: NavKey;
  onPageChange: (page: NavKey) => void;
  theme: ThemeMode;
  onToggleTheme: () => void;
  children: React.ReactNode;
}

export function AppShell({ activePage, onPageChange, theme, onToggleTheme, children }: AppShellProps) {
  const title = useMemo(() => {
    const current = navItems.find((item) => item.key === activePage);
    return current?.label ?? 'Overview';
  }, [activePage]);

  return (
    <div className="min-h-screen text-foreground">
      <div className="mx-auto flex min-h-screen w-full max-w-[1600px] gap-0 lg:gap-6">
        <aside className="sticky top-0 hidden h-screen w-80 shrink-0 flex-col border-r border-white/10 bg-white/5 p-6 backdrop-blur-xl lg:flex">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-accent text-white shadow-lg shadow-primary/30">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="text-lg font-semibold leading-none">AI Business Growth</p>
              <p className="mt-1 text-xs uppercase tracking-[0.22em] text-muted-foreground">OpenEnv Platform</p>
            </div>
          </div>

          <Separator className="my-6 bg-white/10" />

          <nav className="flex flex-1 flex-col gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = item.key === activePage;
              return (
                <button
                  key={item.key}
                  onClick={() => onPageChange(item.key)}
                  className={cn(
                    'flex items-center gap-3 rounded-2xl px-4 py-3 text-left transition-all duration-200',
                    active
                      ? 'bg-primary/15 text-primary shadow-glow'
                      : 'text-muted-foreground hover:bg-white/5 hover:text-foreground',
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="mt-6 rounded-[1.5rem] border border-white/10 bg-gradient-to-br from-primary/15 via-primary/8 to-accent/10 p-5">
            <p className="text-sm font-semibold">Today&apos;s AI Plan</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Double down on high-leverage content, fast review replies, and one focused revenue move.
            </p>
            <Button className="mt-4 w-full" variant="default" onClick={() => onPageChange('overview')}>
              Open plan <ArrowRight className="h-4 w-4" />
            </Button>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3 text-xs text-muted-foreground">
            {navSummary.map((item) => (
              <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                <div className="uppercase tracking-[0.22em]">{item.label}</div>
                <div className="mt-1 text-base font-semibold text-foreground">{item.value}</div>
              </div>
            ))}
          </div>
        </aside>

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-40 border-b border-white/10 bg-background/80 backdrop-blur-xl">
            <div className="flex items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-muted-foreground">AI Business Growth OpenEnv Platform</p>
                <h1 className="mt-1 text-xl font-semibold sm:text-2xl">{title}</h1>
              </div>

              <div className="flex items-center gap-3">
                <div className="hidden items-center gap-3 rounded-full border border-white/10 bg-white/5 px-3 py-2 md:flex">
                  <SunMedium className="h-4 w-4 text-warning" />
                  <Switch checked={theme === 'dark'} onCheckedChange={onToggleTheme} aria-label="Toggle theme" />
                  <MoonStar className="h-4 w-4 text-primary" />
                </div>
                <Button variant="secondary" className="hidden sm:inline-flex">
                  <BarChart3 className="h-4 w-4" />
                  Connect API
                </Button>
              </div>
            </div>
          </header>

          <main className="flex-1 px-4 py-5 pb-28 sm:px-6 lg:px-8 lg:py-8">{children}</main>
        </div>
      </div>

      <nav className="fixed inset-x-0 bottom-0 z-50 border-t border-white/10 bg-background/95 px-3 py-2 backdrop-blur-xl lg:hidden">
        <div className="grid grid-cols-5 gap-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = item.key === activePage;
            return (
              <button
                key={item.key}
                onClick={() => onPageChange(item.key)}
                className={cn(
                  'flex flex-col items-center justify-center gap-1 rounded-2xl px-2 py-2 text-[11px] transition-all',
                  active ? 'bg-primary/15 text-primary' : 'text-muted-foreground',
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </button>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
