<script setup lang="ts">
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

@font-face {
  font-family: Satoshi;
  src: url('@/assets/fonts/OTF/Satoshi-Bold.otf');
}

@font-face {
  font-family: Satoshi Medium;
  src: url('@/assets/fonts/OTF/Satoshi-Medium.otf');
}

body,
html {
  height: 100%;
  width: 100%;
  background: var(--page);
  color: var(--foreground-1);
  font-family: Satoshi Medium, sans-serif;
  scroll-behavior: smooth;
}
</style>
