<script setup>
/**
 * 主题切换按钮 — 三态循环: system → light → dark
 * 图标: 🖥️ 跟随系统 / ☀️ 浅色 / 🌙 深色
 */
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const icon = computed(() => {
  switch (themeStore.mode) {
    case 'system': return '🖥️'
    case 'light': return '☀️'
    case 'dark': return '🌙'
    default: return '🖥️'
  }
})

const label = computed(() => {
  switch (themeStore.mode) {
    case 'system': return '跟随系统'
    case 'light': return '浅色模式'
    case 'dark': return '深色模式'
    default: return ''
  }
})

function handleToggle() {
  themeStore.toggle()
}
</script>

<template>
  <el-tooltip :content="label" placement="bottom">
    <el-button class="theme-toggle-btn" text @click="handleToggle">
      {{ icon }}
    </el-button>
  </el-tooltip>
</template>

<style scoped>
.theme-toggle-btn {
  font-size: 18px;
  padding: 6px 10px;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}
.theme-toggle-btn:hover {
  background: var(--bg-hover);
}
</style>
