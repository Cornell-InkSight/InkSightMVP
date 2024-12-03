<template>
   <!-- Enter Stream ID Screen -->
   <div
        v-if="!isActiveStream"
        class="input-form flex flex-col items-center bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white p-8 rounded-lg shadow-lg w-full"
      >
          <h2 class="text-2xl font-bold mb-4 w-full h-full">Join a Live Stream</h2>
          <p class="text-sm md:text-base text-gray-600 dark:text-gray-400 mb-6">
            Enter the Stream ID to start watching.
          </p>
          <input
            type="text"
            v-model="callId"
            placeholder="Stream ID"
            class="w-full p-3 mb-4 border border-gray-300 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-700 dark:text-white"
            aria-label="Enter Stream ID"
          />
          <button
            class="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200"
            @click="validateCallId"
          >
            Watch Stream
          </button>
          <p v-if="validationError" class="text-red-500 text-sm mt-2">
            Invalid Stream ID. Please try again.
          </p>
  </div>
  <div v-else>
     <section class="content-section flex flex-col justify-center items-center bg-gray-900">
      <div class="w-full max-w-5xl bg-black rounded-lg overflow-hidden relative">
        <VideoComponent :call="call" :participant="remoteParticipant" />
        <span class="absolute top-4 left-4 bg-red-600 text-white text-sm px-3 py-1 rounded-full">
          🔴 Live Stream
        </span>
      </div>
      <button
        class="mt-4 px-6 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg shadow-md"
        @click="endStream()"
      >
        Leave Stream
      </button>
    </section>
  </div>
  <!-- <section v-if="!showRemoteVideo" class="input-form flex flex-col items-center bg-gray-100 h-full justify-center">
    <input
      type="text"
      v-model="callId"
      placeholder="Enter stream ID to join"
      class="p-3 w-3/4 max-w-md mb-4 border border-gray-300 rounded-lg"
    />
    <button
      class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md"
      @click="watchStream"
    >
      Watch Stream
    </button>
  </section> -->
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useStreamStore } from '@/stores/streamStore'
import VideoComponent from '@/components/Streaming/CameraView.vue'
const store = useStreamStore()
const { call, remoteParticipant } = storeToRefs(store)

const callId = ref('');
const isActiveStream = ref(false);
const validationError = ref(false);

const showRemoteVideo = computed(() => {
  return call.value && remoteParticipant.value
})

function watchStream() {
  isActiveStream.value = true;
  store.watchStream(callId.value)
  callId.value = "";
}

function endStream() {
  store.leaveStream();
  isActiveStream.value=false;
}


/**
 * Validate the Stream ID
 */
const validateCallId = () => {
    const validCallId = "12345";
    if (callId.value === validCallId) {
        watchStream();
        validationError.value = false;
    } else {
        validationError.value = true;
    }
};

</script>
