<template>
<!-- Course Details -->
<div class="space-y-6">
    <!-- Request Status -->
    <div class="border border-green-500 bg-green-50 p-4 rounded-lg">
    <h3 class="text-lg font-semibold text-gray-900 mb-1">Request Status</h3>
    <p class="text-sm text-gray-700">
        Status: <span :class="course.isApprovedForCourse ? 'text-green-600' : 'text-yellow-600'">
        {{ course.isApprovedForCourse ? 'Approved' : 'Pending Approval' }}
        </span>
    </p>
    <p v-if="course.approvalDate" class="text-sm text-gray-500 mt-1">
        Approved {{ course.approvalDate }} by {{ course.approver }}
    </p>
    </div>

    <!-- Course Information -->
    <div class="border border-gray-300 bg-white p-4 rounded-lg shadow-sm">
    <h3 class="text-lg font-bold text-gray-900 mb-4">Course Information</h3>
    <ul class="text-sm text-gray-700 space-y-2">
        <li><strong class="text-gray-900">Term:</strong> {{ course.term }}</li>
        <li><strong class="text-gray-900">Course ID:</strong> {{ course.course_uid }}</li>
        <li><strong class="text-gray-900">Type:</strong> {{ course.type }}</li>
        <li><strong class="text-gray-900">Campus:</strong> {{ course.campus }}</li>
        <li><strong class="text-gray-900">Instructors:</strong> {{ course.instructor }}</li>
        <li>
        <strong class="text-gray-900">Meeting Times:</strong>
        <div class="text-gray-700 space-y-1">
            <p>{{ course.meeting_time }}</p>
            <p>{{ course.location }}</p>
        </div>
        </li>
    </ul>
    </div>
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

<style scoped>
ul li {
line-height: 1.6; 
}
</style>
  