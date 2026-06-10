<script setup>
/**
 * 大字体计时器显示
 * 72px, monospace, font-weight: 200
 * 实时显示 HH:MM:SS
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
  padding: 40px 20px;
  transition: color 0.3s ease;
}
.timer-time {
  font-size: 72px;
  font-weight: 200;
  font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  letter-spacing: 4px;
  line-height: 1.2;
  color: var(--text-primary);
}
.timer-active .timer-time {
  color: var(--primary-color);
}
.timer-paused .timer-time {
  color: var(--warning-color);
}
.timer-title {
  margin-top: 12px;
  font-size: 20px;
  color: var(--text-primary);
  font-weight: 500;
}
.timer-placeholder {
  margin-top: 12px;
  font-size: 16px;
  color: var(--text-muted);
}
</style>
