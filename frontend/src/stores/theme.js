/**
 * 主题模式 Store
 *
 * 职责：
 * - 管理主题状态（system / light / dark）
 * - 持久化：localStorage 即时生效 + API 写入 user_settings 表
 * - 系统跟随：监听 matchMedia 变化自动切换
 * - 不再独立调 GET /api/settings，改由 App.vue 从 settingsStore 统一分发
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { updateSettings } from '@/api'

const THEME_STORAGE_KEY = 'timerfocus-theme'

// 防抖：避免切换主题时频繁 PUT
let debounceTimer = null
function debouncedPersist(data) {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    updateSettings(data).catch(() => {})
  }, 500)
}

export const useThemeStore = defineStore('theme', () => {
  // ========== State ==========
  const mode = ref('system')        // 'system' | 'light' | 'dark'
  const resolved = ref('light')     // 实际生效的模式

  // ========== Internal ==========
  let mediaQuery = null

  function applyTheme(resolvedMode) {
    resolved.value = resolvedMode
    document.documentElement.setAttribute('data-theme', resolvedMode)
  }

  function getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  function onSystemChange(e) {
    if (mode.value === 'system') {
      applyTheme(e.matches ? 'dark' : 'light')
    }
  }

  // ========== Actions ==========

  /** 从 settingsStore 统一数据源加载（不再独立调 GET /api/settings） */
  function loadFromData(settingsData) {
    if (settingsData?.theme_mode) {
      setMode(settingsData.theme_mode, false)
    }
  }

  /** 设置主题模式 */
  function setMode(newMode, persist = true) {
    if (!['system', 'light', 'dark'].includes(newMode)) return
    mode.value = newMode

    const actual = newMode === 'system' ? getSystemPreference() : newMode
    applyTheme(actual)

    if (persist) {
      localStorage.setItem(THEME_STORAGE_KEY, newMode)
      debouncedPersist({ theme_mode: newMode })
    }
  }

  /** 切换主题（三态循环） */
  function toggle() {
    const order = ['system', 'light', 'dark']
    const idx = order.indexOf(mode.value)
    const next = order[(idx + 1) % 3]
    setMode(next)
  }

  /** 启用系统主题监听 */
  function startSystemListener() {
    if (!mediaQuery) {
      mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      mediaQuery.addEventListener('change', onSystemChange)
    }
  }

  /** 销毁系统主题监听 */
  function stopSystemListener() {
    if (mediaQuery) {
      mediaQuery.removeEventListener('change', onSystemChange)
      mediaQuery = null
    }
  }

  // 启动时从 localStorage 读取（API 返回前生效，避免闪烁）
  const saved = localStorage.getItem(THEME_STORAGE_KEY)
  if (saved && ['system', 'light', 'dark'].includes(saved)) {
    mode.value = saved
    const actual = saved === 'system' ? getSystemPreference() : saved
    applyTheme(actual)
  }

  startSystemListener()

  return {
    mode,
    resolved,
    loadFromData,
    setMode,
    toggle,
    startSystemListener,
    stopSystemListener
  }
})
