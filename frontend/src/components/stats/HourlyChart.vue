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

function handleResize() {
  chart?.resize()
}

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
    <h4 class="chart-title">时段分布</h4>
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
  height: 240px;
}
</style>
