import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { adminAuth } from '../tests/utils/mockAuth';
import { test, expect, vi, afterEach } from 'vitest';

afterEach(() => vi.resetModules());

test('shows admin actions for admin user', async () => {
  // Mock auth
  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => adminAuth,
  }));

  // PARTIAL mock of api
  vi.doMock('../api', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual,
      userAPI: {
        getById: vi.fn(() =>
          Promise.resolve({
            id: '1',
            profiles: [],
          })
        ),
      },
      profileAPI: {
        getAll: vi.fn(() => Promise.resolve([])),
      },
    };
  });

  const { default: AccountPage } = await import('./AccountPage');

  renderWithRouter(<AccountPage />);

  expect(await screen.findByText(/admin actions/i)).toBeInTheDocument();
  expect(screen.getByText(/my account/i)).toBeInTheDocument();
  expect(screen.getByText(adminAuth.user.email)).toBeInTheDocument();

});
