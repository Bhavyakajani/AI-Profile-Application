import api from './client';
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