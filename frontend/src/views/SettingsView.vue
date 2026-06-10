<script setup>
/**
 * 设置页 — 使用 el-tabs 分组展示
 */
import { onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useThemeStore } from '@/stores/theme'
import { useSoundStore } from '@/stores/sound'
import ThemeSettings from '@/components/settings/ThemeSettings.vue'
import SoundSettings from '@/components/settings/SoundSettings.vue'
import TimerSettings from '@/components/settings/TimerSettings.vue'
import HotkeySettings from '@/components/settings/HotkeySettings.vue'
import DataSettings from '@/components/settings/DataSettings.vue'

const settingsStore = useSettingsStore()
const themeStore = useThemeStore()
const soundStore = useSoundStore()

onMounted(async () => {
  await settingsStore.load()
  // 从统一数据源分发
  themeStore.loadFromData(settingsStore.settings)
  soundStore.loadFromData(settingsStore.settings)
})
</script>

<template>
  <div class="settings-view">
    <h2>设置</h2>

    <el-tabs tab-position="left" class="settings-tabs">
      <el-tab-pane label="外观">
        <ThemeSettings />
      </el-tab-pane>
      <el-tab-pane label="计时">
        <TimerSettings />
      </el-tab-pane>
      <el-tab-pane label="音效">
        <SoundSettings />
      </el-tab-pane>
      <el-tab-pane label="快捷键">
        <HotkeySettings />
      </el-tab-pane>
      <el-tab-pane label="数据 & 关于">
        <DataSettings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.settings-view {
  padding: 24px;
  overflow-y: auto;
  height: 100%;
}
.settings-view h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.settings-tabs {
  min-height: 500px;
}
</style>
