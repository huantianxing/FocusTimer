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
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.theme-radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.theme-option {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: border-color 0.3s;
}
.theme-option:hover {
  border-color: var(--primary-color);
}
.theme-radio {
  display: flex;
  align-items: center;
}
.option-label {
  font-size: 14px;
  font-weight: 500;
}
.option-desc {
  margin: 6px 0 0 24px;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
