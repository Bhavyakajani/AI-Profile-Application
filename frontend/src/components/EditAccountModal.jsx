import { useState } from 'react';
import { userAPI } from '../api';
import './EditAccountModal.css';

const EditAccountModal = ({ user, onClose, onSuccess }) => {
  const [name, setName] = useState(user.name || '');
  const [email, setEmail] = useState(user.email || '');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const updateData = {};
      if (name !== user.name) updateData.name = name;
      if (email !== user.email) updateData.email = email;
      if (password.trim()) updateData.password = password;

      if (Object.keys(updateData).length === 0) {
        onSuccess();
        return;
      }

      await userAPI.update(user.id, updateData);
      setPassword(''); // Clear password field after successful update
      onSuccess();
    } catch (err) {
      console.error('Error updating account:', err);
      const errorDetail =
        err.response?.data?.detail || 'Failed to update account. Please try again.';
      setError(errorDetail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit Account</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        {error && (
          <div className="modal-error" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">New Password (leave blank to keep current)</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              placeholder="Enter new password"
              minLength={6}
            />
            <p className="form-help">
              Minimum 6 characters. Leave blank if you don't want to change your password.
            </p>
          </div>

          <div className="modal-actions">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditAccountModal;
