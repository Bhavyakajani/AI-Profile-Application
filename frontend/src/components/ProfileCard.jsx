import { Link } from 'react-router-dom';
import './ProfileCard.css';

const ProfileCard = ({ profile }) => {
  return (
    <Link to={`/profile/${profile.id}`} className="profile-card">
      <div className="profile-card-header">
        <h3 className="profile-card-name">{profile.name || 'No Name'}</h3>
        {profile.email && (
          <p className="profile-card-email">{profile.email}</p>
        )}
      </div>
      
      {profile.skills && profile.skills.length > 0 && (
        <div className="profile-card-skills">
          <div className="profile-card-skills-list">
            {profile.skills.slice(0, 3).map((skill, index) => (
              <span key={index} className="profile-card-skill">
                {skill}
              </span>
            ))}
            {profile.skills.length > 3 && (
              <span className="profile-card-skill-more">
                +{profile.skills.length - 3} more
              </span>
            )}
          </div>
        </div>
      )}

      {profile.YoE && (
        <div className="profile-card-yoe">
          <strong>Experience:</strong> {profile.YoE}
        </div>
      )}

      <div className="profile-card-footer">
        <span className="profile-card-link">View Details →</span>
      </div>
    </Link>
  );
};

export default ProfileCard;
