import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

export const analyzePrompt = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/analyze`, { prompt });
  return response.data;
};

export const optimizePrompt = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/optimize`, { prompt });
  return response.data;
};

export const compareModels = async (prompt) => {
  const response = await axios.post(`${API_BASE_URL}/compare`, { prompt });
  return response.data;
};

export const abTestPrompts = async (promptA, promptB, expectedKeywords = [], expectedFormat = null, idealLength = 100) => {
  const response = await axios.post(`${API_BASE_URL}/ab-test`, {
    prompt_a: promptA,
    prompt_b: promptB,
    expected_keywords: expectedKeywords,
    expected_format: expectedFormat,
    ideal_length: idealLength,
  });
  return response.data;
};

export const submitFeedback = async (prompt, feedback, score = null, comment = null) => {
  const response = await axios.post(`${API_BASE_URL}/feedback`, {
    prompt,
    feedback,
    score,
    comment,
  });
  return response.data;
};

export const saveDatasetEntry = async (prompt, expectedKeywords = [], expectedFormat = null, idealLength = 100, version = null) => {
  const response = await axios.post(`${API_BASE_URL}/dataset`, {
    prompt,
    expected_keywords: expectedKeywords,
    expected_format: expectedFormat,
    ideal_length: idealLength,
    version,
  });
  return response.data;
};

export const getPromptHistory = async (prompt = null) => {
  const url = prompt ? `${API_BASE_URL}/prompt-history?prompt=${encodeURIComponent(prompt)}` : `${API_BASE_URL}/prompt-history`;
  const response = await axios.get(url);
  return response.data;
};

export const savePromptVersion = async (prompt, version) => {
  const response = await axios.post(`${API_BASE_URL}/prompt-history`, {
    prompt,
    expected_keywords: [],
    expected_format: null,
    ideal_length: 100,
    version,
  });
  return response.data;
};

export const getDatasetEntries = async () => {
  const response = await axios.get(`${API_BASE_URL}/dataset`);
  return response.data;
};
