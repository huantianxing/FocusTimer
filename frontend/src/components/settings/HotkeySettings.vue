<script setup>
/**
 * 快捷键设置 — 展示当前配置
 * Electron 全局快捷键在 Phase 5 桌面端实现
 */
import { computed, ref, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { ElMessage } from 'element-plus'

const settingsStore = useSettingsStore()
const saving = ref(false)

const hotkeyStart = ref('Ctrl+Alt+S')
const hotkeyEnd = ref('Ctrl+Alt+E')

onMounted(() => {
  hotkeyStart.value = settingsStore.settings.global_hotkey_start || 'Ctrl+Alt+S'
  hotkeyEnd.value = settingsStore.settings.global_hotkey_end || 'Ctrl+Alt+E'
})

async function save() {
  saving.value = true
  try {
    await settingsStore.save({
      global_hotkey_start: hotkeyStart.value,
      global_hotkey_end: hotkeyEnd.value
    })
    ElMessage.success('快捷键已保存')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="hotkey-settings">
    <h4>快捷键设置</h4>
    <el-alert
      title="全局快捷键需要 Electron 桌面端支持，当前仅做配置记录"
      type="info"
      :closable="false"
      style="margin-bottom:16px"
    />
    <el-form label-position="top">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="开始/暂停">
            <el-input v-model="hotkeyStart" placeholder="Ctrl+Alt+S" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束计时">
            <el-input v-model="hotkeyEnd" placeholder="Ctrl+Alt+E" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-button type="primary" :loading="saving" @click="save">保存快捷键</el-button>
  </div>
</template>

<style scoped>
.hotkey-settings h4 {
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
</style>
