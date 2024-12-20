<template>
  <section class="h-[10%] bg-gray-50 flex items-center justify-center">
    <div v-if="isCallLive" class="flex flex-col items-center justify-center w-full">
      <!-- Video Component -->
      <div class="relative w-full max-w-5xl bg-black rounded-xl overflow-hidden shadow-md">
        <VideoComponent :call="call" :participant="localParticipant" :isBroadcaster="true" />
        <span
          class="absolute top-4 left-4 bg-red-600 text-white text-sm px-4 py-2 rounded-full shadow-md font-semibold"
        >
          🔴 Live Broadcast
        </span>
      </div>

      <!-- Controls -->
      <div class="flex gap-4 mt-6">
        <button
          class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md font-medium transition"
          @click="goLiveClicked"
        >
          {{ buttonText }}
        </button>
      </div>
    </div>

    <div v-else class="flex flex-col items-center w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
      <h1 class="text-3xl font-extrabold text-gray-800 mb-6">Start a Broadcast</h1>
      <input
        type="text"
        v-model="callId"
        placeholder="Enter call ID"
        class="w-full px-4 py-3 mb-6 border border-gray-300 rounded-lg shadow-sm focus:ring focus:border-blue-300"
      />
      <button
        class="w-full px-6 py-3 bg-black text-white font-bold text-white rounded-lg shadow-md font-medium transition"
        @click="startBroadcast"
      >
        Start Broadcast
      </button>
    </div>
  </section>
  <section>
    <!-- Upload Slides Section -->
    <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Upload Slides</h2>
        <p class="text-sm text-gray-600 mb-6">Share lecture slides with your students. Supported formats: PDF, PowerPoint.</p>
        
        <input 
            type="file" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:border-blue-300" 
            @change="handleFileUpload"
            accept=".pdf, .ppt, .pptx"
        />
        <button
            class="mt-4 px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md font-medium transition"
            @click="uploadSlides"
            :enabled="lectureSessionId"
        >
            Upload
        </button>

        <!-- Uploaded Files Display -->
        <div v-if="uploadedSlides.length" class="mt-6">
            <h3 class="text-lg font-semibold mb-2 text-gray-800">Uploaded Slides</h3>
            <ul class="list-disc pl-5 text-gray-700">
                <li v-for="(slide, index) in uploadedSlides" :key="index" class="mb-2">
                    {{ slide.name }} - <a :href="slide.url" target="_blank" class="text-blue-500 hover:underline">View</a>
                </li>
            </ul>
        </div>
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
import { updateStatusOfLecture, uploadSlidesForLecture } from "@/services/api/add"
import { faker } from '@faker-js/faker';
import * as interfaces from "@/services/api/interfaces";
import VideoComponent from '@/components/Streaming/CameraView.vue'
import Swal from 'sweetalert2';

const store = useStreamStore()
const lectureSessionId = ref<string | null>(null);
const isRecording = ref(false); 

const props = defineProps<{ courseId: string }>();  

const initialized = ref(false);
const callId = ref('')

const uploadedSlides = ref<{ name: string, url: string }[]>([]); // Track uploaded slides
const selectedFile = ref<File | null>(null); // Store the selected file


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
    await call.value?.goLive({ start_hls: true });
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
            call_id: callId.value,
        };

        const response = await addNewLectureSession(lectureSessionData);
        lectureSessionId.value = response.id;
        console.log(lectureSessionId.value)
        console.log("Lecture session created:", response);
    } catch (error) {
        console.error("Failed to start recording:", error);
    }
};


/** Generates a Fake Note Using Faker */
const generateFakeNote = () => {
  const fakeContent = [];
  
  for (let i = 0; i < 5; i++) {
    const type = faker.helpers.arrayElement(["text", "latex", "image"]);
    if (type === "text") {
      fakeContent.push({
        id: faker.string.ulid,
        type: "text",
        value: faker.lorem.paragraph(2),
      });
    } else if (type === "latex") {
      fakeContent.push({
        id: faker.string.ulid,
        type: "latex",
        value: faker.helpers.arrayElement([
          "E = mc^2",
          "\\frac{a}{b} + \\frac{b}{a}",
          "\\int_{a}^{b} x^2 dx",
          "\\sigma = \\sqrt{\\frac{1}{N} \\sum_{i=1}^N (x_i - \\mu)^2}",
        ]),
      });
    } else if (type === "image") {
      fakeContent.push({
        id: faker.string.ulid,
        type: "image",
        url: faker.image.url()
      });
    }
  }

  return fakeContent;
};
 
const fakeNote = ref<interfaces.NotePacketEntry[]>(generateFakeNote()); // Generate a fake note using faker

/**
 * Ends recording, downloads file using recorder uploads new notes packet to the API
 */
const stopRecording = async () => {
    if (!lectureSessionId.value) return; 

    const notes_packet_data: interfaces.NotesPacket = {
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

/**
 * Gets the URL for the call
 */
 const getCallURL = async () => {
    const resp = await call.value.getOrCreate();
    console.log(resp.call)
    const URL = resp.call.egress.hls?.playlist_url;
    console.log(URL)
}


/**
 * Handle file selection
 */
 const handleFileUpload = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile.value = target.files[0];
    }
}

const uploadSlides = async () => {
    if (!selectedFile.value) {
        alert("Please select a file before uploading.");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile.value);

    try {
        console.log(lectureSessionId.value)
        const data = await uploadSlidesForLecture(formData, lectureSessionId.value);

        Swal.fire({
            title: 'File Uploaded',
            text: `The file has been uploaded..`,
            icon: 'success',
            confirmButtonText: 'OK'
        });

        selectedFile.value = null;
        return data
    } catch (error) {
        alert(error.message || "An unexpected error occurred while uploading slides.");
    }
};

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