import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000', // Fallback to localhost if the env var is not set
});

export default api;
