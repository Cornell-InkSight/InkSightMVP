<template>
    <!-- Approval Check -->
    <div v-if="course.isApprovedForCourse">
        <!-- Notes Packets -->
        <div v-if="course.notesPackets && course.notesPackets.length > 0" class="mb-4">
        <h4 class="text-sm font-semibold text-gray-700">Recent Notes Packets:</h4>
        <ul class="mt-1 space-y-1">
            <li 
            v-for="packet in course.notesPackets" 
            :key="packet.id" 
            class="text-sm text-gray-500 bg-gray-50 rounded-md p-2 hover:bg-gray-100"
            >
            <div class="text-blue-500 hover:underline">
                <router-link :to="`/notepackets/${packet.id}/`" target='_blank'>
                Study Guide from Lecture Session {{ packet.lecture_session_id }}
                </router-link>
            </div>
            </li>
        </ul>
        </div>
        <p v-else class="text-sm text-gray-500">No recent notes packets available.</p>
    </div>
    <!-- Not Approved Message -->
    <div v-else class="text-sm text-red-500">
        You are not approved for this course. Please request access in the Requests tab.
    </div>
    </template>
    
    <script setup>
    const props = defineProps({
    course: {
        type: Object,
        required: true,
    },
    });
    </script>