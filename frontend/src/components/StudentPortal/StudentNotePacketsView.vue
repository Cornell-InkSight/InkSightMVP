<template>
<!-- Notes Packets -->
<div v-if="course.studentNotePackets && course.studentNotePackets.length > 0" class="space-y-4">
    <div
    v-for="packet in course.studentNotePackets"
    :key="packet.id"
    class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg"
    >
        <!-- Left Content: Icon and Details -->
    <router-link :to="`/studentnotepackets/${packet.id}/`" target='_blank'>
    <div class="flex items-center space-x-4">
        <div>
            <h4 class="text-lg font-semibold text-gray-900">{{ packet.title }}</h4>
            <p class="text-sm text-gray-500">{{ packet.time }}</p>
        </div>
    </div>
    </router-link>


    <!-- Right Content: Menu Icon -->
    <button class="text-gray-500 hover:text-gray-700">
        <i class="fas fa-ellipsis-v"></i>
    </button>
    </div>
</div>
<p v-else class="text-center text-gray-500">No recent notes packets available.</p>
</template>

<script setup>


const props = defineProps({
course: {
    type: Object,
    required: true,
},
});
</script>

  