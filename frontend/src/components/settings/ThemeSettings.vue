<script setup>
/**
 * 外观设置：主题模式选择
 * 三选一：跟随系统 / 浅色 / 深色
 */
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const currentMode = computed({
  get: () => themeStore.mode,
  set: (val) => themeStore.setMode(val)
})

const options = [
  { value: 'system', label: '🖥️ 跟随系统', desc: '自动根据系统设置切换浅色/深色模式' },
  { value: 'light', label: '☀️ 浅色模式', desc: '始终使用浅色主题' },
  { value: 'dark', label: '🌙 深色模式', desc: '始终使用深色主题，护眼适合夜间使用' }
]
</script>

<template>
  <div class="theme-settings">
    <h4>外观设置</h4>
    <el-radio-group v-model="currentMode" class="theme-radio-group">
      <div
        v-for="opt in options"
        :key="opt.value"
        class="theme-option"
      >
        <el-radio :value="opt.value" class="theme-radio">
          <span class="option-label">{{ opt.label }}</span>
        </el-radio>
        <p class="option-desc">{{ opt.desc }}</p>
      </div>
    </el-radio-group>
  </div>
</template>

<style scoped>
.theme-settings h4 {
  font-size: var(--font-md);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: var(--space-lg);
}
.theme-radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
.theme-option {
  padding: var(--space-md);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  background: var(--bg-elevated);
}
.theme-option:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-sm);
}
.theme-radio {
  display: flex;
  align-items: center;
}
.option-label {
  font-size: var(--font-base);
  font-weight: 600;
  letter-spacing: -0.01em;
}
.option-desc {
  margin: 6px 0 0 24px;
  font-size: var(--font-xs);
  color: var(--text-muted);
  line-height: 1.5;
}
</style>
