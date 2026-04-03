import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import type { ThemeMode } from '@/types';

export function useThemeMode() {
  const [theme, setTheme] = useLocalStorage<ThemeMode>('ai-business-growth-theme', 'dark');

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.dataset.theme = theme;
    }
  }, [theme]);

  return {
    theme,
    setTheme,
    toggleTheme: () => setTheme(theme === 'dark' ? 'light' : 'dark'),
  };
}
