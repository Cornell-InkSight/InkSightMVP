<template>
<div class="p-6 bg-white rounded-lg border border-gray-200 w-full">
    <!-- Back Button -->
    <button @click="$emit('closeModal')" class="text-blue-500 mb-4">&larr; Back to Classes</button>

    <!-- Header -->
    <h2 class="text-2xl font-bold mb-4">{{ course.name }}</h2>

    <!-- Tab Navigation -->
    <div class="flex border-b border-gray-300 mb-4">
    <button 
        v-for="tab in tabs" 
        :key="tab.id" 
        @click="activeTab = tab.id"
        :class="[
        'flex-1 text-center py-2 font-semibold',
        activeTab === tab.id ? 'text-black border-b-2 border-black' : 'text-gray-500'
        ]"
    >
        {{ tab.label }}
    </button>
    </div>

    <!-- Tab Content -->
    <div>
    <ProfessorCourseInfoView v-if="activeTab === 'info'" :course="course" />
    <ProfessorStudentRequestsView v-if="activeTab === 'approvals'" :course="course" />
    <ProfessorStudyGuideView v-if="activeTab === 'guides'" :course="course" />
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import ProfessorCourseInfoView from '@/components/ProfessorPortal/ProfessorCourseInfoView.vue';
import ProfessorStudyGuideView from '@/components/ProfessorPortal/ProfessorStudyGuideView.vue';
import ProfessorStudentRequestsView from '@/components/ProfessorPortal/ProfessorStudentRequestsView.vue';

const props = defineProps({
    course: {
        type: Object,
        required: true,
    },
});

const emit = defineEmits(['closeModal']);

const tabs = [
    { id: 'info', label: 'Information' },
    { id: 'approvals', label: 'Students' },
    { id: 'guides', label: 'Study guides' },
];

const activeTab = ref('info'); 
</script>

<style scoped>
    button {
    transition: color 0.2s ease, border-color 0.2s ease;
    }
</style>
