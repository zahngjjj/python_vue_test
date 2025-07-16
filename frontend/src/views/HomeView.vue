<template>
  <div class="users-container">
    <h1>用户管理</h1>
    
    <!-- 添加用户表单 -->
    <div class="add-user-form">
      <h3>{{ editingUser ? '编辑用户' : '添加新用户' }}</h3>
      <form @submit.prevent="editingUser ? updateUser() : addUser()">
        <div class="form-row">
          <div class="form-group">
            <label for="name">姓名:</label>
            <input 
              type="text" 
              id="name" 
              v-model="userForm.name" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="email">邮箱:</label>
            <input 
              type="email" 
              id="email" 
              v-model="userForm.email" 
              required 
            />
          </div>
          <div class="form-actions">
            <button type="submit" :disabled="loading">
              {{ editingUser ? '更新用户' : '添加用户' }}
            </button>
            <button 
              v-if="editingUser" 
              type="button" 
              @click="cancelEdit" 
              class="cancel-btn"
            >
              取消
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- 用户表格 -->
    <div class="users-table-container">
      <h3>用户列表</h3>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="users.length === 0" class="no-users">暂无用户</div>
      <table v-else class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>姓名</th>
            <th>邮箱</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td class="actions">
              <button 
                @click="editUser(user)" 
                class="edit-btn"
                :disabled="loading"
              >
                编辑
              </button>
              <button 
                @click="deleteUser(user.id)" 
                class="delete-btn"
                :disabled="loading"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userAPI } from '../services/api'

const users = ref([])
const loading = ref(false)
const editingUser = ref(null)
const userForm = ref({
  name: '',
  email: ''
})

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await userAPI.getUsers()
    users.value = response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
    alert('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 添加用户
const addUser = async () => {
  if (!userForm.value.name || !userForm.value.email) {
    alert('请填写完整信息')
    return
  }
  
  loading.value = true
  try {
    await userAPI.createUser(userForm.value)
    userForm.value = { name: '', email: '' }
    await fetchUsers()
    alert('用户添加成功')
  } catch (error) {
    console.error('添加用户失败:', error)
    alert('添加用户失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 编辑用户
const editUser = (user) => {
  editingUser.value = user
  userForm.value = {
    name: user.name,
    email: user.email
  }
}

// 更新用户
const updateUser = async () => {
  if (!userForm.value.name || !userForm.value.email) {
    alert('请填写完整信息')
    return
  }
  
  loading.value = true
  try {
    await userAPI.updateUser(editingUser.value.id, userForm.value)
    editingUser.value = null
    userForm.value = { name: '', email: '' }
    await fetchUsers()
    alert('用户更新成功')
  } catch (error) {
    console.error('更新用户失败:', error)
    alert('更新用户失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

// 取消编辑
const cancelEdit = () => {
  editingUser.value = null
  userForm.value = { name: '', email: '' }
}

// 删除用户
const deleteUser = async (userId) => {
  if (!confirm('确定要删除这个用户吗？')) {
    return
  }
  
  loading.value = true
  try {
    await userAPI.deleteUser(userId)
    await fetchUsers()
    alert('用户删除成功')
  } catch (error) {
    console.error('删除用户失败:', error)
    alert('删除用户失败')
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 组件挂载时获取用户列表
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.add-user-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid #e9ecef;
}

.form-row {
  display: flex;
  gap: 20px;
  align-items: end;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #495057;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.15s ease-in-out;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.15s ease-in-out;
}

button[type="submit"] {
  background: #007bff;
  color: white;
}

button[type="submit"]:hover {
  background: #0056b3;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #545b62;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.users-table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.users-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
}

.users-table tbody tr:hover {
  background: #f8f9fa;
}

.actions {
  white-space: nowrap;
}

.actions button {
  padding: 6px 12px;
  margin-right: 8px;
  font-size: 12px;
}

.edit-btn {
  background: #28a745;
  color: white;
}

.edit-btn:hover {
  background: #218838;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.loading, .no-users {
  text-align: center;
  padding: 40px;
  color: #6c757d;
  font-style: italic;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    min-width: 100%;
  }
  
  .users-table-container {
    overflow-x: auto;
  }
  
  .users-table {
    min-width: 600px;
  }
}
</style>