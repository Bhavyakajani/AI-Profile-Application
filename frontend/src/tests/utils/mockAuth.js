export const unauthenticated = {
  isAuthenticated: false,
  isAdmin: false,
  isClient: false,
  isCandidate: false,
  user: null,
  login: vi.fn(),
  logout: vi.fn(),
};

export const adminAuth = {
  isAuthenticated: true,
  isAdmin: true,
  isClient: false,
  isCandidate: false,
  user: { id: '1', email: 'admin@test.com', role: 'admin' },
  login: vi.fn(),
  logout: vi.fn(),
};

export const candidateAuth = {
  isAuthenticated: true,
  isAdmin: false,
  isClient: false,
  isCandidate: true,
  user: { id: '2', email: 'candidate@test.com', role: 'candidate' },
  login: vi.fn(),
  logout: vi.fn(),
};

export const clientAuth = {
  isAuthenticated: true,
  isAdmin: false,
  isClient: true,
  isCandidate: false,
  user: { id: '3', email: 'client@test.com', role: 'client' },
  login: vi.fn(),
  logout: vi.fn(),
};
