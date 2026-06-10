<script setup>
/**
 * 设置页 — 使用 el-tabs 左栏分组展示
 * 包含返回首页按钮
 */
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '@/stores/settings'
import { useThemeStore } from '@/stores/theme'
import { useSoundStore } from '@/stores/sound'
import ThemeSettings from '@/components/settings/ThemeSettings.vue'
import SoundSettings from '@/components/settings/SoundSettings.vue'
import TimerSettings from '@/components/settings/TimerSettings.vue'
import HotkeySettings from '@/components/settings/HotkeySettings.vue'
import DataSettings from '@/components/settings/DataSettings.vue'

const router = useRouter()
const settingsStore = useSettingsStore()
const themeStore = useThemeStore()
const soundStore = useSoundStore()

onMounted(async () => {
  await settingsStore.load()
  themeStore.loadFromData(settingsStore.settings)
  soundStore.loadFromData(settingsStore.settings)
})

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="settings-view">
    <div class="settings-header">
      <el-button :icon="'ArrowLeft'" @click="goHome">返回首页</el-button>
      <h2>设置</h2>
    </div>

    <div class="settings-body">
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
  </div>
</template>

<style scoped>
.settings-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: var(--space-xl);
  overflow: hidden;
  animation: fadeInUp var(--transition-slow) ease forwards;
}

.settings-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
  flex-shrink: 0;
}

.settings-header h2 {
  font-size: var(--font-xl);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin: 0;
}

.settings-body {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.settings-tabs {
  height: 100%;
}

.settings-tabs :deep(.el-tabs__header) {
  flex-shrink: 0;
}

.settings-tabs :deep(.el-tabs__content) {
  padding: var(--space-lg);
  background: var(--bg-card);
  border-radius: 0 var(--radius-lg) var(--radius-lg) var(--radius-lg);
  border: 1px solid var(--border-subtle);
  border-left: none;
  height: 100%;
  overflow-y: auto;
}

/* ==================== 响应式 ==================== */

@media (max-width: 768px) {
  .settings-view {
    padding: var(--space-md);
    max-width: 100%;
  }

  /* 左栏 tabs → 顶部 tabs */
  .settings-tabs :deep(.el-tabs__header) {
    width: 100%;
  }
  .settings-tabs :deep(.el-tabs__content) {
    border-radius: 0 0 var(--radius-lg) var(--radius-lg);
    border-left: 1px solid var(--border-subtle);
    border-top: none;
    height: auto;
    min-height: 360px;
    padding: var(--space-md);
  }

  .settings-header {
    margin-bottom: var(--space-md);
  }
}

@media (max-width: 480px) {
  .settings-view {
    padding: var(--space-sm);
  }
  .settings-tabs :deep(.el-tabs__content) {
    padding: var(--space-sm);
  }
  .settings-header h2 {
    font-size: var(--font-lg);
  }
}
</style>
