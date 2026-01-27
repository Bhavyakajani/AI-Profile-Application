import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import CreateProfile from './CreateProfile';
import { clientAuth } from '../tests/utils/mockAuth';

vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => clientAuth,
}));

test('client cannot create profile', () => {
  renderWithRouter(<CreateProfile />);

  expect(
    screen.getByText(/do not have permission/i)
  ).toBeInTheDocument();
});
