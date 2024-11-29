import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL;

const authAxios = axios.create({
  baseURL,
});

authAxios.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken"); 
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

authAxios.defaults.xsrfHeaderName = "X-CSRFToken";
authAxios.defaults.xsrfCookieName = "csrftoken";


export default authAxios;
