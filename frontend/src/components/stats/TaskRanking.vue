<script setup>
/**
 * 任务排行榜 — 横向条形图 Top N
 */
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getTaskRanking } from '@/api'
import { useThemeStore } from '@/stores/theme'
import { getChartTheme, getAxisConfig } from '@/utils/chartConfig'

const themeStore = useThemeStore()
const chartRef = ref(null)
let chart = null
let resizeObserver = null

async function load() {
  if (!chartRef.value) return
  try {
    const res = await getTaskRanking({ limit: 10 })
    if (res.code !== 200 || !Array.isArray(res.data) || !res.data.length) return

    // 横向条形图：反转数据使最长排在最上
    const data = [...res.data].reverse()
    const names = data.map(d => d.title)
    const minutes = data.map(d => Math.round(d.total_seconds / 60))
    const isDark = themeStore.resolved === 'dark'
    const axisConfig = getAxisConfig(themeStore.resolved)

    if (!chart) {
      chart = echarts.init(chartRef.value, isDark ? 'dark' : undefined)
    }

    chart.setOption({
      ...getChartTheme(themeStore.resolved),
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: (params) => {
          const p = params[0]
          const item = data[data.length - 1 - p.dataIndex]
          return `${p.name}<br/>${item?.display_time || p.value + '分钟'} (${item?.percentage || 0}%)`
        }
      },
      grid: { left: '3%', right: '10%', bottom: '3%', top: 0, containLabel: true },
      xAxis: {
        type: 'value',
        name: '分钟',
        ...axisConfig
      },
      yAxis: {
        type: 'category',
        data: names,
        axisLabel: { width: 100, overflow: 'truncate' },
        ...axisConfig
      },
      series: [{
        data: minutes,
        type: 'bar',
        itemStyle: {
          color: isDark ? '#4cc9f0' : '#409eff',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}分',
          color: isDark ? '#a0a0a0' : '#606266'
        }
      }]
    })
  } catch { /* ignore */ }
}

watch(() => themeStore.resolved, () => {
  chart?.dispose()
  chart = null
  load()
})

onMounted(() => {
  load()
  if (chartRef.value) {
    resizeObserver = new ResizeObserver(() => {
      chart?.resize()
    })
    resizeObserver.observe(chartRef.value)
  }
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  chart?.dispose()
})
</script>

<template>
  <div class="chart-container card">
    <h4 class="chart-title">任务排行 Top 10</h4>
    <div ref="chartRef" class="chart-body" />
  </div>
</template>

<style scoped>
.chart-container {
  margin-bottom: var(--space-md);
  border-radius: var(--radius-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
  padding: var(--space-lg);
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
  height: 100%;
}
.chart-container:hover {
  box-shadow: var(--shadow-md);
}
.chart-title {
  font-size: var(--font-md);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: var(--space-md);
  flex-shrink: 0;
}
.chart-body {
  flex: 1;
  min-height: 240px;
  width: 100%;
}
</style>
