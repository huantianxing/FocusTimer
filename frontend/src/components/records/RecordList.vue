<script setup>
/**
 * 今日记录分组列表
 * 相同标题任务自动合并显示，组头显示累计时长
 * 可展开查看详细记录
 */
import { ref, computed, onMounted } from 'vue'
import { useRecordsStore } from '@/stores/records'
import { useTimerStore } from '@/stores/timer'
import { formatCompact, formatTimeOnly } from '@/utils/timeFormat'
import RecordItem from './RecordItem.vue'
import RecordEditModal from './RecordEditModal.vue'

const recordsStore = useRecordsStore()
const timerStore = useTimerStore()

const expandedGroups = ref(new Set())
const editRecord = ref(null)
const showEditModal = ref(false)

// 将平铺记录按标题分组
const groupedRecords = computed(() => {
  const records = recordsStore.todayRecords
  if (!Array.isArray(records)) return []

  // 如果后端已分组
  if (records.length > 0 && records[0].title && records[0].records) {
    return records
  }

  // 前端自行分组
  const map = new Map()
  records.forEach(r => {
    const key = r.title
    if (!map.has(key)) {
      map.set(key, { title: key, records: [], total_seconds: 0 })
    }
    const group = map.get(key)
    group.records.push(r)
    group.total_seconds += r.duration_seconds || 0
  })
  return Array.from(map.values())
})

function toggleGroup(title) {
  if (expandedGroups.value.has(title)) {
    expandedGroups.value.delete(title)
  } else {
    expandedGroups.value.add(title)
  }
}

function handleEdit(record) {
  editRecord.value = record
  showEditModal.value = true
}

function onEditSaved() {
  recordsStore.fetchTodayRecords()
  timerStore.refresh()
}

onMounted(() => {
  recordsStore.fetchTodayRecords()
})
</script>

<template>
  <div class="record-list">
    <div class="list-header">
      <h3>今日记录</h3>
      <el-button text size="small" @click="recordsStore.fetchTodayRecords()">
        刷新
      </el-button>
    </div>

    <div v-if="!groupedRecords.length" class="empty-state">
      暂无记录，开始你的第一个专注任务吧
    </div>

    <div
      v-for="group in groupedRecords"
      :key="group.title"
      class="record-group"
    >
      <!-- 组头 -->
      <div class="group-header" @click="toggleGroup(group.title)">
        <el-icon class="group-arrow" :class="{ expanded: expandedGroups.has(group.title) }">
          <component :is="'ArrowRight'" />
        </el-icon>
        <span class="group-title">{{ group.title }}</span>
        <el-tag v-if="group.records?.[0]?.tags?.length" size="small" class="group-tags">
          <span
            v-for="tag in group.records[0].tags"
            :key="tag.id"
            :style="{ color: tag.color }"
            style="margin-right:4px"
          >#{{ tag.name }}</span>
        </el-tag>
        <span class="group-duration">{{ formatCompact(group.total_seconds) }}</span>
        <span class="group-count">{{ group.records?.length || 0 }}次</span>
      </div>

      <!-- 展开的记录列表 -->
      <div v-if="expandedGroups.has(group.title)" class="group-items">
        <RecordItem
          v-for="record in (group.records || [])"
          :key="record.id"
          :record="record"
          @edit="handleEdit"
        />
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <RecordEditModal
      :visible="showEditModal"
      :record="editRecord"
      @update:visible="showEditModal = $event"
      @saved="onEditSaved"
    />
  </div>
</template>

<style scoped>
.record-list {
  padding: var(--space-md);
}
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--border-subtle);
}
.list-header h3 {
  font-size: var(--font-md);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
.empty-state {
  text-align: center;
  color: var(--text-muted);
  padding: var(--space-2xl) 0;
  font-size: var(--font-sm);
  line-height: 1.6;
}
.record-group {
  margin-bottom: 2px;
}
.group-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 12px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.group-header:hover {
  background: var(--bg-hover);
}
.group-arrow {
  transition: transform var(--transition-fast);
  font-size: 12px;
  color: var(--text-muted);
  flex-shrink: 0;
}
.group-arrow.expanded {
  transform: rotate(90deg);
}
.group-title {
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: var(--font-sm);
  letter-spacing: -0.01em;
}
.group-tags {
  flex-shrink: 0;
}
.group-duration {
  color: var(--primary-color);
  font-weight: 700;
  font-size: var(--font-sm);
  flex-shrink: 0;
  min-width: 48px;
  text-align: right;
}
.group-count {
  color: var(--text-muted);
  font-size: var(--font-xs);
  flex-shrink: 0;
}
.group-items {
  padding: var(--space-xs) 0 var(--space-sm) 28px;
}
</style>
