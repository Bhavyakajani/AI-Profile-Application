import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../api';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(email, password);
      
      // Store token temporarily to check user status
      const tempToken = response.access_token;
      localStorage.setItem('token', tempToken);
      
      // After successful login, verify user status
      // (Backend already checks this, but we verify on frontend as well)
      try {
        const userInfo = await authAPI.getCurrentUser();
        if (userInfo.status === 'waiting') {
          // This shouldn't happen if backend check works, but just in case
          localStorage.removeItem('token');
          setError('Your account is pending approval. Please wait for an administrator to approve your account.');
          return;
        }
      } catch (userErr) {
        // If we can't fetch user info, still allow login (token is valid)
        console.warn('Could not verify user status:', userErr);
      }
      
      // Update auth context with token
      login(tempToken);
      navigate('/'); // Redirect to home/dashboard after successful login
    } catch (err) {
      console.error('Login error:', err);
      if (err.response) {
        // Server responded with error
        const errorDetail = err.response.data?.detail || err.response.data?.message || err.response.data;
        setError(typeof errorDetail === 'string' ? errorDetail : 'Login failed. Please check your credentials.');
      } else if (err.request) {
        // Request was made but no response received
        setError('Unable to connect to server. Please check if the backend is running.');
      } else {
        // Something else happened
        setError(err.message || 'An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">ReSorcerer</h1>
        <h2 className="login-subtitle">Sign In</h2>
        
        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              disabled={loading}
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
              autoComplete="current-password"
            />
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <p className="login-footer">
            Don't have an account? <Link to="/register" className="login-link">Register here</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
