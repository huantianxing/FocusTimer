<script setup>
/**
 * 顶部导航栏
 * Logo + 应用名称 + 今日总时长 + 主题切换 + 音量控制 + 设置入口
 */
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTimerStore } from '@/stores/timer'
import { useRecordsStore } from '@/stores/records'
import { formatHumanReadable } from '@/utils/timeFormat'
import ThemeToggle from './ThemeToggle.vue'
import SoundControl from './SoundControl.vue'

const router = useRouter()
const timerStore = useTimerStore()
const recordsStore = useRecordsStore()

const todayTotal = computed(() => {
  const records = recordsStore.todayRecords
  if (!Array.isArray(records)) return '0分钟'

  // records 可能是分组结构 [{ title, records: [...], total_seconds }]
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

function goSettings() {
  router.push('/settings')
}
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <span class="logo">⏱️</span>
      <span class="app-name">TimerFocus</span>
    </div>

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
      <el-button
        class="settings-btn"
        :icon="'Setting'"
        text
        @click="goSettings"
      >
        设置
      </el-button>
    </div>
  </header>
</template>

<style scoped>
.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.logo { font-size: 24px; }
.app-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}
.header-center {
  flex: 1;
  text-align: center;
}
.current-task {
  color: var(--primary-color);
  font-weight: 500;
}
.today-total {
  color: var(--text-secondary);
  font-size: 14px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.settings-btn {
  color: var(--text-secondary);
}
</style>
