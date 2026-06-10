<script setup>
/**
 * 24 小时时段分布柱状图
 * X轴：0-23 小时，Y轴：专注分钟数
 */
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getTodayStats } from '@/api'
import { useThemeStore } from '@/stores/theme'
import { getChartTheme, getAxisConfig } from '@/utils/chartConfig'

const themeStore = useThemeStore()
const chartRef = ref(null)
let chart = null
let resizeObserver = null

async function load() {
  if (!chartRef.value) return
  try {
    const res = await getTodayStats()
    if (res.code !== 200 || !res.data?.hourly_data) return

    const hours = res.data.hourly_data.map(d => `${d.hour}时`)
    const minutes = res.data.hourly_data.map(d => d.minutes)
    const isDark = themeStore.resolved === 'dark'
    const axisConfig = getAxisConfig(themeStore.resolved)

    if (!chart) {
      chart = echarts.init(chartRef.value, isDark ? 'dark' : undefined)
    }

    chart.setOption({
      ...getChartTheme(themeStore.resolved),
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}分钟'
      },
      xAxis: {
        type: 'category',
        data: hours,
        ...axisConfig
      },
      yAxis: {
        type: 'value',
        name: '分钟',
        ...axisConfig
      },
      series: [{
        data: minutes,
        type: 'bar',
        itemStyle: {
          color: isDark ? '#4cc9f0' : '#409eff',
          borderRadius: [4, 4, 0, 0]
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
    <h4 class="chart-title">时段分布</h4>
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
  min-height: 200px;
  width: 100%;
}
</style>
