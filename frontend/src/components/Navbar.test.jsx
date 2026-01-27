import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { unauthenticated, adminAuth } from '../tests/utils/mockAuth';
import { afterEach, test, expect, vi } from 'vitest';

afterEach(() => {
  vi.resetModules();
});

test('shows Login and Register when unauthenticated', async () => {
  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => unauthenticated,
  }));

  const { default: Navbar } = await import('./Navbar');

  renderWithRouter(<Navbar />);

  expect(screen.getByText(/login/i)).toBeInTheDocument();
  expect(screen.getByText(/register/i)).toBeInTheDocument();
});

test('shows Admin link for admin user', async () => {
  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => adminAuth,
  }));

  const { default: Navbar } = await import('./Navbar');

  renderWithRouter(<Navbar />);

  expect(screen.getByText('Admin')).toBeInTheDocument();
});
