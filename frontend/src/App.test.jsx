import { render, screen } from '@testing-library/react';
import { unauthenticated } from './tests/utils/mockAuth';
import { afterEach, test, expect, vi } from 'vitest';

afterEach(() => {
  vi.resetModules();
});

test('redirects unauthenticated user to landing', async () => {
  vi.doMock('./contexts/AuthContext', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual, // keep AuthProvider
      useAuth: () => unauthenticated,
    };
  });

  const { default: App } = await import('./App');

  render(<App />);

  // Landing page contains Login button
  expect(await screen.findByText(/login/i)).toBeInTheDocument();
});
