import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:5000' });

api.interceptors.request.use(config => {
  const token = localStorage.getItem('travel_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('travel_token');
      localStorage.removeItem('travel_user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export const authApi = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  register: (data) => api.post('/api/auth/register', data),
  me: () => api.get('/api/auth/me'),
};

export const userApi = {
  getProfile: () => api.get('/api/user/profile'),
  updateProfile: (data) => api.put('/api/user/profile', data),
  getTrips: () => api.get('/api/user/trips'),
  saveTrip: (data) => api.post('/api/user/trips', data),
  getTrip: (id) => api.get(`/api/user/trips/${id}`),
  deleteTrip: (id) => api.delete(`/api/user/trips/${id}`),
};

export const destinationsApi = {
  list: (params) => api.get('/api/destinations/', { params }),
  get: (id) => api.get(`/api/destinations/${id}`),
  addReview: (id, data) => api.post(`/api/destinations/${id}/review`, data),
};

export const aiApi = {
  generateItinerary: (data) => api.post('/api/ai/generate-itinerary', data),
  recommend: (data) => api.post('/api/ai/recommend-destinations', data),
  estimateBudget: (data) => api.post('/api/ai/estimate-budget', data),
  compareDestinations: (data) => api.post('/api/ai/compare-destinations', data),
  foodRecommendations: (destination) => api.post('/api/ai/food-recommendations', { destination }),
};

export const adminApi = {
  stats: () => api.get('/api/admin/stats'),
  users: () => api.get('/api/admin/users'),
  createDestination: (data) => api.post('/api/admin/destinations', data),
  updateDestination: (id, data) => api.put(`/api/admin/destinations/${id}`, data),
  deleteDestination: (id) => api.delete(`/api/admin/destinations/${id}`),
};

export default api;
