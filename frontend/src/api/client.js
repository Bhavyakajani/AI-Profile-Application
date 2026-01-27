import axios from "axios";

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

export default api