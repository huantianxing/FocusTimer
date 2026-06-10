/**
 * 记录列表 Store
 *
 * 职责：
 * - 缓存今日记录 / 历史记录数据
 * - 提供分页、筛选参数管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTodayRecords, getRecords } from '@/api'

export const useRecordsStore = defineStore('records', () => {
  // ========== State ==========
  const todayRecords = ref([])      // 今日记录（带分组信息）
  const historyRecords = ref([])    // 历史查询结果
  const totalCount = ref(0)         // 历史记录总数
  const loading = ref(false)

  // 历史查询筛选参数
  const filters = ref({
    start_date: '',
    end_date: '',
    keyword: '',
    tag_id: null,
    page: 1,
    size: 20
  })

  // ========== Actions ==========

  /** 获取今日记录 */
  async function fetchTodayRecords() {
    loading.value = true
    try {
      const res = await getTodayRecords()
      if (res.code === 200) {
        todayRecords.value = res.data || []
      }
    } finally {
      loading.value = false
    }
  }

  /** 查询历史记录（带分页+筛选） */
  async function fetchHistoryRecords(params = {}) {
    loading.value = true
    // 合并筛选参数
    const mergedParams = { ...filters.value, ...params }
    filters.value = mergedParams

    try {
      const res = await getRecords(mergedParams)
      if (res.code === 200) {
        historyRecords.value = res.data?.records || res.data || []
        totalCount.value = res.data?.total || 0
      }
    } finally {
      loading.value = false
    }
  }

  /** 重置筛选条件 */
  function resetFilters() {
    filters.value = {
      start_date: '',
      end_date: '',
      keyword: '',
      tag_id: null,
      page: 1,
      size: 20
    }
  }

  return {
    todayRecords,
    historyRecords,
    totalCount,
    loading,
    filters,
    fetchTodayRecords,
    fetchHistoryRecords,
    resetFilters
  }
})
