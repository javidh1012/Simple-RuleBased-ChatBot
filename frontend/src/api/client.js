/**
 * client.js - REST API Client for communicating with the Flask backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const errorMsg = data.detail || data.message || data.error || `HTTP ${response.status}`;
    const error = new Error(errorMsg);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

export const api = {
  // Public
  async getDatasetInfo() {
    return request('/dataset/info');
  },

  async getHealth() {
    return request('/health');
  },

  // Student Verification
  async verifyStudent(studentId) {
    return request('/verify-student', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId }),
    });
  },

  // Chat message dispatch
  async sendChat(message, sessionToken = null) {
    const headers = {};
    if (sessionToken) {
      headers['Authorization'] = `Bearer ${sessionToken}`;
    }
    return request('/chat', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        message,
        session_token: sessionToken,
      }),
    });
  },

  // Protected student endpoints
  async getProfile(sessionToken) {
    return request('/student/profile', {
      method: 'GET',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },

  async getAttendance(sessionToken) {
    return request('/student/attendance', {
      method: 'GET',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },

  async getInternalMarks(sessionToken) {
    return request('/student/internal-marks', {
      method: 'GET',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },

  async getPerformance(sessionToken) {
    return request('/student/performance', {
      method: 'GET',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },

  async getRecommendations(sessionToken) {
    return request('/student/recommendations', {
      method: 'GET',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },

  async logout(sessionToken) {
    return request('/logout', {
      method: 'POST',
      headers: { Authorization: `Bearer ${sessionToken}` },
    });
  },
};

