<template>
<section class="content-section" v-if="isCallLive">
    <div class="flex flex-col items-center justify-center h-screen bg-gray-900">
    <!-- Video Component -->
    <div class="relative w-full h-[80vh] max-w-5xl bg-black rounded-lg overflow-hidden">
        <VideoComponent :call="call" :participant="localParticipant" />
        <span
        class="absolute top-2 left-2 bg-red-600 text-white text-sm px-3 py-1 rounded-full"
        >
        🔴 Live Broadcast
        </span>
    </div>

    <!-- Controls -->
    <div class="flex gap-4 mt-4">
        <button
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md"
        @click="goLiveClicked"
        >
        {{ buttonText }}
        </button>
    </div>
    </div>
</section>

<section v-if="!isCallLive" class="input-form content-section h-screen flex flex-col items-center justify-center bg-gray-100">
    <div class="w-1/2 text-center">
    <h1 class="text-2xl font-semibold mb-4">Start a Broadcast</h1>
    <input
        type="text"
        v-model="callId"
        placeholder="Enter call ID"
        class="w-full p-3 mb-4 border border-gray-300 rounded-lg"
    />
    <button
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md"
        @click="startBroadcast"
    >
        Start Broadcast
    </button>
    </div>
</section>
</template>

<style scoped>
.content-section {
width: 100%;
height: 100%;
}
video {
width: 100%;
height: 100%;
object-fit: cover;
}
</style>
  

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useStreamStore } from '@/stores/streamStore'
import { addNewLectureSession, addNewNotesPacket } from "@/services/api/add"
import { updateStatusOfLecture } from "@/services/api/add"
import { faker } from '@faker-js/faker';

import VideoComponent from '@/components/Streaming/CameraView.vue'

const store = useStreamStore()
const lectureSessionId = ref<string | null>(null);
const isRecording = ref(false); 

const props = defineProps<{ courseId: string }>();  

const initialized = ref(false);
const callId = ref('')

// const call = ref(null);
// const localParticipant = ref(null);
// const isBackstage = ref(null);

let { call, localParticipant, isBackstage } = storeToRefs(store);

// Computed property for whether the call is live
let isCallLive, buttonText;

function startBroadcast() {
    if (callId.value) {
        store.createCall(callId.value)
    }
}

async function goLiveClicked() {
  if (isBackstage.value) {
    await call.value?.goLive()
    startRecording()
  } else {
    await call.value?.stopLive()
    store.endCall()
    stopRecording();
  }
}

/**
 * Starts the recording, creates new lecture in the API and calls the POST API
 */
 const startRecording = async () => {
    try {
        // API call to create lecture session
        const lectureSessionData = {
            date: new Date(),
            course_id: parseInt(props.courseId),
            status: "recording",
            url: "https://example.com/stream-url",
        };

        const response = await addNewLectureSession(lectureSessionData);
        lectureSessionId.value = response.id;
        console.log("Lecture session created:", response);
    } catch (error) {
        console.error("Failed to start recording:", error);
    }
};

/**
 * Ends recording, downloads file using recorder uploads new notes packet to the API
 */

 const fakeNote = ref<string>(faker.lorem.paragraph(2)); // Generate a fake note using faker

const stopRecording = async () => {
    if (!lectureSessionId.value) return; 

    const notes_packet_data = {
        "lecture_session_id": lectureSessionId.value,
        "course_id": props.courseId,
        "notes": fakeNote.value,
        "status": "draft",
    };

    await addNewNotesPacket(notes_packet_data);

    try {
        const response = await updateStatusOfLecture(lectureSessionId.value, "done");
        isRecording.value = false;
        console.log("Lecture session stopped:", response);
    } catch (error) {
        console.error("Failed to stop recording:", error);
    }
};

 // Define computed properties after the store is ready
 isCallLive = computed(() => call.value && localParticipant.value);
buttonText = computed(() => (isBackstage.value ? 'Go live' : 'End broadcast'));

onMounted(async () => {
  try {
    await store.loadUserData(); // Ensure data is loaded
    console.log("User data loaded successfully.");
    console.log(store.streamVideoClient)

    // Dynamically destructure `storeToRefs` after loading

    initialized.value = true; // Mark the store as initialized
  } catch (error) {
    console.error("Failed to load user data:", error);
  }
});

</script>