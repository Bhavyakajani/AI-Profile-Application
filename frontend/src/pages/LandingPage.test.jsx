import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { test, expect, vi, afterEach } from 'vitest';
import { candidateAuth } from '../tests/utils/mockAuth';

afterEach(() => {
  vi.resetModules();
});

test('renders profiles list', async () => {
  // ✅ Mock auth for Navbar
  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => candidateAuth,
  }));

  // ✅ Partial mock API
  vi.doMock('../api', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual,
      profileAPI: {
        getAll: vi.fn(() =>
          Promise.resolve({
            profiles: [{ id: '1', name: 'Alice' }],
          })
        ),
      },
    };
  });

  const { default: LandingPage } = await import('./LandingPage');

  renderWithRouter(<LandingPage />);

  expect(await screen.findByText('Alice')).toBeInTheDocument();
});
