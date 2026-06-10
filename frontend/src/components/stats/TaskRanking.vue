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
      grid: { left: '3%', right: '10%', bottom: '3%', containLabel: true },
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

function handleResize() { chart?.resize() }

watch(() => themeStore.resolved, () => {
  chart?.dispose()
  chart = null
  load()
})

onMounted(() => {
  load()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
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
  margin-bottom: 16px;
}
.chart-title {
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 12px;
}
.chart-body {
  width: 100%;
  height: 320px;
}
</style>
