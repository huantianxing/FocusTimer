<script setup>
/**
 * 标签管理页
 * CRUD 表格：标签名称、颜色、使用次数
 */
import { ref, onMounted } from 'vue'
import { getTags, createTag, updateTag, deleteTag } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tags = ref([])
const loading = ref(false)

// 新建/编辑表单
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

onMounted(loadTags)
</script>

<template>
  <div class="tags-view">
    <div class="page-header">
      <h2>标签管理</h2>
      <el-button type="primary" @click="openCreate">新建标签</el-button>
    </div>

    <div class="card">
      <el-table :data="tags" v-loading="loading" stripe>
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
  padding: 24px;
  overflow-y: auto;
  height: 100%;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.page-header h2 {
  font-size: 20px;
  color: var(--text-primary);
}
.color-picker-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.color-swatch {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s, transform 0.2s;
}
.color-swatch:hover {
  transform: scale(1.15);
}
.color-swatch.selected {
  border-color: var(--text-primary);
}
</style>
