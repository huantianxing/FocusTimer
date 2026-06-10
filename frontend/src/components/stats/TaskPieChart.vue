<script setup>
/**
 * 任务占比饼图 / 环形图
 * Top5 + "其他"
 */
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getTodayStats } from '@/api'
import { useThemeStore } from '@/stores/theme'
import { getChartTheme } from '@/utils/chartConfig'

const themeStore = useThemeStore()
const chartRef = ref(null)
let chart = null

const COLORS = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']

async function load() {
  if (!chartRef.value) return
  try {
    const res = await getTodayStats()
    if (res.code !== 200 || !res.data?.pie_data?.length) return

    const pieData = res.data.pie_data.map((d, i) => ({
      name: d.name,
      value: d.value,
      itemStyle: { color: COLORS[i % COLORS.length] }
    }))
    const isDark = themeStore.resolved === 'dark'

    if (!chart) {
      chart = echarts.init(chartRef.value, isDark ? 'dark' : undefined)
    }

    chart.setOption({
      ...getChartTheme(themeStore.resolved),
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}分钟 ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          color: isDark ? '#a0a0a0' : '#606266'
        }
      },
      series: [{
        type: 'pie',
        radius: ['45%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        label: { show: false },
        emphasis: {
          label: { show: true, fontSize: 16, fontWeight: 'bold' }
        },
        data: pieData
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
    <h4 class="chart-title">任务占比</h4>
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
