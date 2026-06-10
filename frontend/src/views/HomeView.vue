<script setup>
/**
 * 首页
 * 计时控制面板 + 今日概览卡片 + 图表区域 + 记录列表（侧边栏）
 */
import { onMounted, onUnmounted } from 'vue'
import { useTimerStore } from '@/stores/timer'
import { useRecordsStore } from '@/stores/records'
import TimerDisplay from '@/components/timer/TimerDisplay.vue'
import TimerControls from '@/components/timer/TimerControls.vue'
import PomodoroIndicator from '@/components/timer/PomodoroIndicator.vue'
import TodayOverview from '@/components/stats/TodayOverview.vue'
import HourlyChart from '@/components/stats/HourlyChart.vue'
import TaskPieChart from '@/components/stats/TaskPieChart.vue'
import RecordList from '@/components/records/RecordList.vue'

const timerStore = useTimerStore()
const recordsStore = useRecordsStore()

onMounted(() => {
  timerStore.refresh()
  recordsStore.fetchTodayRecords()
})

onUnmounted(() => {
  timerStore.stopPolling()
})
</script>

<template>
  <div class="home-view">
    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 计时面板 -->
      <div class="timer-panel card">
        <TimerDisplay />
        <PomodoroIndicator />
        <TimerControls @started="recordsStore.fetchTodayRecords()" @stopped="recordsStore.fetchTodayRecords()" />
      </div>

      <!-- 今日概览 -->
      <TodayOverview />

      <!-- 图表区域 -->
      <div class="charts-row">
        <div class="chart-col">
          <HourlyChart />
        </div>
        <div class="chart-col">
          <TaskPieChart />
        </div>
      </div>
    </div>

    <!-- 侧边栏：今日记录 -->
    <aside class="sidebar">
      <RecordList />
    </aside>
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  height: 100%;
  width: 100%;
  gap: 0;
  background-color: var(--bg-primary);
}

/* ---- 主内容区 ---- */
.main-content {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.timer-panel {
  text-align: center;
  border-radius: var(--radius-xl);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-lg);
  padding: var(--space-2xl) var(--space-xl) var(--space-xl);
  position: relative;
  overflow: hidden;
  max-width: 800px;
  width: 100%;
  align-self: center;
}

.timer-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light), var(--success-color));
}

/* ---- 图表行 ---- */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.chart-col {
  min-width: 0;
}

/* ---- 侧边栏 ---- */
.sidebar {
  width: clamp(280px, 26%, 380px);
  border-left: 1px solid var(--border-subtle);
  background-color: var(--bg-card);
  overflow-y: auto;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

/* ==================== 响应式 ==================== */

/* 平板及以下：图表堆叠，侧边栏变窄 */
@media (max-width: 1100px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
  .sidebar {
    width: 260px;
  }
}

/* 小平板：侧边栏隐藏在底部（可选折叠）或保留右侧 */
@media (max-width: 860px) {
  .home-view {
    flex-direction: column;
  }
  .main-content {
    padding: var(--space-md);
  }
  .sidebar {
    width: 100%;
    max-height: 40vh;
    border-left: none;
    border-top: 1px solid var(--border-subtle);
  }
}

/* 手机 */
@media (max-width: 640px) {
  .main-content {
    padding: var(--space-sm);
    gap: var(--space-md);
  }
  .timer-panel {
    padding: var(--space-lg) var(--space-md);
  }
}
</style>
