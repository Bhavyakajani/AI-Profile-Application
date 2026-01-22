import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';
import sorcererIcon from '../icons/sorcerer.png';


const Navbar = () => {
  const { isAuthenticated, user, logout, isAdmin } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Close dropdown when clicking outside
    const handleClickOutside = (e) => {
      if (!e.target.closest('.navbar-dropdown')) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/landing');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <h1 className="navbar-title">
            ReSorcerer 
            <img src={sorcererIcon} alt="logo" className="navbar-logo-image"/> </h1>
        </Link>

        {isAuthenticated && (
          <form onSubmit={handleSearch} className="navbar-search">
            <input
              type="text"
              placeholder="Search profiles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="navbar-search-input"
            />
            <button type="submit" className="navbar-search-button">
              🔍
            </button>
          </form>
        )}

        <div className="navbar-actions">
          {isAuthenticated ? (
            <>
              {isAdmin && (
                <Link to="/admin/users" className="navbar-link admin-badge">
                  Admin
                </Link>
              )}
              <Link to="/profile/create" className="navbar-link">
                Create Profile
              </Link>
              <div className="navbar-dropdown">
                <button
                  className="navbar-user-button"
                  onClick={() => setShowDropdown(!showDropdown)}
                >
                  {user?.name || 'Account'} ▼
                </button>
                {showDropdown && (
                  <div className="navbar-dropdown-menu">
                    <Link
                      to="/account"
                      className="navbar-dropdown-item"
                      onClick={() => setShowDropdown(false)}
                    >
                      My Account
                    </Link>
                    <button
                      className="navbar-dropdown-item"
                      onClick={handleLogout}
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Login
              </Link>
              <Link to="/register" className="navbar-link navbar-button">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
