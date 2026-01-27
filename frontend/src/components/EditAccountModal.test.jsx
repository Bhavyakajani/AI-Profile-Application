import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { adminAuth } from '../tests/utils/mockAuth';
import { test, expect, vi } from 'vitest';

// ✅ MOCK FIRST (before importing component)
vi.mock('../api', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    userAPI: {
      update: vi.fn(() => Promise.resolve()),
    },
  };
});

test('submits updated account data', async () => {
  const onSuccess = vi.fn();
  const user = userEvent.setup();

  const { default: EditAccountModal } = await import('../components/EditAccountModal');

  render(
    <EditAccountModal
      user={adminAuth.user}
      onClose={vi.fn()}
      onSuccess={onSuccess}
    />
  );

  // 🔑 Ensure updateData is NOT empty
  await user.clear(screen.getByLabelText('Name'));
  await user.type(screen.getByLabelText('Name'), 'New Admin Name');

  await user.click(screen.getByRole('button', { name: /save changes/i }));

  await waitFor(() => {
    expect(onSuccess).toHaveBeenCalled();
  });
});
