/**
 * 计时状态 Store
 *
 * 职责：
 * - 轮询 /api/timer/current（1秒间隔）获取实时计时数据
 * - 管理当前计时运行状态（进行中/已暂停/无任务）
 * - 提供开始/暂停/继续/结束的 actions
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getCurrentTimer,
  startTimer as apiStart,
  pauseTimer as apiPause,
  resumeTimer as apiResume,
  endTimer as apiEnd
} from '@/api'

export const useTimerStore = defineStore('timer', () => {
  // ========== State ==========
  const currentRecord = ref(null)      // 当前计时记录对象（来自 API）
  const isRunning = ref(false)         // 是否正在跑
  const elapsedSeconds = ref(0)        // 实时已用秒数
  let pollingTimer = null

  // ========== Getters ==========
  const hasActiveTimer = computed(() => currentRecord.value !== null)
  const statusText = computed(() => {
    if (!currentRecord.value) return '空闲'
    if (isRunning.value) return '计时中'
    return '已暂停'
  })

  // ========== Actions ==========

  /** 每秒轮询当前计时状态 */
  function startPolling() {
    stopPolling()
    _fetchCurrent()
    pollingTimer = setInterval(_fetchCurrent, 1000)
  }

  function stopPolling() {
    if (pollingTimer) {
      clearInterval(pollingTimer)
      pollingTimer = null
    }
  }

  async function _fetchCurrent() {
    try {
      const res = await getCurrentTimer()
      if (res.code === 200) {
        if (res.data) {
          currentRecord.value = res.data
          elapsedSeconds.value = res.data.elapsed_seconds || 0
          isRunning.value = res.data.is_running || false
        } else {
          // 没有进行中的计时 → 自动停止轮询，节省请求
          currentRecord.value = null
          elapsedSeconds.value = 0
          isRunning.value = false
          stopPolling()
        }
      }
    } catch {
      // 轮询失败静默处理
    }
  }

  /** 开始计时 */
  async function start({ title, tag_ids = [], is_pomodoro = false }) {
    const res = await apiStart({ title, tag_ids, is_pomodoro })
    if (res.code === 200) {
      currentRecord.value = res.data
      elapsedSeconds.value = 0
      isRunning.value = true
      startPolling()
    }
    return res
  }

  /** 暂停 */
  async function pause() {
    const res = await apiPause()
    if (res.code === 200) {
      isRunning.value = false
      currentRecord.value = res.data
    }
    return res
  }

  /** 继续 */
  async function resume() {
    const res = await apiResume()
    if (res.code === 200) {
      isRunning.value = true
      currentRecord.value = res.data
    }
    return res
  }

  /** 结束 */
  async function end() {
    const res = await apiEnd()
    if (res.code === 200) {
      stopPolling()
      currentRecord.value = null
      elapsedSeconds.value = 0
      isRunning.value = false
    }
    return res
  }

  /** 手动刷新（触发数据更新后使用） */
  async function refresh() {
    await _fetchCurrent()
  }

  return {
    currentRecord,
    isRunning,
    elapsedSeconds,
    hasActiveTimer,
    statusText,
    startPolling,
    stopPolling,
    start,
    pause,
    resume,
    end,
    refresh
  }
})
