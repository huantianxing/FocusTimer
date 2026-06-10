<script setup>
/**
 * 今日概览 4 卡片
 * 总专注时长 | 完成任务数 | 最长连续专注 | 进行中任务
 */
import { computed, onMounted, ref } from 'vue'
import { getTodayStats } from '@/api'
import { formatHumanReadable } from '@/utils/timeFormat'

const stats = ref({
  total_seconds: 0,
  total_display: '0小时0分钟',
  task_count: 0,
  max_continuous_minutes: 0,
  current_task: null
})

async function load() {
  try {
    const res = await getTodayStats()
    if (res.code === 200 && res.data) {
      stats.value = res.data
    }
  } catch { /* ignore */ }
}

const cards = computed(() => [
  {
    title: '今日专注',
    value: stats.value.total_display,
    icon: '⏱️',
    color: 'var(--primary-color)'
  },
  {
    title: '完成任务',
    value: `${stats.value.task_count} 个`,
    icon: '✅',
    color: 'var(--success-color)'
  },
  {
    title: '最长连续',
    value: `${stats.value.max_continuous_minutes} 分钟`,
    icon: '🎯',
    color: 'var(--warning-color)'
  },
  {
    title: '进行中',
    value: stats.value.current_task || '休息中 ☕',
    icon: '▶️',
    color: stats.value.current_task ? 'var(--primary-color)' : 'var(--text-muted)'
  }
])

onMounted(load)
</script>

<template>
  <div class="overview-cards">
    <div
      v-for="card in cards"
      :key="card.title"
      class="overview-card card"
    >
      <div class="card-icon">{{ card.icon }}</div>
      <div class="card-info">
        <div class="card-title">{{ card.title }}</div>
        <div class="card-value" :style="{ color: card.color }">{{ card.value }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
}

.overview-card {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg) 20px;
  border-radius: var(--radius-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  min-width: 0;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.card-icon {
  font-size: 32px;
  line-height: 1;
  flex-shrink: 0;
}

.card-info {
  min-width: 0;
}

.card-title {
  font-size: var(--font-xs);
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}

.card-value {
  font-size: var(--font-lg);
  font-weight: 700;
  letter-spacing: -0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.3;
}

/* ==================== 响应式 ==================== */

@media (max-width: 1100px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  .card-icon {
    font-size: 24px;
  }
  .card-value {
    font-size: var(--font-md);
  }
}
</style>
