'use client';

import { AuthProvider } from '@/hooks/use-auth';
import { ThemeProvider } from '@/contexts/theme-context';
import { ReactNode } from 'react';

export default function ClientWrapper({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <AuthProvider>{children}</AuthProvider>
    </ThemeProvider>
  );
}