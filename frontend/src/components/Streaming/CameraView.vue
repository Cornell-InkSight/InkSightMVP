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

onMounted(() => {
  console.log(props.participant)
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
      props.participant?.sessionId || 'sessionId'
    )
  }
})

onUnmounted(() => {
  unbindVideoElement.value?.()
  unbindAudioElement.value?.()
})
</script>
<template>
  <video ref="videoElement" width="100%" height="100%" />
  <audio ref="audioElement" />
</template>

<style scoped>
video {
  object-fit: contain;
}
</style>