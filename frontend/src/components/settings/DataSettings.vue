<script setup>
/**
 * 数据管理设置：备份开关、备份路径、手动备份、关于信息
 */
import { ref, computed, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { triggerBackup } from '@/api'
import { ElMessage } from 'element-plus'

const settingsStore = useSettingsStore()
const backing = ref(false)

const autoBackup = computed({
  get: () => settingsStore.settings.auto_backup_enabled,
  set: (val) => settingsStore.save({ auto_backup_enabled: val })
})

async function handleManualBackup() {
  backing.value = true
  try {
    const res = await triggerBackup()
    if (res.code === 200) {
      ElMessage.success('备份成功')
    }
  } finally {
    backing.value = false
  }
}
</script>

<template>
  <div class="data-settings">
    <h4>数据管理</h4>

    <el-form label-position="top">
      <el-form-item label="自动备份">
        <el-switch v-model="autoBackup" active-text="开启" inactive-text="关闭" />
        <div class="form-tip">每日自动备份数据库到本地目录，保留最近30天</div>
      </el-form-item>

      <el-form-item label="手动备份">
        <el-button :loading="backing" @click="handleManualBackup">
          立即备份
        </el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <div class="about-section">
      <h4>关于</h4>
      <ul class="about-list">
        <li><strong>版本</strong>: 1.0.0</li>
        <li><strong>技术栈</strong>: Vue 3 + Element Plus + Flask + SQLite</li>
        <li><strong>数据存储</strong>: 本地 SQLite，隐私安全，无需网络</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.data-settings h4 {
  font-size: var(--font-md);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: var(--space-lg);
}
.form-tip {
  margin-top: var(--space-xs);
  font-size: var(--font-xs);
  color: var(--text-muted);
  line-height: 1.5;
}
.about-list {
  list-style: none;
  padding: 0;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}
.about-list li {
  padding: 6px 0;
  line-height: 1.5;
}
</style>
