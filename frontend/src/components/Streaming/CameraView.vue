<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Call, StreamVideoParticipant } from '@stream-io/video-client'

const props = defineProps<{
  call: Call | undefined
  participant: StreamVideoParticipant | undefined
  isBroadcaster: boolean,
}>()

const videoElement = ref<HTMLVideoElement | null>(null)
const audioElement = ref<HTMLAudioElement | null>(null)
const unbindVideoElement = ref<(() => void) | undefined>()
const unbindAudioElement = ref<(() => void) | undefined>()

// Canvas-related refs
const canvasElement = ref<HTMLCanvasElement | null>(null)
const context = ref<CanvasRenderingContext2D | null>(null)

let mediaRecorder: MediaRecorder | null = null;
let recordedChunks: Blob[] = [];

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

  if(props.isBroadcaster) {
    startCapturingFrames();
  }
})

onUnmounted(() => {
  unbindVideoElement.value?.()
  unbindAudioElement.value?.()
  stopCapturingFrames()
})


const startCapturingFrames = () => {
  if(videoElement.value) {
    const stream = videoElement.value?.srcObject as MediaStream;
    if (!stream) return;

    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp9' });
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    };

    mediaRecorder.start(); 

  }
}

const stopCapturingFrames = async () => {
  if (mediaRecorder) {
    mediaRecorder.stop();
    console.log('Recording stopped...');

    mediaRecorder.onstop = () => {
      const fullVideoBlob = new Blob(recordedChunks, { type: 'video/webm' });

      const videoURL = URL.createObjectURL(fullVideoBlob);
      
      // sendVideoToServer(fullVideoBlob);
    };
  }
};

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