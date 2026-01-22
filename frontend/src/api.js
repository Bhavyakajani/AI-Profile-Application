import axios from "axios";

// Note: Update this URL if your backend runs on a different port
// The backend can be configured with --port flag (default is 8000)
const api = axios.create({
    baseURL: "http://localhost:8000"
});

// Add token to requests if available
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle 401 errors (unauthorized)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            // Only redirect if not already on landing/login/register pages
            const currentPath = window.location.pathname;
            if (!['/landing', '/login', '/register'].includes(currentPath)) {
                window.location.href = '/landing';
            }
        }
        return Promise.reject(error);
    }
);

// Auth API functions
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

// Profile API functions
export const profileAPI = {
    getAll: async () => {
        const response = await api.get('/profile/');
        return response.data;
    },
    getById: async (id) => {
        const response = await api.get(`/profile/${id}`);
        return response.data;
    },
    search: async (query) => {
        const response = await api.get(`/profile/search?query=${encodeURIComponent(query)}`);
        return response.data;
    },
    create: async (profileData) => {
        const response = await api.post('/profile/', profileData);
        return response.data;
    },
    update: async (id, profileData) => {
        const response = await api.patch(`/profile/${id}`, profileData);
        return response.data;
    },
    delete: async (id) => {
        const response = await api.delete(`/profile/${id}`);
        return response.data;
    },
    parseResume: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/profile/parse', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
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

export default api;