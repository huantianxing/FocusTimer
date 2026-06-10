<script setup>
/**
 * 音量控制 — 🔊 图标 + 悬停弹出滑块
 */
import { ref } from 'vue'
import { useSoundStore } from '@/stores/sound'

const soundStore = useSoundStore()
const showSlider = ref(false)

let hideTimer = null

function showSliderPanel() {
  clearTimeout(hideTimer)
  showSlider.value = true
}

function hideSliderPanel() {
  hideTimer = setTimeout(() => {
    showSlider.value = false
  }, 300)
}

function onVolumeChange(val) {
  soundStore.setVolume(val)
}

function toggleEnabled() {
  soundStore.setEnabled(!soundStore.enabled)
}
</script>

<template>
  <div
    class="sound-control"
    @mouseenter="showSliderPanel"
    @mouseleave="hideSliderPanel"
  >
    <el-button
      class="sound-btn"
      text
      @click="toggleEnabled"
    >
      {{ soundStore.enabled ? '🔊' : '🔇' }}
    </el-button>

    <transition name="el-fade-in">
      <div v-if="showSlider" class="volume-slider-panel">
        <el-slider
          :model-value="soundStore.volume"
          :min="0"
          :max="100"
          :step="5"
          vertical
          height="100px"
          @update:model-value="onVolumeChange"
        />
        <span class="volume-label">{{ soundStore.volume }}%</span>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.sound-control {
  position: relative;
  display: inline-flex;
  align-items: center;
}
.sound-btn {
  font-size: 18px;
  padding: 4px 8px;
}
.volume-slider-panel {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
.volume-label {
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
