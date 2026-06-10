<script setup>
/**
 * 开始任务弹窗
 * - 标题输入（必填，1-50字符），自动聚焦
 * - 标签多选
 * - 快捷模板区域（一键开始常用任务）
 */
import { ref, onMounted, computed, nextTick } from 'vue'
import { useTimerStore } from '@/stores/timer'
import { useSoundStore } from '@/stores/sound'
import { getTags, getTemplates } from '@/api'

const props = defineProps({
  visible: { type: Boolean, default: false }
})
const emit = defineEmits(['update:visible', 'started'])

const timerStore = useTimerStore()
const soundStore = useSoundStore()

// 表单数据
const title = ref('')
const selectedTagIds = ref([])

// 标签列表
const tags = ref([])

// 模板列表
const templates = ref([])

const submitting = ref(false)
const titleInputRef = ref(null)

// 标题校验
const titleError = computed(() => {
  if (!title.value.trim()) return ''
  if (title.value.trim().length > 50) return '标题不能超过50个字符'
  return ''
})

async function loadData() {
  try {
    const [tagsRes, templatesRes] = await Promise.all([
      getTags(),
      getTemplates()
    ])
    if (tagsRes.code === 200) tags.value = tagsRes.data || []
    if (templatesRes.code === 200) templates.value = templatesRes.data || []
  } catch { /* ignore */ }
}

async function handleStart() {
  const t = title.value.trim()
  if (!t || t.length > 50) return

  submitting.value = true
  try {
    const res = await timerStore.start({
      title: t,
      tag_ids: selectedTagIds.value
    })
    if (res.code === 200) {
      soundStore.play('start')
      emit('started')
      handleClose()
    }
  } finally {
    submitting.value = false
  }
}

function handleTemplateClick(tmpl) {
  title.value = tmpl.title
  if (tmpl.tag_ids) {
    selectedTagIds.value = Array.isArray(tmpl.tag_ids)
      ? tmpl.tag_ids.map(Number)
      : tmpl.tag_ids.split(',').filter(Boolean).map(Number)
  }
  // 自动聚焦并开始
  nextTick(() => handleStart())
}

function handleClose() {
  title.value = ''
  selectedTagIds.value = []
  emit('update:visible', false)
}

// 弹窗打开时加载数据 + 聚焦
onMounted(() => {
  loadData()
})
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="开始计时"
    width="480px"
    :close-on-click-modal="false"
    @open="() => { loadData(); nextTick(() => titleInputRef?.focus()) }"
    @close="handleClose"
  >
    <!-- 快捷模板 -->
    <div v-if="templates.length" class="quick-templates">
      <div class="section-label">快速开始</div>
      <div class="template-list">
        <el-tag
          v-for="tmpl in templates"
          :key="tmpl.id"
          class="template-tag"
          type="info"
          @click="handleTemplateClick(tmpl)"
        >
          {{ tmpl.title }}
        </el-tag>
      </div>
    </div>

    <!-- 标题输入 -->
    <el-form label-position="top" @submit.prevent="handleStart">
      <el-form-item label="任务标题" :error="titleError">
        <el-input
          ref="titleInputRef"
          v-model="title"
          placeholder="输入任务标题（1-50字符）"
          maxlength="50"
          show-word-limit
          clearable
          @keyup.enter="handleStart"
        />
      </el-form-item>

      <!-- 标签选择 -->
      <el-form-item label="标签">
        <el-select
          v-model="selectedTagIds"
          multiple
          placeholder="选择标签（可选）"
          style="width: 100%"
          collapse-tags
        >
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          >
            <span
              :style="{ display:'inline-block',width:'12px',height:'12px',borderRadius:'50%',background:tag.color,marginRight:'6px' }"
            />
            {{ tag.name }}
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button
        type="primary"
        :disabled="!title.trim() || title.trim().length > 50"
        :loading="submitting"
        @click="handleStart"
      >
        开始计时
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.quick-templates {
  margin-bottom: var(--space-lg);
  padding: var(--space-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}
.section-label {
  font-size: var(--font-xs);
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: var(--space-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.template-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}
.template-tag {
  cursor: pointer;
  transition: all var(--transition-fast);
  border-radius: var(--radius-sm);
  font-weight: 500;
}
.template-tag:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
</style>
