import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import EditAccountModal from '../components/EditAccountModal';
import { useAuth } from '../contexts/AuthContext';
import { profileAPI } from '../api';
import './AccountPage.css';

const AccountPage = () => {
  const { user, refreshUser, isAdmin } = useAuth();
  const [showEditModal, setShowEditModal] = useState(false);
  const [userProfiles, setUserProfiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProfiles = async () => {
      if (!user) return;
      
      setLoading(true);
      try {
        const data = await profileAPI.getAll();
        // Filter profiles created by current user
        const filtered = data.profiles.filter(
          (profile) => profile.creator === user.email
        );
        setUserProfiles(filtered);
      } catch (err) {
        console.error('Error fetching user profiles:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfiles();
  }, [user]);

  const handleEditSuccess = () => {
    refreshUser();
    setShowEditModal(false);
  };

  if (!user) {
    return (
      <div className="account-page">
        <Navbar />
        <div className="loading-container">
          <p>Loading account information...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="account-page">
      <Navbar />
      <main className="account-content">
        <h1>My Account</h1>

        <div className="account-card">
          <div className="account-header">
            <div>
              <h2>{user.name}</h2>
              <p className="account-email">{user.email}</p>
              <div className="account-badges">
                {isAdmin && <span className="badge badge-admin">Admin</span>}
                <span className={`badge badge-status badge-${user.status}`}>
                  {user.status || 'waiting'}
                </span>
              </div>
            </div>
            <button
              onClick={() => setShowEditModal(true)}
              className="btn btn-primary"
            >
              Edit Account
            </button>
          </div>

          <div className="account-stats">
            <div className="stat-item">
              <div className="stat-value">{userProfiles.length}</div>
              <div className="stat-label">Profiles Created</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{user.role || 'N/A'}</div>
              <div className="stat-label">Role</div>
            </div>
          </div>
        </div>

        {user.status === 'waiting' && (
          <div className="account-alert">
            <p>
              ⏳ Your account is pending approval. You will be able to create
              profiles once an administrator approves your account.
            </p>
          </div>
        )}

        <div className="account-profiles">
  <h2>My Profiles</h2>

  {loading ? (
    <div className="profiles-skeleton">
      <div className="skeleton-item" />
      <div className="skeleton-item" />
      <div className="skeleton-item" />
    </div>
  ) : 
          userProfiles.length > 0 ? (
            <div className="profiles-list">
              {userProfiles.map((profile) => (
                <div key={profile.id} className="profile-link-wrapper">
                  <Link to={`/profile/${profile.id}`} className="profile-link">
                    <div className="profile-link-content">
                      <h3>{profile.name || 'Unnamed Profile'}</h3>
                      {profile.skills?.length > 0 && (
                        <p className="profile-skills">
                          {profile.skills.slice(0, 3).join(', ')}
                          {profile.skills.length > 3 && '...'}
                        </p>
                      )}
                    </div>
                    <div className="profile-link-actions">
                      {(isAdmin || profile.creator === user.email) && (
                        <Link
                          to={`/profile/${profile.id}/edit`}
                          className="btn btn-edit btn-small"
                          onClick={(e) => e.stopPropagation()}
                        >
                          Edit
                        </Link>
                      )}
                      <span className="profile-link-arrow">→</span>
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-profiles">No profiles created yet.</p>
          )}
        </div>


        {isAdmin && (
          <div className="account-admin-section">
            <h2>Admin Actions</h2>
            <Link to="/admin/users" className="btn btn-primary">
              Manage Users
            </Link>
          </div>
        )}
      </main>

      {showEditModal && (
        <EditAccountModal
          user={user}
          onClose={() => setShowEditModal(false)}
          onSuccess={handleEditSuccess}
        />
      )}
    </div>
  );
};

export default AccountPage;
