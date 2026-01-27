import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load user info when token exists
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const userData = await authAPI.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to load user:', error);
          // Token might be invalid, clear it
          setToken(null);
          localStorage.removeItem('token');
        }
      } else {
        setUser(null);
      }
    };
    loadUser();
  }, [token]);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  const login = async (newToken) => {
    setToken(newToken);
    // User will be loaded by useEffect
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const refreshUser = async () => {
    if (token) {
      try {
        const userData = await authAPI.getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Failed to refresh user:', error);
      }
    }
  };

  const isAuthenticated = !!token;
  const isAdmin = user?.role === 'admin';
  const isClient = user?.role === 'client';
  const isCandidate = user?.role === 'candidate';

  return (
    <AuthContext.Provider value={{ 
      token, 
      user,
      login, 
      logout, 
      isAuthenticated, 
      isAdmin,
      isClient,
      isCandidate,
      loading, 
      setLoading,
      refreshUser
    }}>
      {children}
    </AuthContext.Provider>
  );
};
