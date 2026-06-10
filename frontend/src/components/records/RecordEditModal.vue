<script setup>
/**
 * 记录编辑弹窗
 * 可修改标题、开始/结束时间、标签
 */
import { ref, watch, computed } from 'vue'
import { updateRecord, getTags } from '@/api'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: { type: Boolean, default: false },
  record: { type: Object, default: null }
})
const emit = defineEmits(['update:visible', 'saved'])

const title = ref('')
const startTime = ref('')
const endTime = ref('')
const selectedTagIds = ref([])
const tags = ref([])
const submitting = ref(false)

const titleError = computed(() => {
  if (!title.value.trim()) return ''
  if (title.value.trim().length > 50) return '标题不能超过50个字符'
  return ''
})

function toDatetimeLocal(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toISOString().slice(0, 16) // 'YYYY-MM-DDTHH:mm' 格式
}

watch(() => props.record, (rec) => {
  if (rec) {
    title.value = rec.title || ''
    startTime.value = toDatetimeLocal(rec.start_time)
    endTime.value = toDatetimeLocal(rec.end_time)
    selectedTagIds.value = (rec.tag_ids || []).map(Number)
  }
}, { immediate: true })

watch(() => props.visible, async (val) => {
  if (val) {
    try {
      const res = await getTags()
      if (res.code === 200) tags.value = res.data || []
    } catch { /* ignore */ }
  }
})

async function handleSave() {
  if (!title.value.trim() || title.value.trim().length > 50) return
  submitting.value = true
  try {
    const data = {
      title: title.value.trim(),
      tag_ids: selectedTagIds.value
    }
    if (startTime.value) data.start_time = new Date(startTime.value).toISOString()
    if (endTime.value) data.end_time = new Date(endTime.value).toISOString()

    const res = await updateRecord(props.record.id, data)
    if (res.code === 200) {
      ElMessage.success('修改成功')
      emit('saved')
      handleClose()
    }
  } finally {
    submitting.value = false
  }
}

function handleClose() {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="编辑记录"
    width="480px"
    @close="handleClose"
  >
    <el-form label-position="top">
      <el-form-item label="任务标题" :error="titleError">
        <el-input v-model="title" maxlength="50" show-word-limit />
      </el-form-item>
      <el-form-item label="开始时间">
        <el-input v-model="startTime" type="datetime-local" />
      </el-form-item>
      <el-form-item label="结束时间">
        <el-input v-model="endTime" type="datetime-local" />
      </el-form-item>
      <el-form-item label="标签">
        <el-select v-model="selectedTagIds" multiple style="width:100%" placeholder="选择标签" collapse-tags>
          <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id">
            <span :style="{ display:'inline-block',width:'12px',height:'12px',borderRadius:'50%',background:tag.color,marginRight:'6px' }" />
            {{ tag.name }}
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>
</template>
