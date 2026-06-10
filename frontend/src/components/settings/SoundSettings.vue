<script setup>
/**
 * 音效设置：开关、音量、自定义上传
 */
import { ref, computed } from 'vue'
import { useSoundStore } from '@/stores/sound'
import { uploadSound } from '@/api'
import { ElMessage } from 'element-plus'

const soundStore = useSoundStore()
const uploading = ref(false)
const uploadRef = ref(null)

const soundEnabled = computed({
  get: () => soundStore.enabled,
  set: (val) => soundStore.setEnabled(val)
})
const volume = computed({
  get: () => soundStore.volume,
  set: (val) => soundStore.setVolume(val)
})

async function handleUpload(file) {
  uploading.value = true
  try {
    const res = await uploadSound(file.file)
    if (res.code === 200) {
      soundStore.customSoundPath = res.data?.custom_sound_path
      ElMessage.success('音效上传成功')
    }
  } finally {
    uploading.value = false
  }
}

function handlePreview(eventType) {
  soundStore.play(eventType)
}
</script>

<template>
  <div class="sound-settings">
    <h4>音效设置</h4>

    <el-form label-position="top">
      <el-form-item label="音效开关">
        <el-switch v-model="soundEnabled" active-text="开启" inactive-text="关闭" />
      </el-form-item>

      <el-form-item label="音量">
        <el-slider v-model="volume" :min="0" :max="100" :step="5" show-input />
      </el-form-item>

      <el-form-item label="预览默认音效">
        <div class="preview-btns">
          <el-button size="small" @click="handlePreview('start')">开始音效</el-button>
          <el-button size="small" @click="handlePreview('pause')">暂停音效</el-button>
          <el-button size="small" @click="handlePreview('end')">结束音效</el-button>
        </div>
      </el-form-item>

      <el-form-item label="自定义音效（MP3/WAV，最大5MB）">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          accept=".mp3,.wav"
          :http-request="handleUpload"
        >
          <el-button :loading="uploading" size="small">选择文件并上传</el-button>
        </el-upload>
        <div v-if="soundStore.customSoundPath" class="custom-path">
          已上传: {{ soundStore.customSoundPath }}
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.sound-settings h4 {
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.preview-btns {
  display: flex;
  gap: 8px;
}
.custom-path {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
