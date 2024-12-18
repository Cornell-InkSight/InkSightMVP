<template>
<div class="max-w-4xl mx-auto p-6 bg-gray-100 rounded-lg shadow-lg mt-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-500 animate-pulse">
        Loading notes packet...
    </div>

    <!-- Main Content -->
    <div v-else-if="notePacket">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900">
                Notes Packet For Lecture {{ notePacket.lecture_session_id }}
            </h2>
            <span :class="statusClass(notePacket.status as string)" class="text-sm font-semibold px-2 py-1 rounded-full">
                {{ notePacket.status }}
            </span>
        </div>

        <!-- Course Information -->
        <div class="mb-4 p-4 bg-white rounded-md shadow-sm">
            <h3 class="text-xl font-semibold text-gray-800">Course: {{ courseName }}</h3>
            <p class="text-gray-600">{{ notePacket.course_id }}</p>
        </div>

        <!-- Notes Content Editor -->
        <div v-if="notePacket.notes && notePacket.notes.length" class="p-4 bg-white rounded-md shadow-sm">
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Edit Notes:</h4>
            <ul class="space-y-4">
                <li
                    v-for="(note, index) in editableNotes"
                    :key="note.id"
                    class="p-3 border-l-4 rounded-md shadow-sm"
                    :class="noteTypeClass(note.type)"
                >
                    <!-- Editable Text Notes -->
                    <div v-if="note.type === 'text'">
                        <label class="font-semibold text-gray-700">Text Note:</label>
                        <textarea v-model="note.value" class="w-full p-2 border border-gray-300 rounded-md mt-2"></textarea>
                    </div>

                    <!-- Editable LaTeX Notes -->
                    <div v-else-if="note.type === 'latex'">
                        <label class="font-semibold text-gray-700">LaTeX Note:</label>
                        <textarea v-model="note.value" class="w-full p-2 border border-gray-300 rounded-md mt-2"></textarea>
                        <div class="mt-2 text-gray-600">
                            <span v-html="renderLatex(note.value)"></span>
                        </div>
                    </div>

                    <!-- Editable Image Notes -->
                    <div v-else-if="note.type === 'image'">
                        <label class="font-semibold text-gray-700">Image Editor:</label>
                        <canvas
                            ref="canvasRefs[index]"
                            :id="`canvas-${index}`"
                            class="border mt-2 w-full h-64"
                        ></canvas>
                        <div class="flex space-x-2 mt-2">
                            <button @click="togglePen(index)" :class="penActive[index] ? 'bg-blue-500 text-white' : 'bg-gray-200'" class="px-4 py-2 rounded-md">
                                ✏️ Pen
                            </button>
                            <button @click="clearCanvas(index)" class="px-4 py-2 bg-gray-200 rounded-md">🧹 Clear</button>
                            <button @click="undo(index)" class="px-4 py-2 bg-gray-200 rounded-md">↩️ Undo</button>
                            <button @click="redo(index)" class="px-4 py-2 bg-gray-200 rounded-md">↪️ Redo</button>
                        </div>
                    </div>

                </li>
            </ul>
            <div class="flex justify-end mt-6">
                <button @click="saveNotes" :disabled="isSaving" class="px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600">
                    {{ isSaving ? "Saving..." : "Save Changes" }}
                </button>
            </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-gray-500 text-center">
            No notes available for this packet.
        </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-red-500 text-center">
        Error loading notes packet data.
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, nextTick } from 'vue';
import { fetchNotePacket, fetchCourse } from '@/services/api/fetch';
import { updateTextOfNotePacket } from '@/services/api/add';
import { useRoute } from 'vue-router';
import 'katex/dist/katex.min.css';
import katex from 'katex';

const route = useRoute();
const notePacket = ref<any>(null);
const loading = ref(true);
const isSaving = ref(false);
const courseName = ref<string>("");
const editableNotes = reactive<any[]>([]);
const canvasRefs = ref<HTMLCanvasElement[]>([]);
const penActive = reactive<boolean[]>([]);
const undoStack = reactive<Array<ImageData[]>>([]);
const redoStack = reactive<Array<ImageData[]>>([]);

