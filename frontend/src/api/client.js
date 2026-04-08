import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const analyzePrompt = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/analyze`, { prompt });
  return response.data;
};

export const optimizePrompt = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/optimize`, { prompt });
  return response.data;
};

export const compareModels = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/compare-models`, { prompt });
  return response.data;
};
