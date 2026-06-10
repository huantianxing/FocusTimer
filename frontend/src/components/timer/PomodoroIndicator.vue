<script setup>
/**
 * 番茄钟进度指示器 — 4 个圆点表示第几个番茄
 * 预留组件，番茄钟功能 Phase 5 启用
 */
import { computed } from 'vue'
import { useTimerStore } from '@/stores/timer'
import { useSettingsStore } from '@/stores/settings'

const timerStore = useTimerStore()
const settingsStore = useSettingsStore()

const totalCycles = computed(() => settingsStore.settings.pomodoro_cycles || 4)
const currentCount = computed(() => timerStore.currentRecord?.pomodoro_count || 0)

const isPomodoro = computed(() => timerStore.currentRecord?.is_pomodoro === 1)
</script>

<template>
  <div v-if="isPomodoro" class="pomodoro-indicator">
    <div class="cycle-dots">
      <span
        v-for="i in totalCycles"
        :key="i"
        class="dot"
        :class="{ active: i <= currentCount, current: i === currentCount + 1 && timerStore.hasActiveTimer }"
      />
    </div>
    <span class="cycle-label">
      番茄 {{ currentCount }} / {{ totalCycles }}
    </span>
  </div>
</template>

<style scoped>
.pomodoro-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}
.cycle-dots {
  display: flex;
  gap: 8px;
}
.dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--border-color);
  transition: background 0.3s ease;
}
.dot.active {
  background: var(--success-color);
}
.dot.current {
  background: var(--primary-color);
  box-shadow: 0 0 6px var(--primary-color);
}
.cycle-label {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
