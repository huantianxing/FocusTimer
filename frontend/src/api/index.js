/**
 * Axios 封装 + 所有 API 方法
 *
 * 统一响应格式: { code: 200, message: 'ok', data: { ... } }
 * 错误码: 400/404/409/413/422/500
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'

// ============================================================
// Axios 实例
// ============================================================
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 响应拦截器 — 统一错误提示
api.interceptors.response.use(
  (response) => {
    const { code, message } = response.data
    if (code !== 200 && code !== undefined) {
      ElMessage.warning(message || '请求异常')
    }
    return response.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      const msg = data?.message || `请求失败 (${status})`
      ElMessage.error(msg)
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查后端服务是否运行')
    } else {
      ElMessage.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

// ============================================================
// 1. 计时相关 API
// ============================================================

/** 开始计时 */
export function startTimer({ title, tag_ids = [], is_pomodoro = false }) {
  return api.post('/timer/start', { title, tag_ids, is_pomodoro })
}

/** 暂停计时 */
export function pauseTimer() {
  return api.post('/timer/pause')
}

/** 继续计时 */
export function resumeTimer() {
  return api.post('/timer/resume')
}

/** 结束计时 */
export function endTimer() {
  return api.post('/timer/end')
}

/** 获取当前计时状态 */
export function getCurrentTimer() {
  return api.get('/timer/current')
}

// ============================================================
// 2. 记录相关 API
// ============================================================

/** 获取今日记录 */
export function getTodayRecords() {
  return api.get('/records/today')
}

/** 查询历史记录 */
export function getRecords(params = {}) {
  return api.get('/records', { params })
}

/** 修改记录 */
export function updateRecord(id, data) {
  return api.put(`/records/${id}`, data)
}

/** 标记记录无效 */
export function markRecordInvalid(id, reason = '') {
  return api.post(`/records/${id}/invalid`, { reason })
}

// ============================================================
// 3. 统计相关 API
// ============================================================

/** 今日统计 */
export function getTodayStats() {
  return api.get('/stats/today')
}

/** 趋势数据 */
export function getTrendStats(days = 7) {
  return api.get('/stats/trend', { params: { range: days } })
}

/** 任务排名 */
export function getTaskRanking(params = {}) {
  return api.get('/stats/tasks', { params })
}

// ============================================================
// 4. 标签相关 API
// ============================================================

/** 获取所有标签 */
export function getTags() {
  return api.get('/tags')
}

/** 创建标签 */
export function createTag(data) {
  return api.post('/tags', data)
}

/** 修改标签 */
export function updateTag(id, data) {
  return api.put(`/tags/${id}`, data)
}

/** 删除标签 */
export function deleteTag(id) {
  return api.delete(`/tags/${id}`)
}

// ============================================================
// 5. 设置相关 API
// ============================================================

/** 获取用户设置 */
export function getSettings() {
  return api.get('/settings')
}

/** 更新用户设置 */
export function updateSettings(data) {
  return api.put('/settings', data)
}

/** 上传自定义音效 */
export function uploadSound(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/settings/sound', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// ============================================================
// 6. 模板相关 API
// ============================================================

/** 获取所有模板 */
export function getTemplates() {
  return api.get('/templates')
}

/** 创建模板 */
export function createTemplate(data) {
  return api.post('/templates', data)
}

/** 删除模板 */
export function deleteTemplate(id) {
  return api.delete(`/templates/${id}`)
}

// ============================================================
// 7. 备份 API
// ============================================================

/** 手动触发备份 */
export function triggerBackup() {
  return api.get('/backup')
}

/** 获取备份列表 */
export function getBackupList() {
  return api.get('/backup/list')
}
