<script setup>
/**
 * 计时控制按钮组
 * 根据当前状态动态显示:
 * - 空闲 → [开始]
 * - 计时中 → [暂停] [结束]
 * - 已暂停 → [继续] [结束]
 */
import { ref, computed } from 'vue'
import { useTimerStore } from '@/stores/timer'
import { useSoundStore } from '@/stores/sound'
import { useRecordsStore } from '@/stores/records'
import TaskModal from './TaskModal.vue'

const emit = defineEmits(['started', 'stopped'])

const timerStore = useTimerStore()
const soundStore = useSoundStore()
const recordsStore = useRecordsStore()

const showTaskModal = ref(false)
const loading = ref(false)

const canStart = computed(() => !timerStore.hasActiveTimer)
const canPause = computed(() => timerStore.hasActiveTimer && timerStore.isRunning)
const canResume = computed(() => timerStore.hasActiveTimer && !timerStore.isRunning)
const canEnd = computed(() => timerStore.hasActiveTimer)

async function handlePause() {
  loading.value = true
  try {
    await timerStore.pause()
    soundStore.play('pause')
  } finally {
    loading.value = false
  }
}

async function handleResume() {
  loading.value = true
  try {
    await timerStore.resume()
    soundStore.play('start')
  } finally {
    loading.value = false
  }
}

async function handleEnd() {
  loading.value = true
  try {
    await timerStore.end()
    soundStore.play('end')
    recordsStore.fetchTodayRecords()
    emit('stopped')
  } finally {
    loading.value = false
  }
}

function onTaskModalStarted() {
  recordsStore.fetchTodayRecords()
  emit('started')
}
</script>

<template>
  <div class="timer-controls">
    <!-- 开始按钮（空闲状态） -->
    <el-button
      v-if="canStart"
      type="primary"
      size="large"
      round
      :icon="'VideoPlay'"
      @click="showTaskModal = true"
    >
      开始计时
    </el-button>

    <!-- 暂停按钮（进行中） -->
    <el-button
      v-if="canPause"
      type="warning"
      size="large"
      round
      :icon="'VideoPause'"
      :loading="loading"
      @click="handlePause"
    >
      暂停
    </el-button>

    <!-- 继续按钮（已暂停） -->
    <el-button
      v-if="canResume"
      type="success"
      size="large"
      round
      :icon="'VideoPlay'"
      :loading="loading"
      @click="handleResume"
    >
      继续
    </el-button>

    <!-- 结束按钮（进行中或已暂停） -->
    <el-button
      v-if="canEnd"
      type="danger"
      size="large"
      round
      :icon="'SwitchButton'"
      :loading="loading"
      @click="handleEnd"
    >
      结束
    </el-button>

    <!-- 任务弹窗 -->
    <TaskModal
      :visible="showTaskModal"
      @update:visible="showTaskModal = $event"
      @started="onTaskModalStarted"
    />
  </div>
</template>

<style scoped>
.timer-controls {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--space-md);
  margin: var(--space-md) 0 var(--space-lg);
}
:deep(.el-button--large) {
  min-width: 130px;
  height: 52px;
  font-size: var(--font-md);
  font-weight: 600;
  border-radius: var(--radius-md);
  letter-spacing: -0.01em;
  transition: all var(--transition-base);
}
:deep(.el-button--large:hover) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
:deep(.el-button--primary.el-button--large) {
  background: var(--primary-color);
  border-color: var(--primary-color);
  box-shadow: 0 4px 16px var(--primary-glow);
}

@media (max-width: 480px) {
  .timer-controls {
    gap: var(--space-sm);
  }
  :deep(.el-button--large) {
    min-width: 100px;
    height: 44px;
    font-size: var(--font-sm);
  }
}
</style>
