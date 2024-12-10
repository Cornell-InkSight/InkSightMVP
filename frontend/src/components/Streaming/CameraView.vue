<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Call, StreamVideoParticipant } from '@stream-io/video-client'

const props = defineProps<{
  call: Call | undefined
  participant: StreamVideoParticipant | undefined
}>()

const videoElement = ref<HTMLVideoElement | null>(null)
const audioElement = ref<HTMLAudioElement | null>(null)
const unbindVideoElement = ref<(() => void) | undefined>()
const unbindAudioElement = ref<(() => void) | undefined>()

// Canvas-related refs
const canvasElement = ref<HTMLCanvasElement | null>(null)
const context = ref<CanvasRenderingContext2D | null>(null)

onMounted(() => {
  if (videoElement.value) {
    unbindVideoElement.value = props.call?.bindVideoElement(
      videoElement.value,
      props.participant?.sessionId || 'sessionId',
      'videoTrack'
    )
  }
  if (audioElement.value) {
    unbindAudioElement.value = props.call?.bindAudioElement(
      audioElement.value,
      props.participant?.sessionId || 'sessionId',
      'audioTrack'
    )
  }

  if (canvasElement.value) {
    context.value = canvasElement.value.getContext('2d')
  }

  startCapturingFrames()
})

onUnmounted(() => {
  unbindVideoElement.value?.()
  unbindAudioElement.value?.()
})

let captureInterval: ReturnType<typeof setInterval> | undefined;

const startCapturingFrames = () => {
  if (videoElement.value && context.value) {
    captureInterval = setInterval(() => {
      const video = videoElement.value
      const canvas = canvasElement.value
      if (canvas && video) {
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        context.value!.drawImage(video, 0, 0, canvas.width, canvas.height)
        const frame = canvas.toDataURL('image/jpeg')
        const frameData = { "frame": frame }

      }
    }, 10000) 
  }
}

const stopCapturingFrames = () => {
  if (captureInterval) {
    clearInterval(captureInterval)
    captureInterval = undefined
  }
}
</script>

<template>
  <video ref="videoElement" width="100%" height="100%" />
  <audio ref="audioElement" />
  <!-- Canvas for frame extraction -->
  <canvas ref="canvasElement" style="display: none;"></canvas>
</template>

<style scoped>
video {
  object-fit: contain;
}
</style>