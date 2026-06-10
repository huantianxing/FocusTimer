<script setup>
/**
 * 计时参数设置：番茄钟工作时长、短休息、长休息、循环次数
 */
import { ref, computed, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { ElMessage } from 'element-plus'

const settingsStore = useSettingsStore()
const saving = ref(false)

const workMinutes = ref(25)
const shortBreak = ref(5)
const longBreak = ref(15)
const cycles = ref(4)

onMounted(() => {
  workMinutes.value = settingsStore.settings.pomodoro_work_minutes
  shortBreak.value = settingsStore.settings.pomodoro_short_break
  longBreak.value = settingsStore.settings.pomodoro_long_break
  cycles.value = settingsStore.settings.pomodoro_cycles
})

async function save() {
  saving.value = true
  try {
    await settingsStore.save({
      pomodoro_work_minutes: workMinutes.value,
      pomodoro_short_break: shortBreak.value,
      pomodoro_long_break: longBreak.value,
      pomodoro_cycles: cycles.value
    })
    ElMessage.success('计时设置已保存')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="timer-settings">
    <h4>计时设置</h4>
    <el-form label-position="top">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="工作时长（分钟）">
            <el-input-number v-model="workMinutes" :min="1" :max="120" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="短休息（分钟）">
            <el-input-number v-model="shortBreak" :min="1" :max="30" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="长休息（分钟）">
            <el-input-number v-model="longBreak" :min="1" :max="60" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="循环次数">
            <el-input-number v-model="cycles" :min="1" :max="10" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-button type="primary" :loading="saving" @click="save">保存计时设置</el-button>
  </div>
</template>

<style scoped>
.timer-settings h4 {
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
</style>
