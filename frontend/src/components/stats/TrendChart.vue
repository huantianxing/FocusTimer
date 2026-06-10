<script setup>
/**
 * 趋势折线图（日视图）
 * X轴：日期，Y轴：时长（分钟）
 * 支持切换 7天 / 30天 / 90天
 */
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getTrendStats } from '@/api'
import { useThemeStore } from '@/stores/theme'
import { getChartTheme, getAxisConfig } from '@/utils/chartConfig'

const themeStore = useThemeStore()
const chartRef = ref(null)
let chart = null

const days = ref(7)

async function load() {
  if (!chartRef.value) return
  try {
    const res = await getTrendStats(days.value)
    if (res.code !== 200 || !res.data?.trend) return

    const dates = res.data.trend.map(d => d.date)
    const minutes = res.data.trend.map(d => d.minutes)
    const isDark = themeStore.resolved === 'dark'
    const axisConfig = getAxisConfig(themeStore.resolved)

    if (!chart) {
      chart = echarts.init(chartRef.value, isDark ? 'dark' : undefined)
    }

    chart.setOption({
      ...getChartTheme(themeStore.resolved),
      tooltip: {
        trigger: 'axis',
        formatter: '{b}<br/>专注: {c}分钟'
      },
      xAxis: {
        type: 'category',
        data: dates,
        ...axisConfig
      },
      yAxis: {
        type: 'value',
        name: '分钟',
        ...axisConfig
      },
      series: [{
        data: minutes,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color: isDark ? '#4cc9f0' : '#409eff', width: 2 },
        itemStyle: { color: isDark ? '#4cc9f0' : '#409eff' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: isDark ? 'rgba(76,201,240,0.3)' : 'rgba(64,158,255,0.3)' },
            { offset: 1, color: 'rgba(0,0,0,0)' }
          ])
        }
      }]
    })
  } catch { /* ignore */ }
}

function handleResize() { chart?.resize() }

function changeDays(d) {
  days.value = d
  chart?.dispose()
  chart = null
  load()
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
    <div class="chart-header">
      <h4 class="chart-title">专注趋势</h4>
      <el-radio-group v-model="days" size="small" @change="changeDays">
        <el-radio-button :value="7">7天</el-radio-button>
        <el-radio-button :value="30">30天</el-radio-button>
        <el-radio-button :value="90">90天</el-radio-button>
      </el-radio-group>
    </div>
    <div ref="chartRef" class="chart-body" />
  </div>
</template>

<style scoped>
.chart-container {
  margin-bottom: 16px;
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.chart-title {
  font-size: 15px;
  color: var(--text-primary);
}
.chart-body {
  width: 100%;
  height: 280px;
}
</style>
