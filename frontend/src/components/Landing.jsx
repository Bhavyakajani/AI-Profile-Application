import { useNavigate } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1 className="landing-title">ReSorcerer</h1>
        <p className="landing-subtitle">An AI-Powered Resource Discovery and Profile Management System</p>
        
        <div className="landing-actions">
          <button 
            className="landing-button primary"
            onClick={() => navigate('/login')}
          >
            Login
          </button>
          <button 
            className="landing-button secondary"
            onClick={() => navigate('/register')}
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default Landing;
