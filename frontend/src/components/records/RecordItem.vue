<script setup>
/**
 * 单条记录行
 * 显示：时间范围 | 时长 | 状态 | 操作按钮
 */
import { computed } from 'vue'
import { formatTimeOnly, formatCompact } from '@/utils/timeFormat'

const props = defineProps({
  record: { type: Object, required: true }
})
const emit = defineEmits(['edit'])

const statusMap = {
  0: { text: '进行中', type: 'primary' },
  1: { text: '已完成', type: 'success' },
  2: { text: '已暂停', type: 'warning' },
  3: { text: '已中断', type: 'info' },
  4: { text: '无效', type: 'danger' }
}

const statusInfo = computed(() => statusMap[props.record.status] || statusMap[1])

const timeRange = computed(() => {
  const start = formatTimeOnly(props.record.start_time)
  const end = props.record.end_time ? formatTimeOnly(props.record.end_time) : '进行中'
  return `${start} - ${end}`
})

const duration = computed(() => formatCompact(props.record.duration_seconds || 0))

const canEdit = computed(() => [1, 3].includes(props.record.status)) // 已完成或已中断才可编辑
</script>

<template>
  <div class="record-item">
    <div class="item-time">{{ timeRange }}</div>
    <div class="item-duration">{{ duration }}</div>
    <el-tag :type="statusInfo.type" size="small" class="item-status">
      {{ statusInfo.text }}
    </el-tag>
    <el-button
      v-if="canEdit"
      text
      size="small"
      class="item-action"
      @click="emit('edit', record)"
    >
      编辑
    </el-button>
  </div>
</template>

<style scoped>
.record-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  transition: all var(--transition-fast);
}
.record-item:hover {
  background: var(--bg-hover);
}
.item-time {
  flex: 1;
  color: var(--text-secondary);
  font-family: 'Plus Jakarta Sans', monospace;
  font-variant-numeric: tabular-nums;
  font-size: var(--font-xs);
}
.item-duration {
  color: var(--text-primary);
  font-weight: 600;
  min-width: 48px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.item-status {
  min-width: 56px;
  text-align: center;
}
.item-action {
  color: var(--primary-color);
  font-weight: 500;
  transition: all var(--transition-fast);
}
.item-action:hover {
  color: var(--primary-light);
}
</style>
