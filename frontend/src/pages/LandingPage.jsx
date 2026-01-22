import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ProfileCard from '../components/ProfileCard';
import { profileAPI } from '../api';
import './LandingPage.css';

const LandingPage = () => {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('q');

  useEffect(() => {
    const fetchProfiles = async () => {
      setLoading(true);
      setError('');
      try {
        let data;
        if (searchQuery) {
          data = await profileAPI.search(searchQuery);
        } else {
          data = await profileAPI.getAll();
        }
        setProfiles(data.profiles || []);
      } catch (err) {
        console.error('Error fetching profiles:', err);
        if (err.response?.status === 404 && searchQuery) {
          setError(`No profiles found matching "${searchQuery}"`);
        } else {
          setError('Failed to load profiles. Please try again later.');
        }
        setProfiles([]);
      } finally {
        setLoading(false);
      }
    };

    fetchProfiles();
  }, [searchQuery]);

  return (
    <div className="landing-page">
      <Navbar />
      <main className="landing-content">
        <div className="landing-header">
          <div className="landing-header-content">
            <h1>Profile Directory</h1>
            {searchQuery && (
              <p className="search-results-info">
                Search results for: <strong>"{searchQuery}"</strong>
              </p>
            )}
          </div>
          {searchQuery && (
            <Link to="/" className="btn btn-secondary">
              ← Back to All Profiles
            </Link>
          )}
        </div>

        {loading ? (
          <div className="loading-container">
            <p>Loading profiles...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <p>{error}</p>
          </div>
        ) : profiles.length === 0 ? (
          <div className="empty-container">
            <p>No profiles found.</p>
          </div>
        ) : (
          <>
            <div className="profiles-grid">
              {profiles.map((profile) => (
                <ProfileCard key={profile.id} profile={profile} />
              ))}
            </div>
            {profiles.length > 0 && (
              <div className="profiles-count">
                Showing {profiles.length} profile{profiles.length !== 1 ? 's' : ''}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default LandingPage;
