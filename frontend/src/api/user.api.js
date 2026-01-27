// Auth API functions
import api from './client';
export const authAPI = {
    login: async (email, password) => {
        // OAuth2PasswordRequestForm expects form data, not JSON
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await api.post('/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },
    register: async (name, email, password) => {
        const response = await api.post('/user/register', {
            name,
            email,
            password,
        });
        return response.data;
    },
    getCurrentUser: async () => {
        const response = await api.get('/user/me');
        return response.data;
    },
};

// User API functions
export const userAPI = {
    getById: async (id) => {
        const response = await api.get(`/user/${id}`);
        return response.data;
    },
    update: async (id, userData) => {
        const response = await api.patch(`/user/${id}`, userData);
        return response.data;
    },
    delete: async (id) => {
        const response = await api.delete(`/user/${id}`);
        return response.data;
    },
    getRoleApprovalList: async () => {
        const response = await api.get('/user/role-approval-list');
        return response.data;
    },
    updateRole: async (id, role) => {
        const response = await api.patch(`/user/${id}/role?role=${role}`);
        return response.data;
    },
};