import { render, screen, fireEvent } from '@testing-library/react';
import { test, expect, vi } from 'vitest';

const navigateMock = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

test('login button navigates to login page', async () => {
  const { default: Landing } = await import('../components/Landing');

  render(<Landing />);

  fireEvent.click(screen.getByRole('button', { name: /login/i }));

  expect(navigateMock).toHaveBeenCalledWith('/login');
});
