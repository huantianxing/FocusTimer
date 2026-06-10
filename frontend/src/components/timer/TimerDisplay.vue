<script setup>
/**
 * 大字体计时器显示
 * 使用 clamp() 自适应，桌面 ~60px，小屏 ~36px
 */
import { computed } from 'vue'
import { useTimerStore } from '@/stores/timer'
import { formatHHMMSS } from '@/utils/timeFormat'

const timerStore = useTimerStore()

const displayTime = computed(() => {
  return formatHHMMSS(timerStore.elapsedSeconds)
})

const isActive = computed(() => timerStore.hasActiveTimer)
const statusClass = computed(() => ({
  'timer-active': timerStore.isRunning,
  'timer-paused': timerStore.hasActiveTimer && !timerStore.isRunning,
  'timer-idle': !timerStore.hasActiveTimer
}))
</script>

<template>
  <div class="timer-display" :class="statusClass">
    <div class="timer-time">{{ displayTime }}</div>
    <div v-if="timerStore.currentRecord" class="timer-title">
      {{ timerStore.currentRecord.title }}
    </div>
    <div v-else class="timer-placeholder">
      点击下方按钮开始专注
    </div>
  </div>
</template>

<style scoped>
.timer-display {
  text-align: center;
  padding: var(--space-md) var(--space-lg);
  transition: color var(--transition-base);
}

.timer-time {
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 300;
  font-family: 'Plus Jakarta Sans', 'SF Mono', 'Fira Code', 'Consolas', monospace;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  transition: all var(--transition-base);
  word-break: keep-all;
}

.timer-active .timer-time {
  color: var(--primary-color);
  text-shadow: 0 0 40px var(--primary-glow);
}

.timer-paused .timer-time {
  color: var(--warning-color);
  text-shadow: 0 0 24px rgba(234, 88, 12, 0.15);
}

.timer-title {
  margin-top: var(--space-sm);
  font-size: var(--font-lg);
  color: var(--text-primary);
  font-weight: 600;
  letter-spacing: -0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.timer-placeholder {
  margin-top: var(--space-sm);
  font-size: var(--font-sm);
  color: var(--text-muted);
  font-weight: 400;
}
</style>
