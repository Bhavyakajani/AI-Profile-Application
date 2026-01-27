import { screen, fireEvent, act } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { adminAuth } from '../tests/utils/mockAuth';
import { test, expect, vi, afterEach, beforeEach } from 'vitest';

afterEach(() => {
  vi.resetModules();
  vi.restoreAllMocks();
});

beforeEach(() => {
  vi.spyOn(window, 'confirm').mockReturnValue(true);
});

test('admin can assign role to waiting user', async () => {
  const updateRoleMock = vi.fn();

  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => ({
      ...adminAuth,
      isAdmin: true,
    }),
  }));

  vi.doMock('../api', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual,
      userAPI: {
        getRoleApprovalList: vi.fn(() =>
          Promise.resolve([
            {
              id: 'u1',
              name: 'Test User',
              email: 'user@test.com',
              status: 'waiting',
            },
          ])
        ),
        updateRole: updateRoleMock,
        delete: vi.fn(),
      },
    };
  });

  const { default: AdminUsers } = await import('./AdminUsers');

  renderWithRouter(<AdminUsers />);

  expect(await screen.findByText('user@test.com')).toBeInTheDocument();

  const roleSelect = screen.getByRole('combobox');

  // ✅ Wrap async-triggering event
  await act(async () => {
    fireEvent.change(roleSelect, {
      target: { value: 'candidate' },
    });
  });

  expect(updateRoleMock).toHaveBeenCalledWith('u1', 'candidate');
});
