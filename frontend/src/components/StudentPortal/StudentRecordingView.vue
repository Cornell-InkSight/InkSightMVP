<template>
<div class="video-container">
  <video
    id="student-live-view"
    class="video-js vjs-default-skin vjs-big-play-centered"
    controls
    autoplay
    muted
    preload="auto"
    width="100%"
    height="100%"
  ></video>
</div>
</template>

<script setup lang="ts">
import videojs from "video.js";
import { onMounted } from "vue";

const liveStreamUrl = "https://your.streaming.server/live/streamkey.m3u8"; // HLS URL from your streaming server

/**
 * Lifecycle hook called when the component is mounted.
 * Fetches and sets data for livestream
 */
onMounted(() => {
  const player = videojs("student-live-view", {
      sources: [{ src: liveStreamUrl, type: "application/x-mpegURL" }],
      autoplay: true,
      controls: true,
  });

  player.play();
});
</script>

<style>
.video-container {
  max-width: 100%;
  aspect-ratio: 16 / 9;
  background-color: black;
}
</style>
