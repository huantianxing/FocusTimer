<script setup>
/**
 * 统计分析页
 * 趋势折线图 + 任务排行榜 + 效率指标
 */
import TrendChart from '@/components/stats/TrendChart.vue'
import TaskRanking from '@/components/stats/TaskRanking.vue'
</script>

<template>
  <div class="stats-view">
    <h2>统计分析</h2>

    <div class="stats-grid">
      <div class="stats-main">
        <TrendChart />
      </div>
      <div class="stats-side">
        <TaskRanking />
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-view {
  padding: 24px;
  overflow-y: auto;
  height: 100%;
}
.stats-view h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 16px;
}
.stats-main, .stats-side {
  min-height: 400px;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
