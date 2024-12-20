<template>
  <section class="bg-gray-50 flex items-center justify-center">
    <div v-if="!isActiveStream" class="flex flex-col items-center w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <h2 class="text-3xl font-extrabold text-gray-800 mb-6">Join a Live Stream</h2>

      <!-- Description -->
      <p class="text-sm md:text-base text-gray-600 mb-6 text-center">
        Enter the Stream ID to start watching.
      </p>

      <!-- Input Field -->
      <input
        type="text"
        v-model="callId"
        placeholder="Stream ID"
        class="w-full px-4 py-3 mb-6 border border-gray-300 rounded-lg shadow-sm focus:ring focus:border-gray-800 text-gray-800"
        aria-label="Enter Stream ID"
      />

      <!-- Action Button -->
      <button
        class="w-full px-6 py-3 bg-black text-white font-semibold rounded-lg shadow-md hover:bg-gray-800 transition-all duration-200"
        @click="validateCallId"
      >
        Watch Stream
      </button>

      <!-- Validation Error -->
      <p v-if="validationError" class="text-red-500 text-sm mt-4 text-center">
        Invalid Stream ID. Please try again.
      </p>
    </div>

    <div v-else class="flex flex-col items-center w-full">
      <!-- Video Section -->
      <div class="w-full max-w-5xl bg-black rounded-xl overflow-hidden shadow-md relative">
        <VideoComponent :call="call" :participant="remoteParticipant"  :isBroadcaster="false" />
        <span class="absolute top-4 left-4 bg-red-600 text-white text-sm px-4 py-2 rounded-full shadow-md font-semibold">
          🔴 Live Stream
        </span>
      </div>

      <!-- Leave Stream Button -->
      <button
        class="mt-6 px-6 py-3 bg-black text-white font-semibold rounded-lg shadow-md hover:bg-gray-800 transition-all duration-200"
        @click="endStream()"
      >
        Leave Stream
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useStreamStore } from '@/stores/streamStore'
import VideoComponent from '@/components/Streaming/CameraView.vue'

const store = useStreamStore()

const { call, remoteParticipant } = storeToRefs(store)

const callId = ref('');
const isActiveStream = ref(false);
const validationError = ref(false);
const initialized = ref(false);

const props = defineProps({
  lectureSessionValidCode: String
})

const showRemoteVideo = computed(() => {
  return call.value && remoteParticipant.value
})


function watchStreamHandler() {
  store
    .watchStream(callId.value)
    .then(() => {
      isActiveStream.value = true;
      callId.value = '';
    })
    .catch((error) => {
      console.error("Error starting stream:", error);
    });
}

function endStream() {
  store.leaveStream();
  isActiveStream.value=false;
}


/**
 * Validate the Stream ID
 */
const validateCallId = () => {
    const validCallId = props.lectureSessionValidCode;
    console.log(validCallId)
    if (callId.value === validCallId) {
      watchStreamHandler();
        validationError.value = false;
    } else {
        validationError.value = true;
    }
};


onMounted(async () => {
  try {
    await store.loadUserData(); // Ensure data is loaded

    // Dynamically destructure `storeToRefs` after loading

    initialized.value = true; // Mark the store as initialized
  } catch (error) {
    console.error("Failed to load user data:", error);
  }
});

</script>
