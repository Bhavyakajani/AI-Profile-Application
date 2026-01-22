import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { profileAPI } from '../api';
import { useAuth } from '../contexts/AuthContext';
import './EditProfile.css';

const EditProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAdmin, isClient, isCandidate } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [profile, setProfile] = useState(null);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    contact_number: '',
    skills: '',
    YoE: '',
  });
  const [workExperiences, setWorkExperiences] = useState([]);
  const [educations, setEducations] = useState([]);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const data = await profileAPI.getById(id);
        setProfile(data);
        
        // Check RBAC: only admin OR (candidate who created the profile) can edit
        // Clients cannot edit profiles
        const canEdit = isAdmin || (isCandidate && data.creator === user?.email);
        if (!canEdit || isClient) {
          navigate(`/profile/${id}`);
          return;
        }

        setFormData({
          name: data.name || '',
          email: data.email || '',
          contact_number: data.contact_number || '',
          skills: data.skills?.join(', ') || '',
          YoE: data.YoE || '',
        });
        setEducations(
          data.educations && data.educations.length > 0
            ? data.educations.map(edu => ({
                institution: edu.institution || '',
                degree: edu.degree || '',
                start_date: edu.start_date || '',
                end_date: edu.end_date || '',
                location: edu.location || '',
                cgpa: edu.cgpa || '',
              }))
            : [
                {
                  institution: '',
                  degree: '',
                  start_date: '',
                  end_date: '',
                  location: '',
                  cgpa: '',
                },
              ]
        );
        setWorkExperiences(
          data.work_experiences && data.work_experiences.length > 0
            ? data.work_experiences.map(exp => ({
                company: exp.company || '',
                role: exp.role || '',
                start_date: exp.start_date || '',
                end_date: exp.end_date || '',
                location: exp.location || '',
              }))
            : [
                {
                  company: '',
                  role: '',
                  start_date: '',
                  end_date: '',
                  location: '',
                },
              ]
        );
      } catch (err) {
        console.error('Error fetching profile:', err);
        setError('Failed to load profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [id, isAdmin, user, navigate]);

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
        institution: '',
        degree: '',
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');

    try {
      const profileData = {
        name: formData.name,
        email: formData.email || profile?.email || undefined,
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
          .map(() => ({
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
        creator: profile?.creator || user?.email, // Preserve creator field
      };

      await profileAPI.update(id, profileData);
      navigate(`/profile/${id}`);
    } catch (err) {
      console.error('Error updating profile:', err);
      const errorDetail =
        err.response?.data?.detail || 'Failed to update profile. Please try again.';
      setError(errorDetail);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="edit-profile-page">
        <Navbar />
        <div className="loading-container">
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error && !profile) {
    return (
      <div className="edit-profile-page">
        <Navbar />
        <div className="error-container">
          <p>{error}</p>
          <button onClick={() => navigate(`/profile/${id}`)} className="btn btn-primary">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="edit-profile-page">
      <Navbar />
      <main className="edit-profile-content">
        <h1>Edit Profile</h1>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="edit-profile-form">
          <div className="form-fields-grid">
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleInputChange}
                required
                disabled={saving}
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
                disabled={saving}
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
                disabled={saving}
                placeholder="+1234567890"
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
                disabled={saving}
                placeholder="5 years"
              />
            </div>

            <div className="form-group form-group-full-width">
              <label htmlFor="skills">Skills (comma-separated)</label>
              <input
                id="skills"
                name="skills"
                type="text"
                value={formData.skills}
                onChange={handleInputChange}
                disabled={saving}
                placeholder="JavaScript, Python, React"
              />
            </div>
          </div>

          <div className="form-section">
            <div className="form-section-header">
              <h3>Education</h3>
              <button
                type="button"
                onClick={addEducation}
                className="btn btn-secondary btn-small"
                disabled={saving}
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
                      disabled={saving}
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
                      disabled={saving}
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
                      disabled={saving}
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
                      disabled={saving}
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
                      disabled={saving}
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
                      disabled={saving}
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
                disabled={saving}
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
                      disabled={saving}
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
                      value={exp.company || ''}
                      onChange={(e) =>
                        handleWorkExperienceChange(index, 'company', e.target.value)
                      }
                      disabled={saving}
                      placeholder="Company name"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor={`role-${index}`}>Role/Position</label>
                    <input
                      id={`role-${index}`}
                      type="text"
                      value={exp.role || ''}
                      onChange={(e) =>
                        handleWorkExperienceChange(index, 'role', e.target.value)
                      }
                      disabled={saving}
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
                      value={exp.start_date || ''}
                      onChange={(e) =>
                        handleWorkExperienceChange(
                          index,
                          'start_date',
                          e.target.value
                        )
                      }
                      disabled={saving}
                      placeholder="YYYY-MM or YYYY"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor={`end-date-${index}`}>End Date</label>
                    <input
                      id={`end-date-${index}`}
                      type="text"
                      value={exp.end_date || ''}
                      onChange={(e) =>
                        handleWorkExperienceChange(index, 'end_date', e.target.value)
                      }
                      disabled={saving}
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
                      value={exp.location || ''}
                      onChange={(e) =>
                        handleWorkExperienceChange(index, 'location', e.target.value)
                      }
                      disabled={saving}
                      placeholder="City, Country"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="form-actions">
            <button type="button"
              onClick={() => navigate(`/profile/${id}`)}
              className="btn btn-secondary"
              disabled={saving}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default EditProfile;
