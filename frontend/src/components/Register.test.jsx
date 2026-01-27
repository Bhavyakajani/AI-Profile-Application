import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { test, expect } from 'vitest';

test('shows error on password mismatch', async () => {
  const user = userEvent.setup();
  const { default: Register } = await import('./Register');

  renderWithRouter(<Register />);

  // 🔑 REQUIRED fields must be filled, otherwise submit never runs
  await user.type(screen.getByLabelText('Full Name'), 'Test User');
  await user.type(screen.getByLabelText('Email'), 'test@test.com');
  await user.type(screen.getByLabelText('Password'), '123456');
  await user.type(screen.getByLabelText('Confirm Password'), 'abcdef');

  await user.click(screen.getByRole('button', { name: /register/i }));

  const alert = await screen.findByRole('alert');
  expect(alert).toHaveTextContent(/passwords do not match/i);
});
