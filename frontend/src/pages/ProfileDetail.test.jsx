import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import ProfileDetail from './ProfileDetail';
import { candidateAuth } from '../tests/utils/mockAuth';

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => candidateAuth,
}));

vi.mock('../api', () => ({
  profileAPI: {
    getById: vi.fn(() =>
      Promise.resolve({
        id: '1',
        name: 'Test Profile',
        creator: 'candidate@test.com',
        skills: ['React'],
      })
    ),
  },
}));

test('shows Edit Profile button for creator candidate', async () => {
  renderWithRouter(<ProfileDetail />, {
    route: '/profile/1',
  });

  expect(await screen.findByText('Edit Profile')).toBeInTheDocument();
});
