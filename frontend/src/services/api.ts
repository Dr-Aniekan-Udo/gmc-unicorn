import axios from 'axios'

// API base configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Health Check API
export const healthCheck = async () => {
  const response = await apiClient.get('/api/v1/health')
  return response.data
}

// Calculations API
export const getCalculations = async (projectId: string) => {
  const response = await apiClient.get('/api/v1/calculations', {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

export const createCalculation = async (calculationData: any, projectId: string) => {
  const response = await apiClient.post('/api/v1/calculations', calculationData, {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

export const updateCalculation = async (id: string, calculationData: any, projectId: string) => {
  const response = await apiClient.put(`/api/v1/calculations/${id}`, calculationData, {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

export const deleteCalculation = async (id: string, projectId: string) => {
  const response = await apiClient.delete(`/api/v1/calculations/${id}`, {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

// Knowledge Graph API
export const getKnowledgeGraph = async (projectId: string) => {
  const response = await apiClient.get('/api/v1/knowledge/graph', {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

export const getKnowledgeRules = async (projectId: string) => {
  const response = await apiClient.get('/api/v1/knowledge/rules', {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

// User Management API
export const login = async (credentials: { email: string; password: string }) => {
  const response = await apiClient.post('/api/v1/users/login', credentials)
  return response.data
}

export const register = async (userData: { 
  email: string; 
  password: string; 
  name: string 
}) => {
  const response = await apiClient.post('/api/v1/users/register', userData)
  return response.data
}

export const getUserProfile = async (token?: string) => {
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {}
  const response = await apiClient.get('/api/v1/users/profile', { headers })
  return response.data
}

export const updateUserProfile = async (userData: any) => {
  const response = await apiClient.put('/api/v1/users/profile', userData)
  return response.data
}

// Project Management API
export const getUserProjects = async () => {
  const response = await apiClient.get('/api/v1/users/projects')
  return response.data
}

export const createProject = async (projectData: { name: string; description?: string }) => {
  const response = await apiClient.post('/api/v1/projects', projectData)
  return response.data
}

export const getProjectDetails = async (projectId: string) => {
  const response = await apiClient.get(`/api/v1/projects/${projectId}`, {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

// AI Coaching API
export const sendMessage = async (message: string, projectId: string) => {
  const response = await apiClient.post('/api/v1/coaching/message', 
    { message },
    { headers: { 'X-Project-ID': projectId } }
  )
  return response.data
}

export const getConversationHistory = async (projectId: string) => {
  const response = await apiClient.get('/api/v1/coaching/conversations', {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

// Analytics API
export const getAnalytics = async (projectId: string, timeRange?: string) => {
  const params = timeRange ? { time_range: timeRange } : {}
  const response = await apiClient.get('/api/v1/analytics/dashboard', {
    headers: { 'X-Project-ID': projectId },
    params
  })
  return response.data
}

export const getPerformanceMetrics = async (projectId: string) => {
  const response = await apiClient.get('/api/v1/analytics/performance', {
    headers: { 'X-Project-ID': projectId }
  })
  return response.data
}

// File Upload API
export const uploadFile = async (file: File, projectId: string) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await apiClient.post('/api/v1/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'X-Project-ID': projectId
    }
  })
  return response.data
}

export const downloadFile = async (fileId: string, projectId: string) => {
  const response = await apiClient.get(`/api/v1/files/${fileId}/download`, {
    headers: { 'X-Project-ID': projectId },
    responseType: 'blob'
  })
  return response.data
}

// Utility functions
export const isApiError = (error: any): error is { response: { status: number; data: any } } => {
  return error && error.response && typeof error.response.status === 'number'
}

export const getErrorMessage = (error: any): string => {
  if (isApiError(error)) {
    return error.response.data?.message || error.response.data?.error || 'An error occurred'
  }
  return error.message || 'An unexpected error occurred'
}

export default apiClient