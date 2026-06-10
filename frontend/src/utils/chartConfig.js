/**
 * ECharts 图表主题配置
 * 根据当前主题模式（light/dark）返回对应的图表样式
 */

/**
 * 获取当前主题模式下的 ECharts 主题配置
 * @param {'light'|'dark'} mode
 * @returns {object} ECharts option 公共配置
 */
export function getChartTheme(mode) {
  const isDark = mode === 'dark'

  return {
    textStyle: {
      color: isDark ? '#a0a0a0' : '#606266'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    }
  }
}

/**
 * 获取坐标轴通用配置
 */
export function getAxisConfig(mode) {
  const isDark = mode === 'dark'
  return {
    axisLine: {
      lineStyle: { color: isDark ? '#2a2a4a' : '#dcdfe6' }
    },
    axisTick: {
      lineStyle: { color: isDark ? '#2a2a4a' : '#dcdfe6' }
    },
    axisLabel: {
      color: isDark ? '#a0a0a0' : '#606266'
    },
    splitLine: {
      lineStyle: { color: isDark ? '#2a2a4a' : '#ebeef5' }
    }
  }
}

/**
 * 返回 ECharts 内置主题名称（Element Plus 兼容的）
 */
export function getEChartsThemeName(mode) {
  return mode === 'dark' ? 'dark' : undefined
}
