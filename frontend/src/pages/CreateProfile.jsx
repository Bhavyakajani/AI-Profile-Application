import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { profileAPI } from '../api';
import { useAuth } from '../contexts/AuthContext';
import './CreateProfile.css';

const CreateProfile = () => {
  const navigate = useNavigate();
  const { isClient } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [useFileUpload, setUseFileUpload] = useState(false);
  
  // Form fields
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    contact_number: '',
    skills: '',
    YoE: '',
  });
  const [workExperiences, setWorkExperiences] = useState([
    {
      company: '',
      role: '',
      start_date: '',
      end_date: '',
      location: '',
    },
  ]);

  const [educations, setEducations] = useState([
    {
      degree: '',
      institution: '',
      start_date: '',
      end_date: '',
      location: '',
      cgpa: '',
    }
  ]);

  const [selectedFile, setSelectedFile] = useState(null);

  // Check if user is client (clients can't create profiles)
  if (isClient) {
    return (
      <div className="create-profile-page">
        <Navbar />
        <div className="error-container">
          <p>You do not have permission to create profiles.</p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

   const handleEducationChange = (index, field, value) => {
    const updated = [...educations];
    updated[index] = { ...updated[index], [field]: value };
    setEducations(updated);
  };

  const addEducation = () => {
    setEducations([
      ...educations,
      {
        degree: '',
        institution: '',
        start_date: '',
        end_date: '',
        location: '',
        cgpa: '',
      },
    ]);
  };

  const removeEducation = (index) => {
    if (educations.length > 1) {
      setEducations(educations.filter((_, i) => i !== index));
    }
  };



  const handleWorkExperienceChange = (index, field, value) => {
    const updated = [...workExperiences];
    updated[index] = { ...updated[index], [field]: value };
    setWorkExperiences(updated);
  };

  const addWorkExperience = () => {
    setWorkExperiences([
      ...workExperiences,
      {
        company: '',
        role: '',
        start_date: '',
        end_date: '',
        location: '',
      },
    ]);
  };

  const removeWorkExperience = (index) => {
    if (workExperiences.length > 1) {
      setWorkExperiences(workExperiences.filter((_, i) => i !== index));
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const profile = await profileAPI.parseResume(selectedFile);
      setSuccess('Profile created successfully from resume!');
      setTimeout(() => {
        navigate(`/profile/${profile.id}`);
      }, 2000);
    } catch (err) {
      console.error('Error parsing resume:', err);
      const errorDetail =
        err.response?.data?.detail || 'Failed to parse resume. Please try again.';
      setError(errorDetail);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const profileData = {
        name: formData.name,
        email: formData.email || undefined,
        contact_number: formData.contact_number || undefined,
        skills: formData.skills
          ? formData.skills.split(',').map((s) => s.trim()).filter(Boolean)
          : [],
        YoE: formData.YoE || undefined,
        educations: educations
          .filter(
            (edu) =>
              edu.institution || edu.degree || edu.start_date || edu.end_date
          )
          .map((edu) => ({
            institution: edu.institution || undefined,
            degree: edu.degree || undefined,
            start_date: edu.start_date || undefined,
            end_date: edu.end_date || undefined,
            location: edu.location || undefined,
            cgpa: edu.cgpa || undefined,
          })),
        work_experiences: workExperiences
          .filter(
            (exp) =>
              exp.company || exp.role || exp.start_date || exp.end_date
          )
          .map((exp) => ({
            company: exp.company || undefined,
            role: exp.role || undefined,
            start_date: exp.start_date || undefined,
            end_date: exp.end_date || undefined,
            location: exp.location || undefined,
          })),
      };

      const profile = await profileAPI.create(profileData);
      setSuccess('Profile created successfully!');
      setTimeout(() => {
        navigate(`/profile/${profile.id}`);
      }, 2000);
    } catch (err) {
      console.error('Error creating profile:', err);
      const errorDetail =
        err.response?.data?.detail || 'Failed to create profile. Please try again.';
      setError(errorDetail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-profile-page">
      <Navbar />
      <main className="create-profile-content">
        <h1>Create New Profile</h1>

        <div className="create-profile-tabs">
          <button
            className={`tab-button ${!useFileUpload ? 'active' : ''}`}
            onClick={() => setUseFileUpload(false)}
          >
            Manual Entry
          </button>
          <button
            className={`tab-button ${useFileUpload ? 'active' : ''}`}
            onClick={() => setUseFileUpload(true)}
          >
            AI Assist
          </button>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message" role="alert">
            {success}
          </div>
        )}

        {useFileUpload ? (
          <form onSubmit={handleFileUpload} className="create-profile-form">
            <div className="form-group">
              <label htmlFor="file">Upload Resume (PDF, PPTX, JPG, PNG)</label>
              <input
                id="file"
                type="file"
                accept=".pdf,.pptx,.jpg,.jpeg,.png"
                onChange={handleFileChange}
                required
                disabled={loading}
              />
              <p className="form-help">
                Supported formats: PDF, PPTX, JPG, JPEG, PNG
              </p>
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading || !selectedFile}>
                {loading ? 'Processing...' : 'Upload & Parse Resume'}
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleFormSubmit} className="create-profile-form">
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleInputChange}
                required
                disabled={loading}
                placeholder="Full name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                disabled={loading}
                placeholder="email@example.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="contact_number">Contact Number</label>
              <input
                id="contact_number"
                name="contact_number"
                type="tel"
                value={formData.contact_number}
                onChange={handleInputChange}
                disabled={loading}
                placeholder="+1234567890"
              />
            </div>

            <div className="form-group">
              <label htmlFor="skills">Skills (comma-separated)</label>
              <input
                id="skills"
                name="skills"
                type="text"
                value={formData.skills}
                onChange={handleInputChange}
                disabled={loading}
                placeholder="JavaScript, Python, React"
              />
            </div>

            <div className="form-group">
              <label htmlFor="YoE">Years of Experience</label>
              <input
                id="YoE"
                name="YoE"
                type="text"
                value={formData.YoE}
                onChange={handleInputChange}
                disabled={loading}
                placeholder="5 years"
              />
            </div>
            <div className="form-section">
            <div className="form-section-header">
              <h3>Education</h3>
              <button
                type="button"
                onClick={addEducation}
                className="btn btn-secondary btn-small"
                disabled={loading}
              >
                + Add Education
              </button>
            </div>
            {educations.map((edu, index) => (
              <div key={index} className="education-group">
                <div className="education-header">
                  <h4>Education {index + 1}</h4>
                  {educations.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeEducation(index)}
                      className="btn btn-danger btn-small"
                      disabled={loading}
                    >
                      Remove
                    </button>
                  )}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor={`degree-${index}`}>Degree</label>
                    <input
                      id={`degree-${index}`}
                      type="text"
                      value={edu.degree || ''}
                      onChange={(e) =>
                        handleEducationChange(index, 'degree', e.target.value)
                      }
                      disabled={loading}
                      placeholder="Degree name"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor={`role-${index}`}>Insitution</label>
                    <input
                      id={`role-${index}`}
                      type="text"
                      value={edu.institution || ''}
                      onChange={(e) =>
                        handleEducationChange(index, 'institution', e.target.value)
                      }
                      disabled={loading}
                      placeholder="Institution name"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor={`start-date-${index}`}>Start Date</label>
                    <input
                      id={`start-date-${index}`}
                      type="text"
                      value={edu.start_date || ''}
                      onChange={(e) =>
                        handleEducationChange(
                          index,
                          'start_date',
                          e.target.value
                        )
                      }
                      disabled={loading}
                      placeholder="YYYY-MM or YYYY"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor={`end-date-${index}`}>End Date</label>
                    <input
                      id={`end-date-${index}`}
                      type="text"
                      value={edu.end_date || ''}
                      onChange={(e) =>
                        handleEducationChange(index, 'end_date', e.target.value)
                      }
                      disabled={loading}
                      placeholder="YYYY-MM or YYYY"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group form-group-full-width">
                    <label htmlFor={`location-${index}`}>Location</label>
                    <input
                      id={`location-${index}`}
                      type="text"
                      value={edu.location || ''}
                      onChange={(e) =>
                        handleEducationChange(index, 'location', e.target.value)
                      }
                      disabled={loading}
                      placeholder="City, Country"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

            <div className="form-section">
              <div className="form-section-header">
                <h3>Work Experience</h3>
                <button
                  type="button"
                  onClick={addWorkExperience}
                  className="btn btn-secondary btn-small"
                  disabled={loading}
                >
                  + Add Experience
                </button>
              </div>

              {workExperiences.map((exp, index) => (
                <div key={index} className="work-experience-group">
                  <div className="work-experience-header">
                    <h4>Experience {index + 1}</h4>
                    {workExperiences.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeWorkExperience(index)}
                        className="btn btn-danger btn-small"
                        disabled={loading}
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label htmlFor={`company-${index}`}>Company</label>
                      <input
                        id={`company-${index}`}
                        type="text"
                        value={exp.company}
                        onChange={(e) =>
                          handleWorkExperienceChange(index, 'company', e.target.value)
                        }
                        disabled={loading}
                        placeholder="Company name"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor={`role-${index}`}>Role/Position</label>
                      <input
                        id={`role-${index}`}
                        type="text"
                        value={exp.role}
                        onChange={(e) =>
                          handleWorkExperienceChange(index, 'role', e.target.value)
                        }
                        disabled={loading}
                        placeholder="Job title"
                      />
                    </div>
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label htmlFor={`start-date-${index}`}>Start Date</label>
                      <input
                        id={`start-date-${index}`}
                        type="text"
                        value={exp.start_date}
                        onChange={(e) =>
                          handleWorkExperienceChange(
                            index,
                            'start_date',
                            e.target.value
                          )
                        }
                        disabled={loading}
                        placeholder="YYYY-MM or YYYY"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor={`end-date-${index}`}>End Date</label>
                      <input
                        id={`end-date-${index}`}
                        type="text"
                        value={exp.end_date}
                        onChange={(e) =>
                          handleWorkExperienceChange(index, 'end_date', e.target.value)
                        }
                        disabled={loading}
                        placeholder="YYYY-MM or YYYY"
                      />
                    </div>
                  </div>

                  <div className="form-row">
                    <div className="form-group form-group-full-width">
                      <label htmlFor={`location-${index}`}>Location</label>
                      <input
                        id={`location-${index}`}
                        type="text"
                        value={exp.location}
                        onChange={(e) =>
                          handleWorkExperienceChange(index, 'location', e.target.value)
                        }
                        disabled={loading}
                        placeholder="City, Country"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Creating...' : 'Create Profile'}
              </button>
            </div>
          </form>
        )}
      </main>
    </div>
  );
};

export default CreateProfile;
