/**
 * 用户设置 Store
 *
 * 职责：
 * - 缓存全部用户设置（从 /api/settings 加载）
 * - 提供更新任意配置项的 action
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSettings, updateSettings } from '@/api'

export const useSettingsStore = defineStore('settings', () => {
  // ========== State ==========
  const settings = ref({
    theme_mode: 'system',
    sound_enabled: true,
    sound_volume: 80,
    custom_sound_path: null,
    pomodoro_work_minutes: 25,
    pomodoro_short_break: 5,
    pomodoro_long_break: 15,
    pomodoro_cycles: 4,
    auto_backup_enabled: true,
    backup_path: '',
    global_hotkey_start: 'Ctrl+Alt+S',
    global_hotkey_end: 'Ctrl+Alt+E'
  })

  const loading = ref(false)

  // ========== Actions ==========

  /** 从 API 加载全部设置 */
  async function load() {
    loading.value = true
    try {
      const res = await getSettings()
      if (res.code === 200 && res.data) {
        settings.value = { ...settings.value, ...res.data }
      }
    } catch {
      // 使用默认值
    } finally {
      loading.value = false
    }
  }

  /** 更新部分设置 */
  async function save(partial) {
    try {
      const res = await updateSettings(partial)
      if (res.code === 200) {
        // 合并更新
        settings.value = { ...settings.value, ...partial }
      }
      return res
    } catch {
      return null
    }
  }

  return {
    settings,
    loading,
    load,
    save
  }
})
