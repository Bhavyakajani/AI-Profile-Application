import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import { candidateAuth } from '../tests/utils/mockAuth';
import { test, expect, vi, afterEach } from 'vitest';

afterEach(() => {
  vi.resetModules();
});

test('candidate sees prefilled edit profile form (RBAC allowed)', async () => {
  // Navbar → useAuth
  vi.doMock('../contexts/AuthContext', () => ({
    useAuth: () => ({
      ...candidateAuth,
      isCandidate: true,
      isAdmin: false,
      isClient: false,
    }),
  }));

  // Route param
  vi.doMock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
      ...actual,
      useParams: () => ({ id: 'p1' }),
      useNavigate: () => vi.fn(), // prevent real navigation
    };
  });

  // 🔑 API MOCK WITH *EMAIL-BASED CREATOR*
  vi.doMock('../api', async (importOriginal) => {
    const actual = await importOriginal();
    return {
      ...actual,
      profileAPI: {
        getById: vi.fn(() =>
          Promise.resolve({
            id: 'p1',
            name: 'John Doe',
            email: 'john@doe.com',
            contact_number: '+123456789',
            skills: ['React', 'Node'],
            YoE: '3',
            creator: candidateAuth.user.email, // ✅ THIS IS THE FIX
            educations: [],
            work_experiences: [],
          })
        ),
        update: vi.fn(),
      },
    };
  });

  const { default: EditProfile } = await import('./EditProfile');

  renderWithRouter(<EditProfile />, { route: '/profile/edit/p1' });

  // ✅ Now the form WILL be populated
  expect(await screen.findByLabelText(/name/i)).toHaveValue('John Doe');
  expect(screen.getByLabelText(/email/i)).toHaveValue('john@doe.com');
  expect(screen.getByLabelText(/years of experience/i)).toHaveValue('3');
});
