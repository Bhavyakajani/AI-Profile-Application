import { screen } from '@testing-library/react';
import { renderWithRouter } from '../tests/utils/renderWithRouter';
import ProfileCard from './ProfileCard';

test('renders profile info correctly', () => {
  renderWithRouter(
    <ProfileCard
      profile={{
        id: 'p1',
        name: 'Jane',
        skills: ['React', 'Node'],
      }}
    />
  );

  expect(screen.getByText('Jane')).toBeInTheDocument();
  expect(screen.getByText('React')).toBeInTheDocument();
});
