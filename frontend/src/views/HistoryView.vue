<script setup>
/**
 * 历史记录页
 * 筛选工具栏 + 分页表格
 */
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRecordsStore } from '@/stores/records'
import { getTags } from '@/api'
import { formatDateTime, formatHumanReadable } from '@/utils/timeFormat'

const router = useRouter()
const recordsStore = useRecordsStore()

// 筛选参数
const filters = reactive({
  start_date: '',
  end_date: '',
  keyword: '',
  tag_id: null,
  page: 1,
  size: 20
})

const tags = ref([])

const statusMap = {
  0: '进行中',
  1: '已完成',
  2: '已暂停',
  3: '已中断',
  4: '无效'
}

async function loadData() {
  try {
    const res = await getTags()
    if (res.code === 200) tags.value = res.data || []
  } catch { /* ignore */ }
  fetchRecords()
}

function fetchRecords() {
  recordsStore.fetchHistoryRecords({ ...filters })
}

function handleSearch() {
  filters.page = 1
  fetchRecords()
}

function handleReset() {
  filters.start_date = ''
  filters.end_date = ''
  filters.keyword = ''
  filters.tag_id = null
  filters.page = 1
  fetchRecords()
}

function handlePageChange(page) {
  filters.page = page
  fetchRecords()
}

function setQuickRange(days) {
  const today = new Date()
  const start = new Date()
  start.setDate(today.getDate() - days)
  filters.start_date = start.toISOString().slice(0, 10)
  filters.end_date = today.toISOString().slice(0, 10)
  filters.page = 1
  fetchRecords()
}

function goHome() {
  router.push('/')
}

onMounted(loadData)
</script>

<template>
  <div class="history-view">
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="'ArrowLeft'" text @click="goHome">返回</el-button>
        <h2>历史记录</h2>
      </div>
    </div>

    <!-- 筛选工具栏 -->
    <div class="filter-bar card">
      <el-row :gutter="12" class="filter-row">
        <el-col :xs="12" :sm="6" :md="4" class="filter-col">
          <el-date-picker
            v-model="filters.start_date"
            type="date"
            placeholder="开始日期"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-col>
        <el-col :xs="12" :sm="6" :md="4" class="filter-col">
          <el-date-picker
            v-model="filters.end_date"
            type="date"
            placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="4" class="filter-col">
          <el-input
            v-model="filters.keyword"
            placeholder="搜索标题"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :xs="12" :sm="6" :md="3" class="filter-col">
          <el-select v-model="filters.tag_id" placeholder="标签" clearable style="width:100%">
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-col>
        <el-col :xs="12" :sm="6" :md="5" class="filter-col filter-actions">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>

      <!-- 快捷筛选 -->
      <div class="quick-filters">
        <el-button size="small" @click="setQuickRange(7)">最近7天</el-button>
        <el-button size="small" @click="setQuickRange(30)">本月</el-button>
        <el-button size="small" @click="setQuickRange(60)">上月</el-button>
      </div>
    </div>

    <!-- 表格 -->
    <div class="table-wrapper card">
      <el-table
        :data="recordsStore.historyRecords"
        v-loading="recordsStore.loading"
        stripe
        style="width:100%"
        :scrollbar-always-on="false"
      >
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="任务" min-width="150" show-overflow-tooltip />
        <el-table-column label="开始时间" width="140">
          <template #default="{ row }">{{ formatDateTime(row.start_time) }}</template>
        </el-table-column>
        <el-table-column label="结束时间" width="140">
          <template #default="{ row }">{{ row.end_time ? formatDateTime(row.end_time) : '-' }}</template>
        </el-table-column>
        <el-table-column label="时长" width="100">
          <template #default="{ row }">{{ formatHumanReadable(row.duration_seconds) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : row.status === 4 ? 'danger' : 'info'" size="small">
              {{ statusMap[row.status] || '未知' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="filters.page"
          :page-size="filters.size"
          :total="recordsStore.totalCount"
          layout="total, prev, pager, next"
          small
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--space-xl);
  overflow: hidden;
  animation: fadeInUp var(--transition-slow) ease forwards;
}

.page-header {
  flex-shrink: 0;
  margin-bottom: var(--space-lg);
}
.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}
.header-left h2 {
  font-size: var(--font-xl);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin: 0;
}

/* ---- 筛选栏 ---- */
.filter-bar {
  flex-shrink: 0;
  margin-bottom: var(--space-lg);
  border-radius: var(--radius-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
  padding: var(--space-md) var(--space-lg);
}
.filter-row {
  align-items: center;
}
.filter-col {
  margin-bottom: var(--space-sm);
}
.filter-actions {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.quick-filters {
  margin-top: var(--space-sm);
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

/* ---- 表格 ---- */
.table-wrapper {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
  padding: var(--space-lg);
  overflow: hidden;
}

.table-wrapper :deep(.el-table) {
  flex: 1;
}

.table-wrapper :deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: var(--space-md);
  padding-top: var(--space-md);
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

/* ==================== 响应式 ==================== */

@media (max-width: 768px) {
  .history-view {
    padding: var(--space-md);
  }
  .filter-bar {
    padding: var(--space-md);
  }
  .table-wrapper {
    padding: var(--space-md);
  }
}

@media (max-width: 480px) {
  .history-view {
    padding: var(--space-sm);
  }
  .table-wrapper :deep(.el-table__inner-wrapper) {
    overflow-x: auto;
  }
}
</style>
