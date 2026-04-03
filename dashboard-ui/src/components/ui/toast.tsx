import { useToast } from '@/hooks/useToast';
import { cn } from '@/lib/utils';
import { CheckCircle2, Info, TriangleAlert } from 'lucide-react';

const iconMap = {
  success: CheckCircle2,
  error: TriangleAlert,
  info: Info,
};

export function ToastViewport() {
  const { toasts, dismissToast } = useToast();

  return (
    <div className="pointer-events-none fixed bottom-5 right-5 z-[80] flex w-[min(92vw,380px)] flex-col gap-3">
      {toasts.map((toast) => {
        const Icon = iconMap[toast.tone ?? 'info'];
        return (
          <div
            key={toast.id}
            className={cn(
              'pointer-events-auto rounded-2xl border border-white/10 bg-card/95 p-4 shadow-2xl shadow-black/30 backdrop-blur-xl',
              toast.tone === 'success' && 'border-success/30',
              toast.tone === 'error' && 'border-danger/30',
            )}
          >
            <div className="flex items-start gap-3">
              <div className={cn('mt-0.5 rounded-xl p-2', toast.tone === 'success' && 'bg-success/15 text-success', toast.tone === 'error' && 'bg-danger/15 text-danger', toast.tone === 'info' && 'bg-primary/15 text-primary')}>
                <Icon className="h-4 w-4" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-card-foreground">{toast.title}</p>
                {toast.description ? <p className="mt-1 text-sm text-muted-foreground">{toast.description}</p> : null}
              </div>
              <button className="text-xs text-muted-foreground transition hover:text-foreground" onClick={() => dismissToast(toast.id)}>
                Dismiss
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
