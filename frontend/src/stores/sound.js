/**
 * 音效 Store
 *
 * 职责：
 * - 管理音效开关、音量
 * - 使用 Web Audio API 合成默认提示音
 * - 支持 HTML5 Audio 播放自定义音效文件
 * - 不再独立调 GET /api/settings，改由 App.vue 从 settingsStore 统一分发
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { updateSettings } from '@/api'

// 防抖：避免拖拽音量滑块时频繁 PUT
let debounceTimer = null
function debouncedPersist(data) {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    updateSettings(data).catch(() => {})
  }, 600)
}

export const useSoundStore = defineStore('sound', () => {
  // ========== State ==========
  const enabled = ref(true)
  const volume = ref(80)             // 0-100
  const customSoundPath = ref(null)

  let audioContext = null

  // ========== Internal ==========

  function getCtx() {
    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)()
    }
    return audioContext
  }

  function playBeep(frequency = 523, duration = 0.3, type = 'sine') {
    if (!enabled.value) return
    try {
      const ctx = getCtx()
      const oscillator = ctx.createOscillator()
      const gainNode = ctx.createGain()

      oscillator.type = type
      oscillator.frequency.value = frequency
      gainNode.gain.value = volume.value / 100 * 0.3

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      oscillator.start()
      gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration)
      oscillator.stop(ctx.currentTime + duration)
    } catch {
      // 静默失败
    }
  }

  // ========== Actions ==========

  /** 从 settingsStore 统一数据源加载（不再独立调 GET /api/settings） */
  function loadFromData(settingsData) {
    if (!settingsData) return
    enabled.value = settingsData.sound_enabled !== false
    volume.value = settingsData.sound_volume ?? 80
    customSoundPath.value = settingsData.custom_sound_path || null
  }

  /** 设置音效开关 */
  function setEnabled(val) {
    enabled.value = val
    debouncedPersist({ sound_enabled: val })
  }

  /** 设置音量（带防抖，拖拽滑块不会疯狂 PUT） */
  function setVolume(val) {
    volume.value = Math.max(0, Math.min(100, val))
    debouncedPersist({ sound_volume: volume.value })
  }

  /** 播放指定事件音效 */
  function play(eventType) {
    if (!enabled.value) return

    if (customSoundPath.value) {
      try {
        const audio = new Audio(customSoundPath.value)
        audio.volume = volume.value / 100
        audio.play()
        return
      } catch { /* fallback to beep */ }
    }

    switch (eventType) {
      case 'start':
        playBeep(523, 0.3, 'sine')
        break
      case 'pause':
        playBeep(330, 0.2, 'triangle')
        break
      case 'end':
        playBeep(659, 0.8, 'sine')
        setTimeout(() => playBeep(784, 0.4, 'sine'), 200)
        break
      case 'break_start':
        playBeep(440, 0.3, 'sine')
        setTimeout(() => playBeep(554, 0.3, 'sine'), 150)
        break
      case 'break_end':
        playBeep(554, 0.3, 'sine')
        setTimeout(() => playBeep(440, 0.3, 'sine'), 150)
        break
      case 'goal_achieved':
        playBeep(523, 0.2, 'sine')
        setTimeout(() => playBeep(659, 0.2, 'sine'), 200)
        setTimeout(() => playBeep(784, 0.5, 'sine'), 400)
        break
      default:
        playBeep(440, 0.2, 'sine')
    }
  }

  return {
    enabled,
    volume,
    customSoundPath,
    loadFromData,
    setEnabled,
    setVolume,
    play
  }
})
