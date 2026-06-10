<script setup>
/**
 * 统计分析页
 * 趋势折线图 + 任务排行榜
 */
import { useRouter } from 'vue-router'
import TrendChart from '@/components/stats/TrendChart.vue'
import TaskRanking from '@/components/stats/TaskRanking.vue'

const router = useRouter()

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="stats-view">
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="'ArrowLeft'" text @click="goHome">返回</el-button>
        <h2>统计分析</h2>
      </div>
    </div>

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
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  padding: var(--space-xl);
  overflow: hidden;
  animation: fadeInUp var(--transition-slow) ease forwards;
}

.page-header {
  flex-shrink: 0;
  margin-bottom: var(--space-lg);
}
.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}
.header-left h2 {
  font-size: var(--font-xl);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin: 0;
}

.stats-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr minmax(320px, 380px);
  gap: var(--space-lg);
  overflow: hidden;
}

.stats-main {
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
}

.stats-side {
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
}

/* ==================== 响应式 ==================== */

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .stats-side {
    max-height: 420px;
  }
}

@media (max-width: 768px) {
  .stats-view {
    padding: var(--space-md);
  }
}

@media (max-width: 480px) {
  .stats-view {
    padding: var(--space-sm);
  }
}
</style>
