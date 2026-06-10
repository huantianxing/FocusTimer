<script setup>
/**
 * 历史记录页
 * 筛选工具栏 + 分页表格
 */
import { ref, reactive, onMounted, computed } from 'vue'
import { useRecordsStore } from '@/stores/records'
import { getTags } from '@/api'
import { formatDateTime, formatHumanReadable } from '@/utils/timeFormat'

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
  // 加载标签列表用于筛选
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

// 快捷日期范围
function setQuickRange(days) {
  const today = new Date()
  const start = new Date()
  start.setDate(today.getDate() - days)
  filters.start_date = start.toISOString().slice(0, 10)
  filters.end_date = today.toISOString().slice(0, 10)
  filters.page = 1
  fetchRecords()
}

onMounted(loadData)
</script>

<template>
  <div class="history-view">
    <h2>历史记录</h2>

    <!-- 筛选工具栏 -->
    <div class="filter-bar card">
      <el-row :gutter="12" align="middle">
        <el-col :span="4">
          <el-date-picker
            v-model="filters.start_date"
            type="date"
            placeholder="开始日期"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="filters.end_date"
            type="date"
            placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-col>
        <el-col :span="4">
          <el-input
            v-model="filters.keyword"
            placeholder="搜索标题"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="3">
          <el-select v-model="filters.tag_id" placeholder="标签" clearable style="width:100%">
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-col>
        <el-col :span="3">
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
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-view {
  padding: 24px;
  overflow-y: auto;
  height: 100%;
}
.history-view h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.filter-bar {
  margin-bottom: 16px;
}
.quick-filters {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}
.table-wrapper {
  min-height: 400px;
}
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
</style>
