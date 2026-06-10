/**
 * ECharts 图表主题配置
 * 设计系统: UI-UX-Pro-Max — Exaggerated Minimalism
 * 根据当前主题模式（light/dark）返回对应的图表样式
 */

// 浅色模式图表配色
const LIGHT_COLORS = ['#0D9488', '#EA580C', '#6366F1', '#059669', '#F59E0B', '#DC2626', '#8B5CF6', '#14B8A6', '#EC4899', '#0EA5E9']

// 深色模式图表配色
const DARK_COLORS = ['#DC2626', '#059669', '#F59E0B', '#6366F1', '#14B8A6', '#EC4899', '#3B82F6', '#EF4444', '#10B981', '#818CF8']

/**
 * 获取当前主题模式下的 ECharts 主题配置
 * @param {'light'|'dark'} mode
 * @returns {object} ECharts option 公共配置
 */
export function getChartTheme(mode) {
  const isDark = mode === 'dark'

  return {
    backgroundColor: 'transparent',
    textStyle: {
      color: isDark ? '#94A3B8' : '#5B8C87',
      fontFamily: "'Plus Jakarta Sans', sans-serif"
    },
    grid: {
      left: '3%',
      right: '4%',
      top: 12,
      bottom: '3%',
      containLabel: true
    },
    color: isDark ? DARK_COLORS : LIGHT_COLORS
  }
}

/**
 * 获取坐标轴通用配置
 */
export function getAxisConfig(mode) {
  const isDark = mode === 'dark'
  return {
    axisLine: {
      lineStyle: { color: isDark ? 'rgba(255,255,255,0.08)' : '#99F6E4' }
    },
    axisTick: {
      lineStyle: { color: isDark ? 'rgba(255,255,255,0.08)' : '#99F6E4' }
    },
    axisLabel: {
      color: isDark ? '#94A3B8' : '#5B8C87',
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(153,246,228,0.4)',
        type: 'dashed'
      }
    }
  }
}