/** Fetch note packet data */
const fetchNotePacketData = async (id: string) => {
    loading.value = true;
    const { data } = await fetchNotePacket(id);
    notePacket.value = data;
    editableNotes.splice(0, editableNotes.length, ...JSON.parse(JSON.stringify(data.notes || [])));
    await loadCourseName(data.course_id);
    loading.value = false;
    await nextTick(initCanvases);
};

/** Fetch course name */
const loadCourseName = async (courseId: string) => {
    const { data } = await fetchCourse(courseId);
    courseName.value = data.name;
};

/** Initialize all canvases */
const initCanvases = () => {
    editableNotes.forEach((note, index) => {
        if (note.type === 'image') {
            setupCanvas(index);
        }
    });
};

const setupCanvas = (index: number) => {
    const canvas = canvasRefs.value[index];
    if (!canvas) return;

    const imageUrl = editableNotes[index].url; 
    addImageToCanvas(imageUrl, canvas);

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    undoStack[index] = [];
    redoStack[index] = [];

    let drawing = false;

    // Add drawing functionality
    canvas.addEventListener("mousedown", () => {
        if (penActive[index]) {
            saveState(index);
            drawing = true;
            ctx.beginPath();
        }
    });
    canvas.addEventListener("mousemove", (e) => {
        if (drawing && penActive[index]) {
            ctx.lineTo(e.offsetX, e.offsetY);
            ctx.stroke();
        }
    });
    window.addEventListener("mouseup", () => {
        if (drawing) {
            drawing = false;
            ctx.closePath();
        }
    });
};


/**
 * Function to save state @ Index
 * @param index 
 */
const saveState = (index: number) => {
    const canvas = canvasRefs.value[index];
    if (!canvas) return;
    undoStack[index].push(canvas.getContext("2d")!.getImageData(0, 0, canvas.width, canvas.height));
};

/**
 * Function to undo @ Specific Index
 * @param index 
 */
const undo = (index: number) => {
    const canvas = canvasRefs.value[index];
    if (!undoStack[index].length || !canvas) return;
    redoStack[index].push(canvas.getContext("2d")!.getImageData(0, 0, canvas.width, canvas.height));
    canvas.getContext("2d")!.putImageData(undoStack[index].pop()!, 0, 0);
};

/**
 * Function redo @ Specific index
 * @param index 
 */
const redo = (index: number) => {
    const canvas = canvasRefs.value[index];
    if (!redoStack[index].length || !canvas) return;
    saveState(index);
    canvas.getContext("2d")!.putImageData(redoStack[index].pop()!, 0, 0);
};

/**
 * Function to clearCanvas @ Specific Index
 * @param index 
 */
const clearCanvas = (index: number) => {
    const canvas = canvasRefs.value[index];
    if (!canvas) return;
    saveState(index);
    canvas.getContext("2d")!.clearRect(0, 0, canvas.width, canvas.height);
};

const togglePen = (index: number) => penActive[index] = !penActive[index];

/** Save Notes */
const saveNotes = async () => {
    isSaving.value = true;
    await updateTextOfNotePacket(notePacket.value.id, editableNotes);
    isSaving.value = false;
};

/** Render LaTeX */
const renderLatex = (latex: string) => {
    try {
        return katex.renderToString(latex, { throwOnError: false });
    } catch {
        return latex;
    }
};

const addImageToCanvas = (url: string, canvas) => {
    const context = canvas.getContext('2d');
    const base_image = new Image();
    console.log(base_image, url)
    base_image.src = url;
    base_image.onload = function(){
        context.drawImage(base_image, 0, 0);
    }
}

/** Status Class */
const statusClass = (status: string) => {
    switch (status) {
        case 'approved': return 'bg-green-100 text-green-700';
        case 'edits': return 'bg-yellow-100 text-yellow-700';
        case 'draft': return 'bg-gray-100 text-gray-600';
        default: return 'bg-gray-100 text-gray-600';
    }
};

/** Note Type Class */
const noteTypeClass = (type: string) => {
    switch (type) {
        case 'text': return 'border-blue-500 bg-blue-50';
        case 'latex': return 'border-green-500 bg-green-50';
        case 'image': return 'border-yellow-500 bg-yellow-50';
        default: return 'border-gray-300 bg-gray-50';
    }
};

onMounted(async () => {
    await fetchNotePacketData(route.params.notepacketId as string);
});
</script>
