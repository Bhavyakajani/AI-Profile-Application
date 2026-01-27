import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { profileAPI } from '../api';
import { useAuth } from '../contexts/AuthContext';
import './ProfileDetail.css';

const ProfileDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAdmin, isClient, isCandidate, user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await profileAPI.getById(id);
        setProfile(data);
      } catch (err) {
        console.error('Error fetching profile:', err);
        setError('Failed to load profile. It may not exist.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [id]);

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this profile? This action cannot be undone.')) {
      return;
    }

    setDeleting(true);
    try {
      await profileAPI.delete(id);
      navigate('/');
    } catch (err) {
      console.error('Error deleting profile:', err);
      alert('Failed to delete profile. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  // Check if user can edit/delete: admin OR (candidate who created the profile)
  // Clients cannot edit/delete profiles
  const canEditOrDelete = profile && user && (
    isAdmin || 
    (isCandidate && profile.creator === user.email)
  );

  if (loading) {
    return (
      <div className="profile-detail-page">
        <Navbar />
        <div className="loading-container">
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="profile-detail-page">
        <Navbar />
        <div className="error-container">
          <p>{error || 'Profile not found'}</p>
          <Link to="/" className="back-link">← Back to Profiles</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-detail-page">
      <Navbar />
      <main className="profile-detail-content">
        <Link to="/" className="back-link">← Back to Profiles</Link>

        <div className="profile-detail-header">
          <div>
            <h1>{profile.name || 'No Name'}</h1>
            {profile.email && <p className="profile-email">{profile.email}</p>}
            {profile.contact_number && (
              <p className="profile-contact">📞 {profile.contact_number}</p>
            )}
            {profile.YoE && (
              <p className="profile-yoe">💼 Years of Experience: {profile.YoE}</p>
            )}
          </div>
          {canEditOrDelete && (
            <div className="profile-actions">
              <Link
                to={`/profile/${id}/edit`}
                className="btn btn-primary"
              >
                Edit Profile
              </Link>
              {isAdmin && (
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="btn btn-danger"
                >
                  {deleting ? 'Deleting...' : 'Delete Profile'}
                </button>
              )}
            </div>
          )}
        </div>

        {profile.skills && profile.skills.length > 0 && (
          <div className="profile-section">
            <h2>Skills</h2>
            <div className="skills-list">
              {profile.skills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {profile.educations && profile.educations.length > 0 && (
          <div className="profile-section">
            <h2>Education</h2>
            <div className="education-list">
              {profile.educations.map((edu, index) => (
                <div key={index} className="education-item">
                  <h3>{edu.degree || 'Degree Not Specified'}</h3>
                  <p className="institution">{edu.institution}</p>
                  {(edu.start_date || edu.end_date) && (
                    <p className="dates">
                      {edu.start_date || 'Start'} - {edu.end_date || 'Present'}
                    </p>
                  )}
                  {edu.location && <p className="location">📍 {edu.location}</p>}
                  {edu.cgpa && <p className="cgpa">CGPA: {edu.cgpa}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {profile.work_experiences && profile.work_experiences.length > 0 && (
          <div className="profile-section">
            <h2>Work Experience</h2>
            <div className="experience-list">
              {profile.work_experiences.map((exp, index) => (
                <div key={index} className="experience-item">
                  <h3>{exp.role || 'Role Not Specified'}</h3>
                  <p className="company">{exp.company}</p>
                  {(exp.start_date || exp.end_date) && (
                    <p className="dates">
                      {exp.start_date || 'Start'} - {exp.end_date || 'End Date Not Specified'}
                    </p>
                  )}
                  {exp.location && <p className="location">📍 {exp.location}</p>}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ProfileDetail;
