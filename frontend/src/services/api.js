import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 用户相关API
export const userAPI = {
  // 获取所有用户
  getUsers: () => api.get('/api/users'),
  
  // 创建用户
  createUser: (userData) => api.post('/api/users', userData),
  
  // 获取单个用户
  getUser: (userId) => api.get(`/api/users/${userId}`),

    // 更新用户
  updateUser: (userId, userData) => api.put(`/api/users/${userId}`, userData),
  
  
  // 删除用户
  deleteUser: (userId) => api.delete(`/api/users/${userId}`),
}

export default api