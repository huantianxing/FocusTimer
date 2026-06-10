/**
 * 时间格式化工具
 * 后端返回的 duration_seconds (秒) 转为前端展示格式
 */

/**
 * 秒数 → HH:MM:SS 显示格式
 * @param {number} seconds - 总秒数
 * @returns {string} 格式化的时间字符串
 */
export function formatHHMMSS(seconds) {
  if (!seconds || seconds < 0) return '00:00:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return [h, m, s].map(v => String(v).padStart(2, '0')).join(':')
}

/**
 * 秒数 → "X小时X分钟" 人性化显示
 * @param {number} seconds - 总秒数
 * @returns {string}
 */
export function formatHumanReadable(seconds) {
  if (!seconds || seconds <= 0) return '0分钟'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  if (h > 0 && m > 0) return `${h}小时${m}分钟`
  if (h > 0) return `${h}小时`
  return `${m}分钟`
}

/**
 * 秒数 → "Xh Ym" 紧凑格式（用于侧边栏等空间有限场景）
 * @param {number} seconds
 * @returns {string}
 */
export function formatCompact(seconds) {
  if (!seconds || seconds <= 0) return '0m'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  if (h > 0 && m > 0) return `${h}h ${m}m`
  if (h > 0) return `${h}h`
  return `${m}m`
}

/**
 * ISO 时间字符串 → "HH:mm:ss" 时间部分
 * @param {string} isoStr
 * @returns {string}
 */
export function formatTimeOnly(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return [d.getHours(), d.getMinutes(), d.getSeconds()]
    .map(v => String(v).padStart(2, '0'))
    .join(':')
}

/**
 * ISO 时间字符串 → "MM/DD HH:mm" 日期+时间
 * @param {string} isoStr
 * @returns {string}
 */
export function formatDateTime(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const time = [d.getHours(), d.getMinutes()].map(v => String(v).padStart(2, '0')).join(':')
  return `${m}/${day} ${time}`
}

/**
 * 获取今天日期字符串 YYYY-MM-DD
 */
export function getTodayStr() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

/**
 * 获取 N 天前的日期字符串
 */
export function getDateStrDaysAgo(days) {
  const d = new Date()
  d.setDate(d.getDate() - days)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}
