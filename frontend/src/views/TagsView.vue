<script setup>
/**
 * 标签管理页
 * CRUD 表格：标签名称、颜色、使用次数
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTags, createTag, updateTag, deleteTag } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const tags = ref([])
const loading = ref(false)

const showDialog = ref(false)
const dialogTitle = ref('新建标签')
const form = ref({ id: null, name: '', color: '#409EFF' })
const submitting = ref(false)

const presetColors = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
  '#F8C471'
]

async function loadTags() {
  loading.value = true
  try {
    const res = await getTags()
    if (res.code === 200) {
      tags.value = (res.data || []).map(t => ({
        ...t,
        usage_count: t.usage_count || 0
      }))
    }
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.value = { id: null, name: '', color: '#409EFF' }
  dialogTitle.value = '新建标签'
  showDialog.value = true
}

function openEdit(tag) {
  form.value = { ...tag }
  dialogTitle.value = '编辑标签'
  showDialog.value = true
}

async function handleSave() {
  if (!form.value.name.trim()) {
    ElMessage.warning('标签名称不能为空')
    return
  }
  submitting.value = true
  try {
    if (form.value.id) {
      const res = await updateTag(form.value.id, {
        name: form.value.name.trim(),
        color: form.value.color
      })
      if (res.code === 200) ElMessage.success('修改成功')
    } else {
      const res = await createTag({
        name: form.value.name.trim(),
        color: form.value.color
      })
      if (res.code === 200) ElMessage.success('创建成功')
    }
    showDialog.value = false
    await loadTags()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(tag) {
  try {
    await ElMessageBox.confirm(
      `确定删除标签「${tag.name}」吗？`,
      '确认删除',
      { type: 'warning' }
    )
    const res = await deleteTag(tag.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      await loadTags()
    }
  } catch { /* 用户取消 */ }
}

function goHome() {
  router.push('/')
}

onMounted(loadTags)
</script>

<template>
  <div class="tags-view">
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="'ArrowLeft'" text @click="goHome">返回</el-button>
        <h2>标签管理</h2>
      </div>
      <el-button type="primary" @click="openCreate">新建标签</el-button>
    </div>

    <div class="table-card card">
      <el-table :data="tags" v-loading="loading" stripe style="width:100%">
        <el-table-column label="颜色" width="80">
          <template #default="{ row }">
            <span
              :style="{
                display:'inline-block',width:'24px',height:'24px',borderRadius:'50%',
                background:row.color,border:'2px solid var(--border-color)'
              }"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="color" label="色值" width="100" />
        <el-table-column prop="usage_count" label="使用次数" width="100" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" text @click="openEdit(row)">编辑</el-button>
            <el-button size="small" text type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新建/编辑弹窗 -->
    <el-dialog v-model="showDialog" :title="dialogTitle" width="400px">
      <el-form label-position="top">
        <el-form-item label="标签名称">
          <el-input v-model="form.name" placeholder="最多10个字符" maxlength="10" show-word-limit />
        </el-form-item>
        <el-form-item label="标签颜色">
          <div class="color-picker-row">
            <span
              v-for="c in presetColors"
              :key="c"
              class="color-swatch"
              :class="{ selected: form.color === c }"
              :style="{ background: c }"
              @click="form.color = c"
            />
          </div>
          <el-input v-model="form.color" placeholder="#409EFF" style="margin-top:8px" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.tags-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: var(--space-xl);
  overflow: hidden;
  animation: fadeInUp var(--transition-slow) ease forwards;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  margin-bottom: var(--space-lg);
  flex-wrap: wrap;
  gap: var(--space-sm);
}
.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}
.page-header h2 {
  font-size: var(--font-xl);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin: 0;
}

.table-card {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.table-card :deep(.el-table) {
  flex: 1;
}

.color-picker-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}
.color-swatch {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  border: 3px solid transparent;
  transition: all var(--transition-fast);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.color-swatch:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.color-swatch.selected {
  border-color: var(--text-primary);
  box-shadow: 0 0 0 3px var(--primary-glow);
}

/* ==================== 响应式 ==================== */

@media (max-width: 768px) {
  .tags-view {
    padding: var(--space-md);
  }
}

@media (max-width: 480px) {
  .tags-view {
    padding: var(--space-sm);
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
