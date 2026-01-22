import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { userAPI } from '../api';
import { useAuth } from '../contexts/AuthContext';
import './AdminUsers.css';

const AdminUsers = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [updating, setUpdating] = useState(null);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }

    const fetchUsers = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await userAPI.getRoleApprovalList();
        setUsers(data);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError('Failed to load users. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [isAdmin, navigate]);

  const handleRoleUpdate = async (userId, newRole) => {
    if (!window.confirm(`Assign role "${newRole}" to this user?`)) {
      return;
    }

    setUpdating(userId);
    try {
      await userAPI.updateRole(userId, newRole);
      // Refresh the list
      const data = await userAPI.getRoleApprovalList();
      setUsers(data);
    } catch (err) {
      console.error('Error updating user role:', err);
      alert('Failed to update user role. Please try again.');
    } finally {
      setUpdating(null);
    }
  };

  const handleDelete = async (userId, userName) => {
    if (!window.confirm(`Are you sure you want to delete user "${userName}"? This action cannot be undone.`)) {
      return;
    }

    setUpdating(userId);
    try {
      await userAPI.delete(userId);
      // Refresh the list
      const data = await userAPI.getRoleApprovalList();
      setUsers(data);
    } catch (err) {
      console.error('Error deleting user:', err);
      alert('Failed to delete user. Please try again.');
    } finally {
      setUpdating(null);
    }
  };

  if (!isAdmin) {
    return null;
  }

  const waitingUsers = users.filter((u) => u.status === 'waiting');
  const approvedUsers = users.filter((u) => u.status === 'approved');

  return (
    <div className="admin-users-page">
      <Navbar />
      <main className="admin-users-content">
        <h1>User Management</h1>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <p>Loading users...</p>
          </div>
        ) : (
          <>
            {waitingUsers.length > 0 && (
              <section className="users-section">
                <h2>Pending Approval ({waitingUsers.length})</h2>
                <div className="users-table-container">
                  <table className="users-table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {waitingUsers.map((user) => (
                        <tr key={user.id}>
                          <td>{user.name}</td>
                          <td>{user.email}</td>
                          <td>
                            <span className={`badge badge-${user.status}`}>
                              {user.status}
                            </span>
                          </td>
                          <td>
                            <div className="action-buttons">
                              <select
                                onChange={(e) =>
                                  handleRoleUpdate(user.id, e.target.value)
                                }
                                disabled={updating === user.id}
                                className="role-select"
                                defaultValue=""
                              >
                                <option value="" disabled>
                                  Assign Role
                                </option>
                                <option value="admin">Admin</option>
                                <option value="candidate">Candidate</option>
                                <option value="client">Client</option>
                              </select>
                              <button
                                onClick={() => handleDelete(user.id, user.name)}
                                disabled={updating === user.id}
                                className="btn btn-danger btn-small"
                              >
                                Delete
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}

            {approvedUsers.length > 0 && (
              <section className="users-section">
                <h2>Approved Users ({approvedUsers.length})</h2>
                <div className="users-table-container">
                  <table className="users-table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {approvedUsers.map((user) => (
                        <tr key={user.id}>
                          <td>{user.name}</td>
                          <td>{user.email}</td>
                          <td>{user.role || 'N/A'}</td>
                          <td>
                            <span className={`badge badge-${user.status}`}>
                              {user.status}
                            </span>
                          </td>
                          <td>
                            <button
                              onClick={() => handleDelete(user.id, user.name)}
                              disabled={updating === user.id}
                              className="btn btn-danger btn-small"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}

            {users.length === 0 && (
              <div className="empty-container">
                <p>No users found.</p>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default AdminUsers;
