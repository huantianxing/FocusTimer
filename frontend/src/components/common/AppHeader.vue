<script setup>
/**
 * 顶部导航栏
 * Logo + 应用名称 + 主导航 + 今日总时长 + 主题切换 + 音量控制
 */
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTimerStore } from '@/stores/timer'
import { useRecordsStore } from '@/stores/records'
import { formatHumanReadable } from '@/utils/timeFormat'
import ThemeToggle from './ThemeToggle.vue'
import SoundControl from './SoundControl.vue'

const router = useRouter()
const route = useRoute()
const timerStore = useTimerStore()
const recordsStore = useRecordsStore()

const navItems = [
  { path: '/', name: 'Home', label: '计时', icon: '⏱️' },
  { path: '/history', name: 'History', label: '历史', icon: '📋' },
  { path: '/stats', name: 'Stats', label: '统计', icon: '📊' },
  { path: '/tags', name: 'Tags', label: '标签', icon: '🏷️' },
  { path: '/settings', name: 'Settings', label: '设置', icon: '⚙️' }
]

const todayTotal = computed(() => {
  const records = recordsStore.todayRecords
  if (!Array.isArray(records)) return '0分钟'

  let total = 0
  records.forEach(group => {
    if (group.total_seconds) {
      total += group.total_seconds
    } else if (group.duration_seconds) {
      total += group.duration_seconds
    }
  })
  return formatHumanReadable(total)
})

const currentTitle = computed(() => {
  return timerStore.currentRecord?.title || ''
})

function goTo(path) {
  router.push(path)
}
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo-link">
        <span class="logo">⏱️</span>
        <span class="app-name">TimerFocus</span>
      </router-link>
    </div>

    <!-- 主导航 -->
    <nav class="header-nav">
      <router-link
        v-for="item in navItems"
        :key="item.name"
        :to="item.path"
        class="nav-item"
        :class="{ active: route.path === item.path }"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="header-center">
      <span v-if="currentTitle" class="current-task">
        {{ currentTitle }} — {{ todayTotal }} 今日
      </span>
      <span v-else class="today-total">
        今日专注 {{ todayTotal }}
      </span>
    </div>

    <div class="header-right">
      <SoundControl />
      <ThemeToggle />
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 60px;
  background-color: var(--bg-card);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  padding: 0 var(--space-lg);
  flex-shrink: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--shadow-sm);
  gap: 0;
}

/* ---- 左侧 Logo ---- */
.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.logo-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  color: inherit;
}
.logo {
  font-size: 26px;
  line-height: 1;
}
.app-name {
  font-size: var(--font-lg);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

/* ---- 主导航 ---- */
.header-nav {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  margin-left: var(--space-xl);
  flex-shrink: 0;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: var(--font-sm);
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
}
.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.nav-item.active {
  background: var(--primary-color);
  color: #FFFFFF;
}
.nav-icon {
  font-size: 14px;
  line-height: 1;
}
.nav-label {
  letter-spacing: -0.01em;
}

/* ---- 中间状态 ---- */
.header-center {
  flex: 1;
  text-align: center;
  min-width: 0;
}
.current-task {
  color: var(--primary-color);
  font-weight: 600;
  font-size: var(--font-sm);
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.today-total {
  color: var(--text-secondary);
  font-size: var(--font-sm);
  font-weight: 500;
}

/* ---- 右侧工具 ---- */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  flex-shrink: 0;
}

/* ---- 响应式 ---- */
@media (max-width: 900px) {
  .header-nav {
    display: none;
  }
  .header-center {
    display: none;
  }
}
@media (max-width: 640px) {
  .app-header {
    padding: 0 var(--space-md);
  }
  .app-name {
    display: none;
  }
}
</style>
