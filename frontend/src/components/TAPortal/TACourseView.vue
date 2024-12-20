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
    <TACourseInfoView v-if="activeTab === 'info'" :course="course" />
    <TAStudyGuideView v-if="activeTab === 'guides'" :course="course" />
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import TACourseInfoView from '@/components/TAPortal/TACourseInfoView.vue';
import TAStudyGuideView from '@/components/TAPortal/TAStudyGuideView.vue';

const props = defineProps({
    course: {
        type: Object,
        required: true,
    },
});

const emit = defineEmits(['closeModal']);

const tabs = [
    { id: 'info', label: 'Information' },
    { id: 'guides', label: 'Study Guides' },
];

const activeTab = ref('info'); 
</script>

<style scoped>
    button {
    transition: color 0.2s ease, border-color 0.2s ease;
    }
</style>
    