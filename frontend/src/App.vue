<script setup>
/**
 * 根组件 — 主布局
 * Header（固定顶部） + Body（RouterView）
 */
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useSoundStore } from '@/stores/sound'
import { useSettingsStore } from '@/stores/settings'
import AppHeader from '@/components/common/AppHeader.vue'

const themeStore = useThemeStore()
const soundStore = useSoundStore()
const settingsStore = useSettingsStore()

// 初始化：只调 1 次 GET /api/settings，然后分发给 theme/sound
onMounted(async () => {
  await settingsStore.load()
  // 从统一数据源分发，不再各自独立请求
  themeStore.loadFromData(settingsStore.settings)
  soundStore.loadFromData(settingsStore.settings)
})
</script>

<template>
  <div class="app-layout">
    <AppHeader />
    <div class="app-body">
      <router-view />
    </div>
  </div>
</template>
