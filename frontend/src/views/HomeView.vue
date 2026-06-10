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
  // refresh() 只查一次当前状态：有进行中任务才自动开始轮询，没任务不浪费请求
  timerStore.refresh()
  recordsStore.fetchTodayRecords()
})

onUnmounted(() => {
  timerStore.stopPolling()
})
</script>

<template>
  <div class="home-view">
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
      <el-row :gutter="16">
        <el-col :span="12">
          <HourlyChart />
        </el-col>
        <el-col :span="12">
          <TaskPieChart />
        </el-col>
      </el-row>
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
  gap: 0;
}
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
.timer-panel {
  margin-bottom: 24px;
  text-align: center;
}
.sidebar {
  width: 320px;
  border-left: 1px solid var(--border-color);
  background-color: var(--bg-card);
  overflow-y: auto;
  flex-shrink: 0;
}
</style>
