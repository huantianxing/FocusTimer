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
  padding: 6px 10px;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}
.sound-btn:hover {
  background: var(--bg-hover);
}
.volume-slider-panel {
  position: absolute;
  top: 44px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-md) var(--space-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  z-index: 1000;
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.volume-label {
  font-size: var(--font-xs);
  font-weight: 600;
  color: var(--text-secondary);
}
</style>
