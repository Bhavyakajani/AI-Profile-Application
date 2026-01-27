import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { test, expect, vi } from 'vitest';

test('successful login calls auth context login', async () => {
  const loginMock = vi.fn();

  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => ({ login: loginMock }),
  }));

  vi.doMock('../api', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual,
      authAPI: {
        login: vi.fn(() =>
          Promise.resolve({ access_token: 'token' })
        ),
        getCurrentUser: vi.fn(() =>
          Promise.resolve({ status: 'approved' })
        ),
      },
    };
  });

  const { default: Login } = await import('./Login');

  const user = userEvent.setup();
  renderWithRouter(<Login />);

  await user.type(screen.getByLabelText('Email'), 'test@test.com');
  await user.type(screen.getByLabelText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: /sign in/i }));

  await waitFor(() => {
    expect(loginMock).toHaveBeenCalledWith('token');
  });
});
