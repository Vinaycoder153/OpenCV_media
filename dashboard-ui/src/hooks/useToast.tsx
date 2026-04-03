import { createContext, useCallback, useContext, useMemo, useState } from 'react';

export interface ToastMessage {
  id: string;
  title: string;
  description?: string;
  tone?: 'success' | 'error' | 'info';
}

interface ToastContextValue {
  toasts: ToastMessage[];
  pushToast: (toast: Omit<ToastMessage, 'id'>) => void;
  dismissToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const dismissToast = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const pushToast = useCallback((toast: Omit<ToastMessage, 'id'>) => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    setToasts((current) => [...current, { id, ...toast }]);
    window.setTimeout(() => dismissToast(id), 3600);
  }, [dismissToast]);

  const value = useMemo(() => ({ toasts, pushToast, dismissToast }), [toasts, pushToast, dismissToast]);

  return <ToastContext.Provider value={value}>{children}</ToastContext.Provider>;
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}
