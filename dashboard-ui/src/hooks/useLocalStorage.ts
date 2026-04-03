import { useEffect, useState } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue;
    }

    let stored: string | null = null;

    try {
      stored = window.localStorage.getItem(key);
    } catch {
      return initialValue;
    }

    if (stored === null) {
      return initialValue;
    }

    try {
      return JSON.parse(stored) as T;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Ignore storage failures and keep the in-memory value active.
    }
  }, [key, value]);

  return [value, setValue] as const;
}
